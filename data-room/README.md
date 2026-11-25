# Vanna data room (open)

Everything here supports [company.md](../company.md). Figures as of 24 November 2026.

| File | What it holds |
|---|---|
| [RISK_MEMO.md](RISK_MEMO.md) | How the risk engine works, the backtest, correlated risk, the projected book |
| [Vanna_Risk_Model.xlsx](Vanna_Risk_Model.xlsx) | Every result; yellow cells are assumptions you can change |
| sol_backtest.csv | All 60 SOL combinations: strategy, share of maximum borrow, liquidation delay |
| xstock_backtest.csv | NVDA, TSLA, AAPL, GOOGL, daily bars since 2015 |
| distance_table.csv | Price fall to liquidation and to insolvency, by strategy |
| testnet_book_stress.csv | Instant price shocks on the real testnet book |
| backtest.py, book_stress.py | The code that produced the results |

Shared directly with named reviewers: code access, full audit reports, company documents. Contact: op@vanna.finance
