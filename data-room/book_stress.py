"""Applies instant price shocks to the real testnet book (accounts without venue positions) with the on-chain weights.
No liquidation is allowed on the way down, so bad debt here is the worst case."""
import json, sys, os, csv
SC = json.load(open(sys.argv[1]))['baseline']; OUT = os.path.dirname(os.path.abspath(__file__))
STABLE = {'USDC', 'USDT', 'JupUSD', 'kUSDC', 'USD*', 'USD* Junior'}
LT = dict(USDC=.85, USDT=.85, JupUSD=.85, SOL=.80, JitoSOL=.80, JupSOL=.80, NVDAx=.65, TSLAx=.65, AAPLx=.65, GOOGLx=.65,
          kSOL=.60, kUSDC=.60, kJitoSOL=.60, **{'USD*': .60, 'USD* Junior': .60})
def val(c, s): return c['usd'] * (1 if c['symbol'] in STABLE else 1 - s)
rows = []
for s in (0, .1, .2, .3, .4, .5, .6, .7, .8, .9):
    n = liqd = 0; bd = debt = col = 0.0; bad_n = 0
    for a in SC['covered']:
        dd = sum(x['usd'] * (1 if x['symbol'] in STABLE else 1 - s) for x in a['debts'])
        if dd <= 0.01: continue
        n += 1; w = sum(LT.get(c['symbol'], 0) * val(c, s) for c in a['collateral']); t = sum(val(c, s) for c in a['collateral'] if c['symbol'] in LT)
        debt += dd; col += t
        if w <= dd: liqd += 1
        if t < dd: bd += dd - t; bad_n += 1
    rows.append(dict(shock_pct=int(s*100), borrowers=n, liquidatable=liqd, debt_usd=round(debt), collateral_usd=round(col), insolvent_accounts=bad_n, bad_debt_usd=round(bd, 2), bad_debt_pct_of_debt=round(100*bd/debt, 3)))
with open(OUT + '/testnet_book_stress.csv', 'w') as f:
    w = csv.DictWriter(f, rows[0].keys()); w.writeheader(); w.writerows(rows)
for r in rows: print(r)
