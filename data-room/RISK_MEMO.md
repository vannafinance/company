# Vanna risk memo, 24 November 2026

Written by Vanna. Every number is in the workbook or the CSV files beside this memo. Rules source: `vanna_credit_layer`, commit 624c6a6; LTV, thresholds and bonuses read from the testnet's accounts on 24 November 2026.

## 1. The rule
Vanna watches the whole account, collateral and borrowed assets together. Each asset counts at its own weight. An account can take new risk while the sum of value times LTV is above its debt, and can be liquidated when the sum of value times liquidation threshold is at or below its debt. The app shows the second as a health factor, with liquidation at 1.10. Every token, vault share, perp and option leg is in that sum, and every action is checked against it.

| Collateral | LTV | Liquidation threshold | Max leverage, USDC kept as cash | Max leverage, all in the asset |
|---|---|---|---|---|
| USDC, USDT, JupUSD | 80% | 85% | 5.0x | 5.0x |
| SOL, JitoSOL, JupSOL | 70% | 80% | 4.5x | 3.3x |
| NVDAx, TSLAx, AAPLx, GOOGLx | 55% | 65% | 3.75x | 2.2x |
| Receipts (kUSDC, kSOL, USD*) | 50% | 60% | 3.5x | 2.0x |

The app opens at about 4x (its own buffer is health 1.15).

## 2. How far prices must fall
| Account | Fall to liquidation, full / half of maximum borrow | Fall to bad debt, full / half |
|---|---|---|
| SOL posted, USDC held as cash | 34% / 67% | none while the cash stays in the account |
| SOL posted, USDC in a yield vault | 30% / 65% | none unless the vault loses value |
| SOL posted, USDC swapped into more SOL | 13% / 33% | 30% / 46% |
| xStock posted, USDC held as cash | 37% / 68% | none while the cash stays in the account |
| xStock posted, swapped into more of it | 15% / 42% | 45% / 62% |

Check on live data: the formula reproduces the app's health factor within 0.5% on all 382 borrower accounts without perp or option positions.

## 3. Backtest
Every 6 hours from 11 August 2020 to 23 November 2026 a new loan opens and is held for 30 days: 9,060 loans per row over 3,304,455 one-minute SOL prices (Binance). All interest is charged up front at 8% APR. A liquidation fills at the lowest price between crossing the line and crossing plus the delay.

Bad debt at 75% of maximum borrow, in basis points of everything lent, per 30-day loan:

| Strategy | Liquidated within 30 days | 1 min | 5 min | 60 min | 4 hours |
|---|---|---|---|---|---|
| Cash credit | 6.4% | 0 | 0 | 0 | 0 |
| Yield carry | 7.7% | 0 | 0 | 0 | 0 |
| Delta-neutral basis | 7.2% | 0 | 0 | 0.6 | 2.0 |
| Directional long | 44.4% | 0 | 0.26 | 7.4 | 13.6 |

The worst single directional loan lost 24% of its size at a four-hour delay (May 2021). In the basis row the venue closed an unattended short early in 23% of loans, which is why hedges need their margin kept up. Stocks, daily bars since 2015, liquidated a full trading day late at the worst print: no bad debt in any of 16 rows.

## 4. Correlated risk
Loans of one kind reach their line together. Share of a steady 30-day book liquidated in the single worst hour since 2020, at 75% of maximum borrow:

| Strategy | Share | Hour |
|---|---|---|
| Directional | 74% | 19 May 2021 |
| Yield carry | 68% | 11 May 2022 |
| Cash credit | 64% | 11 May 2022 |
| Delta-neutral basis | 34% | 3 January 2024 |

If every part of the base book had its worst hour at once, about 53% of it would need liquidating: stablecoins worth about half of all loans in that hour. This is what launch caps, limits by direction, a liquidation path that sells seized collateral in the same transaction, and Risk Guardian are for.

Instant shock on the real testnet book (776 accounts; SOL, staking tokens and xStocks fall together; nobody may liquidate on the way down): $0 bad debt to -40%, $98 at -50% (0.08% of debt), $2,186 at -90% (1.9%).

## 5. Projected book by instrument (planning assumptions)
| Instrument type | Hedged | Base | Directional |
|---|---|---|---|
| Delta-neutral basis | 45% | 30% | 10% |
| Yield carry | 30% | 25% | 10% |
| Directional spot and perps | 5% | 20% | 50% |
| Options (modelled as directional) | 5% | 10% | 20% |
| xStock-backed credit | 10% | 10% | 5% |
| Cash credit and prediction markets | 5% | 5% | 5% |
| Liquidated within 30 days | 10% | 18% | 33% |
| Expected bad debt a year, 5-minute liquidation | 0.003% | 0.009% | 0.022% |
| Worst-hour liquidation share | 46% | 53% | 65% |

The testnet campaign replaces these shares with measured ones.

## 6. What the model covers
Covered: price moves of SOL and four stocks, liquidation delay, partial liquidation, the bonus, interest. Not covered: liquidator inventory, price impact of our own liquidations, oracle outage, staking-token or stablecoin depeg, contract failure, option greeks. The model uses a 7% bonus for xStocks, the testnet setting. The external economic review before mainnet takes these up.
