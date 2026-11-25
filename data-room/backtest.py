"""Vanna risk backtest. Replays the deployed liquidation rules (vanna_credit_layer, branch
feature/options-standalone, parameters read from chain 24 Nov 2026) on real price history.

Rules replicated from the program:
  open:        sum(LTV_i * value_i)  > debt      (borrow weight 1.1*LTV, line 1.10)
  liquidatable sum(LT_i  * value_i) <= debt      (weight min(1.1*LT,1), line 1.10)
  close size   100% of debt if solvency <= 1 + bonus or debt <= $100, else 50% per call
  bonus        clamp(solvency, 1, 1 + asset bonus); an underwater account pays no bonus
Modelling choice (conservative): a liquidation executes at the LOWEST price seen between the
crossing and crossing + delay, never at the crossing price.
"""
import glob, io, json, os, sys, zipfile
import numpy as np, pandas as pd

PX = sys.argv[1]; OUT = os.path.dirname(os.path.abspath(__file__))
LTV = dict(USDC=.80, USDT=.80, SOL=.70, JitoSOL=.70, XSTK=.55, VAULT=.50, PHX=.80)
LT  = dict(USDC=.85, USDT=.85, SOL=.80, JitoSOL=.80, XSTK=.65, VAULT=.60, PHX=.85)
BONUS = dict(SOL=.05, JitoSOL=.05, XSTK=.07, USDC=.05, VAULT=.05, PHX=.05)
APR = .08                      # USDC borrow APR on the test pool, 24 Nov 2026 (7.9%)

def load_minutes():
    fr = []
    for f in sorted(glob.glob(PX + '/SOLUSDT-1m-*.zip')):
        z = zipfile.ZipFile(f); raw = z.read(z.namelist()[0])
        head = 0 if raw[:4].isdigit() else 1
        d = pd.read_csv(io.BytesIO(raw), header=None, skiprows=head, usecols=[0, 1, 2, 3, 4, 7], names=['t', 'o', 'h', 'l', 'c', 'q'])
        d['t'] = np.where(d.t > 10**14, d.t // 1000, d.t); fr.append(d)
    d = pd.concat(fr).drop_duplicates('t').sort_values('t').reset_index(drop=True)
    return d

# ---- portfolios. equity at entry = 1.0. Each returns units dict at price ratio p=1 and debt ----
def build(kind, f):
    """f = share of the maximum borrow the account takes. Returns holdings {asset:(stable_value, sol_units)}, debt."""
    if kind == 'cash':   B = f * LTV['SOL'] / (1 - LTV['USDC']);  return dict(SOL=1.0, USDC=B), B
    if kind == 'long':   B = f * LTV['SOL'] / (1 - LTV['SOL']);   return dict(SOL=1.0 + B), B
    if kind == 'yield':  B = f * LTV['SOL'] / (1 - LTV['VAULT']); return dict(SOL=1.0, VAULT=B), B
    if kind == 'xstk':   B = f * LTV['XSTK'] / (1 - LTV['USDC']); return dict(XSTK=1.0, USDC=B), B
    if kind == 'xlong':  B = f * LTV['XSTK'] / (1 - LTV['XSTK']); return dict(XSTK=1.0 + B), B
    if kind == 'basis':  # USDC deposit, N long spot SOL, N short on Phoenix with margin N/2 (2x venue leverage)
        # T=1+B, N=2T/3 ; open: .7N + .8*N/2 = 1.1N > B  -> B = 1.1*(2/3)(1+B)
        k = 2/3; a = (LTV['SOL'] + LTV['PHX'] / 2) * k; B = f * a / (1 - a); N = k * (1 + B)
        return dict(SOL=N, PHX=N / 2, SHORT=N), B
    raise KeyError(kind)

def legs(h, p, venue_closed=None):
    """values and weights at price ratio p."""
    out = []
    for a, u in h.items():
        if a in ('SOL', 'JitoSOL', 'XSTK'): out.append((a, u * p))
        elif a == 'PHX': out.append((a, max(0.0, u + h['SHORT'] * (1 - p))))
        elif a != 'SHORT': out.append((a, u))
    return out

def weighted(h, p): return sum(LT[a] * v for a, v in legs(h, p))
def total(h, p):    return sum(v for a, v in legs(h, p))

def solve_line(h, B, fn):
    """highest price ratio (up to 20x entry) at which fn(h,p) <= B on the way down; 0 if never. Only valid for falling-value books."""
    lo, hi = 0.0, 20.0
    if fn(h, hi) <= B: return hi
    if fn(h, 0.0) > B: return 0.0
    for _ in range(60):
        m = (lo + hi) / 2
        if fn(h, m) > B: hi = m
        else: lo = m
    return hi

def liquidate(h, B, p, risky):
    """Repeat the program's liquidation call at price p until healthy or nothing is left."""
    h = dict(h); pen = 0.0; B0 = B
    for _ in range(40):
        if B <= 1e-9 or weighted(h, p) > B: break
        tot = total(h, p)
        if tot <= 1e-9: break
        solv = tot / B
        # basis: venue is closed first, phUSD becomes plain stable margin
        if 'PHX' in h: h['USDC'] = h.get('USDC', 0) + max(0., h['PHX'] + h['SHORT'] * (1 - p)); h.pop('PHX'); h.pop('SHORT'); continue
        a = risky if h.get(risky, 0) > 1e-12 else max((x for x in h), key=lambda x: h[x])
        val = h[a] * (p if a in ('SOL', 'JitoSOL', 'XSTK') else 1)
        mx = 1 + BONUS[a]; bonus = min(max(solv, 1.0), mx)
        rep = B if solv <= mx else B * .5
        seize = rep * bonus
        if seize > val: seize = val; rep = min(rep, val / bonus)
        h[a] -= seize / (p if a in ('SOL', 'JitoSOL', 'XSTK') else 1)
        if h[a] < 1e-12: h.pop(a)
        B -= rep; pen += seize - rep
    tot = total(h, p) if h else 0.0
    bad = max(0.0, B - tot) if weighted(h, p) <= B else 0.0
    return h, B, pen, bad

def run(px, kind, f, delay, step, horizon, hours=None):
    lo, hi, cl, vol = px.l.values, px.h.values, px.c.values, px.q.values; n = len(lo)
    n_e = liq = bad_n = venue_n = 0; bad_sum = lent = pen_sum = 0.0; worst = (0.0, None); hit = []
    for i in range(0, n - horizon, step):
        n_e += 1; s0 = cl[i]; h, B0 = build(kind, f); lent += B0; end = i + horizon; j = i + 1; was = False; bad_here = 0.0
        B = B0 * (1 + APR * horizon / 525600)                 # the whole holding period's interest is charged up front
        while j < end and B > 1e-9:
            line = solve_line(h, B, weighted)
            k = int((lo[j:end] <= line * s0).argmax()) if line > 0 else 0
            t = j + k if line > 0 and lo[j + k] <= line * s0 else end
            if 'PHX' in h:                                    # a rally that leaves the short 5% of notional: the venue closes it
                top = (1 + h['PHX'] / h['SHORT'] - .05) * s0
                k2 = int((hi[j:end] >= top).argmax()); t2 = j + k2 if hi[j + k2] >= top else end
                if t2 < t:
                    h = dict(SOL=h['SOL'], USDC=.05 * h['SHORT']); venue_n += 1; j = t2 + 1; continue
            if t >= end: break
            if not was: hit.append((px.t.values[t], 1, B0))      # one per loan, so clustering counts accounts
            was = True
            p = lo[t:t + delay + 1].min() / s0
            h, B, pen, bad = liquidate(h, B, p, 'SOL'); pen_sum += pen; bad_here += bad
            if bad > 0 or not h: break
            j = t + delay + 1
        liq += was
        if bad_here > 1e-9:
            bad_n += 1; bad_sum += bad_here
            if bad_here > worst[0]: worst = (bad_here, px.t.values[i])
    B0 = build(kind, f)[1]
    # clustering: a steady book adds one equal loan every `step` minutes and holds it `horizon` minutes
    book = horizon / step; first = pd.Series([x[0] for x in hit])
    cl_h = cl_d = 0.0; cl_when = ''
    if len(first):
        hh = first.floordiv(3600000).value_counts(); cl_h = hh.max() / book; cl_when = str(pd.to_datetime(int(hh.idxmax()) * 3600000, unit='ms'))
        cl_d = first.floordiv(86400000).value_counts().max() / book
    return dict(kind=kind, f=f, delay_min=delay, entries=n_e, liq_rate=round(liq / n_e, 5), venue_closed_short=venue_n, bad_events=bad_n,
                bad_bps_of_lent=round(1e4 * bad_sum / lent, 4), worst_bad_pct_of_loan=round(100 * worst[0] / B0, 2),
                worst_entry=str(pd.to_datetime(worst[1], unit='ms')) if worst[1] is not None else '',
                penalty_bps_of_lent=round(1e4 * pen_sum / lent, 2), worst_hour_share_of_book=round(min(cl_h, 1), 3), worst_hour=cl_when,
                worst_day_share_of_book=round(min(cl_d, 1), 3))

def stocks(sym, kind, f):
    r = json.load(open(f'{PX}/{sym}.json'))['chart']['result'][0]; q = r['indicators']['quote'][0]
    d = pd.DataFrame(dict(t=r['timestamp'], o=q['open'], l=q['low'], c=q['close'])).dropna().reset_index(drop=True)
    n = len(d); H = 21; liq = bad_n = 0; bad = lent = worst = 0.0; N = 0
    for i in range(n - H - 2):
        N += 1; h, B0 = build(kind, f); lent += B0; B = B0 * (1 + APR * 30 / 365); s0 = d.c[i]; j = i + 1; was = False; bh = 0
        while j <= i + H and B > 1e-9:
            line = solve_line(h, B, weighted)
            k = [x for x in range(j, i + H + 1) if d.l.values[x] <= line * s0]
            if line <= 0 or not k: break
            t = k[0]; was = True; p = min(d.l.values[t], d.l.values[t + 1]) / s0     # one full trading day late, at the worst print
            h, B, pen, b = liquidate(h, B, p, 'XSTK'); bh += b
            if b > 0 or not h: break
            j = t + 2
        liq += was
        if bh > 1e-9: bad_n += 1; bad += bh; worst = max(worst, bh / B0)
    return dict(sym=sym, kind=kind, f=f, entries=N, first=str(pd.to_datetime(d.t[0], unit='s').date()), liq_rate=round(liq / N, 5), bad_events=bad_n, bad_bps_of_lent=round(1e4 * bad / lent, 4), worst_bad_pct_of_loan=round(100 * worst, 2))

if __name__ == '__main__':
    px = load_minutes()
    print('minutes', len(px), pd.to_datetime(px.t.iloc[0], unit='ms'), pd.to_datetime(px.t.iloc[-1], unit='ms'))
    px.to_pickle(PX + '/sol.pkl')
    # 1. distance table
    rows = []
    for kind in ['cash', 'yield', 'long', 'basis', 'xstk', 'xlong']:
        for f in (.5, .75, 1.0):
            h, B = build(kind, f)
            rows.append(dict(kind=kind, f=f, borrowed_per_1_equity=B, leverage=1 + B,
                             drop_to_liquidation=1 - solve_line(h, B, weighted), drop_to_insolvency=1 - solve_line(h, B, total)))
    pd.DataFrame(rows).to_csv(OUT + '/distance_table.csv', index=False)
    # 2. stocks, daily, one trading day late
    st = [stocks(x, k, f) for x in ('NVDA', 'TSLA', 'AAPL', 'GOOGL') for k in ('xstk', 'xlong') for f in (.75, 1.0)]
    pd.DataFrame(st).to_csv(OUT + '/xstock_backtest.csv', index=False)
    # 3. SOL replay
    res = []
    for kind in ['cash', 'yield', 'long', 'basis']:
        for f in (.5, .75, 1.0):
            for delay in (1, 5, 30, 60, 240):
                res.append(run(px, kind, f, delay, 360, 43200)); print(res[-1], flush=True)
    pd.DataFrame(res).to_csv(OUT + '/sol_backtest.csv', index=False)
