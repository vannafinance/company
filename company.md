# Vanna: company.md

*Written for AI readers. This is the one file about Vanna: the plain-text version of the investor deck (v10, Solana Incubator, November 2026), plus the detail a technical partner would otherwise dig for. Every figure carries the date it was checked and, where it is derived, the inputs. Nothing here is a projection unless it says "scenario" or "plan". Where something is not built or not proven, this file says so. Last synced with the deck: 24 Nov 2026.*

- This file, always the latest version: https://github.com/vannafinance/company/blob/main/company.md
- Deck: on request (op@vanna.finance)
- Product (private testnet): https://test.vanna.finance, access code on request, sign in with email, test funds from the in-app faucet
- Documentation: https://docs.vanna.finance (Solana: https://docs.solana.vanna.finance). Where the docs describe an unweighted health factor, they are older than the November 2026 contracts; section 18.1 is current
- Website: https://vanna.finance
- 1-minute founder video: https://youtu.be/UApnnZ1-FiI
- X: https://x.com/vannaprotocol
- Code: private; read access for named reviewers on request (op@vanna.finance)
- Data room (view-only folder, on request): risk memo, risk model spreadsheet, backtest code and results, internal security reports, deck, code access. This file holds the results; the data room holds the documents behind them (section 16)
- Status: pre-mainnet, private testnet. In early conversations with investors. Applying to the Solana Incubator Cohort 6 (NYC, March 2027).

---

## 1. Summary

Vanna is composable credit infrastructure for DeFi. A trader, fund or AI agent posts assets they already hold (SOL, liquid staking tokens such as JitoSOL, tokenized stocks such as xStocks, stablecoins) into one **unified margin account**, borrows real assets (USDC, USDT or SOL) from Vanna's credit pools (up to 10x; the app opens at about 4x, set by collateral, section 5.2), and uses that credit across lending, spot, perps, options, prediction markets and yield vaults. Positions in the account count in one **unified health factor**. The account is a Solana program-derived address (PDA) that only Vanna's program can sign for, so borrowed funds move between connected venues, and the leveraged part of the loan can never be withdrawn.

Who it is for: active traders first; then businesses that want to offer leverage to their own customers (apps, wallets, exchanges) through an API; then funds, desks and banks through an SDK and MCP. Who it is not for: retail users looking for a savings product, and anyone who wants unsecured credit.

How it makes money: a share of the interest borrowers pay to lenders, plus fees on liquidations, delta-neutral vaults, routing, and business, Copilot and MCP usage (section 9).

## 2. The problem

- **Perp leverage is synthetic and stuck in one venue.** On a perp DEX no money is lent; leverage is a number on that venue's ledger and cannot be used anywhere else.
- **Lending is overcollateralized.** Kamino, Aave, Morpho and similar lend up to roughly 80% of what you deposit (loan-to-value below 100%), so a borrower gets less capital than they hold.
- **So liquidity and volume crowd into perps**, while spot, options, prediction markets and other DeFi venues stay thin. New chains launch a perp DEX first because it is the fastest way to volume.
- **Centralized exchanges already sell the fix**: one account, margin across products. Binance and Deribit portfolio margin, Crypto.com smart cross margin, and Coinbase Prime unified cross margin (launched March 2026). DeFi has no equivalent that spans venues.

## 3. The prize

- Hedge funds borrow about **$8 trillion** against their portfolios from prime brokers and banks ($7.95T on 30 June 2026: prime brokerage $3.69T + repo $3.38T + other secured $0.88T; OFR Hedge Fund Monitor). This is cash borrowed against collateral, the prime-brokerage model Vanna brings on-chain.
- All active loans in DeFi total about **$26 billion** (DefiLlama, 348 lending protocols summed on 24 Nov 2026; $31 billion on 5 Oct, before prices fell). The off-chain figure is about 300 times larger.
- Evidence that secured leverage is wanted on-chain: in one Kamino market, $167M was borrowed against $217M of USDe (checked 2 Oct 2026), and Coinbase has originated $2.3B+ in Morpho-powered loans (2026) because businesses want to offer credit without building it.
- About 96% of on-chain tokenized-stock trading ran on Solana in Q2 2026 (Genfinity, July 2026). Tokenized stocks are idle collateral today: there is almost nowhere to borrow against them.

## 4. What we built: traction table

| Item | Value | Checked |
|---|---|---|
| Solana programs written (Anchor) | 4: core credit layer, oracle, validator, options | 23 Nov 2026 |
| Venues integrated on Solana (testnet, mainnet fork) | Kamino (lending), Jupiter and Titan (spot), Phoenix (perps), Perena (stablecoin yield), World (prediction markets), Derive (options, via our options program) | 23 Nov 2026 |
| Venues integrated on Stellar (testnet) | Blend, Soroswap, Aquarius | 23 Nov 2026 |
| Next integration | Polymarket (prediction markets) | 23 Nov 2026 |
| Solana testnet margin accounts (428 with debt) | 843 | 24 Nov 2026 |
| Solana testnet program transactions scanned | 6,758 (since 29 Sep 2026) | 24 Nov 2026 |
| Solana testnet collateral posted / borrowed | $890K / $214K (test funds) | 24 Nov 2026 |
| Solana testnet bad debt | $0 | 24 Nov 2026 |
| Simulated instant price drop on the testnet book, no liquidations allowed | $0 bad debt up to -40%; $98 (0.08% of debt) at -50%. SOL had already fallen 31% since 29 Oct | 24 Nov 2026 |
| Backtest of the liquidation rules on SOL 1-minute prices, Aug 2020 to Nov 2026 | No bad debt at any leverage tested when liquidations land within 1 minute (9,060 loans per strategy); directional loans at 75% of max borrow lose 0.07% per 30 days if they land an hour late | 24 Nov 2026 |
| Solana testnet liquidations executed | 0 in the indexed window; the bot's liquidation scenarios run end to end on the fork (section 13) | 24 Nov 2026 |
| Stellar testnet accounts / collateral / borrowed | 39 / $94K / $22K (test funds) | 24 Nov 2026 |
| Waitlist sign-ups | 1,515 (opened 10 Oct 2026; ~450 in the first two days; 840 by 2 Nov) | 24 Nov 2026 |
| @vannaprotocol X followers | 727 (378 on 13 Oct) | 24 Nov 2026 |
| Grants and prizes | 9, over $230K (section 12) | 23 Nov 2026 |
| Mobile | Native Android app for Solana's Seeker phone, 2nd place at Solana Mobile's Clock In hackathon; being published to the Seeker dApp Store | 23 Nov 2026 |
| Paying customers / revenue | 0 / $0, by design: no real deposits before external audits | 23 Nov 2026 |

How to read the testnet numbers: balances are test funds. The Solana accounts include testers we invited and accounts we created ourselves to stress-test the risk engine; on 29 Oct 2026 an on-chain review found that about 278 of the then 489 accounts were empty or identical scripted positions. We do not quote average leverage because a handful of scripted accounts skew it. Source for all testnet figures: the analytics dashboard at test.vanna.finance (access code on request).

## 5. Product

### 5.1 One account, every market
A trader opens one **unified margin account**, posts collateral and borrows real USDC, USDT or SOL, worth more than the deposit. The loan lands in the same account and can be moved into any connected market. What it buys is held by the account and secures the loan. A withdrawal is allowed only while the assets that remain cover the debt at their loan-to-value, as in an ordinary overcollateralized loan, so the leveraged part cannot leave.

| Market | Connected venues | What a trader can do with the credit |
|---|---|---|
| Spot | Jupiter, Titan (best quote wins); Soroswap, Aquarius on Stellar | Swap any listed asset inside the account |
| Perps | Phoenix | Long or short SOL, ETH, BTC (up to 5x at the venue) and TSLA, META (up to 3x) |
| Options | Derive, through Vanna's options program | Buy or write calls and puts on SOL, ETH and BTC; 27 ready strategies (5.5) |
| Lending | Kamino; Blend on Stellar | Lend borrowed USDC, USDT or SOL and keep the receipt as collateral |
| Stable yield (farm) | Perena USD* and USD* Junior | Earn on USDC; shares stay in the account as collateral |
| Delta-neutral (farm) | Vanna basis vaults: SOL, ETH, BTC, TSLA, META (built; unlisted since the November contract upgrade, until the new oracle prices their shares) | Each vault holds the asset and an equal 1x short on Phoenix to earn funding |
| Liquidity (farm) | Aquarius and Soroswap pools on Stellar | Provide XLM/USDC liquidity |
| Prediction markets | World; Polymarket next | Bet, and earn lending yield while the bet is open (5.6) |

**Assets and markets**

| | On testnet on 24 Nov 2026 | Rolling out from the last week of November 2026 |
|---|---|---|
| Stablecoin collateral | USDC, USDT, JupUSD | PYUSD, USDG, USDY, EURC, JLUSDC |
| SOL and staking tokens | SOL, JitoSOL, JupSOL | |
| Tokenized stocks, funds and commodities | NVDAx, TSLAx, AAPLx, GOOGLx | METAx, GLDx, SPY, SLV, SPCX (SpaceX, Backpack), ANT (Anthropic, Backpack) |
| Bitcoin | | cbBTC |
| Receipts that count as collateral | kSOL, kUSDC, kUSDT, kJitoSOL, kJupSOL, USD*, USD* Junior | |
| Spot pairs | All of the above tokens | All of the added tokens |
| Perps (Phoenix) | SOL, ETH, BTC, TSLA, META | HYPE, GOLD, ZEC |
| Options (Derive) | SOL, ETH, BTC | HYPE, ZEC, XAUT |
| Borrowable | USDC, USDT, SOL | |
| Stellar | XLM and USDC | |

The right-hand column is the release scheduled for the days after this file was written; every risk figure in section 18 covers the middle column only. Each added asset gets its own limits: for example EURC moves with the euro, so it is not treated as a dollar. The contract holds 24 asset slots, so listings are sequenced against that limit.

### 5.2 Leverage and cost
- **Up to 10x.** The app opens at about 4x and the limit depends on the collateral: 4.3x against stablecoins, 3.9x against SOL and its staking tokens, 3.2x against xStocks (borrowed USDC kept as USDC, with the app's safety buffer at health 1.15). The contracts allow 5x, 4.5x and 3.75x at today's settings. Limits rise per trader through the Credit Underwriter (5.7) and per asset as liquidity allows; 10x is set by raising an asset's LTV to about 90%, which the program supports without a code change.
- Perps opened with the credit carry the venue's own leverage on top, inside the same health factor.
- **Cost:** a borrow APR set by pool utilization, not a perp funding fee. Testnet USDC pool on 24 Nov 2026: 95% utilization, 7.9% borrow APR, 6.8% supply APR. If the credit is used on perps, that venue's funding applies to the perp position, which is what makes funding strategies possible.

### 5.3 The unified health factor
One number for the whole account: 1.1 x the sum of each asset's value times its liquidation threshold, divided by debt. Collateral, borrowed cash, lending receipts, vault shares, perp equity and option legs are re-priced together after every action. Two lines use that: the liquidation line counts everything; the borrow line is stricter (options add nothing to borrowing power, an open perp counts as its collateral less the margin it uses). An action that would leave the account below its borrow line reverts on-chain. At 1.10 or below the account can be liquidated.

Why that matters: on separate venues each leg is margined alone, so a hedge can be liquidated leg by leg. In one account a $300 loss on spot and a $300 gain on the short that hedges it cancel, and the trader's other collateral stands behind both. The venue still has its own margin: Phoenix can close a short that runs out of collateral. In our backtest that happened to 23% of delta-neutral loans within 30 days when nobody topped the short up, so the short needs active margin (by the trader, Copilot or a vault).

### 5.4 Strategies traders can build
Each row uses the same account and the same health factor.

| Strategy | Legs | What it earns or protects |
|---|---|---|
| Leveraged long | Post JitoSOL, borrow USDC, swap into SOL | More SOL exposure, staking yield on the deposit |
| Leveraged directional perp | Post xStocks, borrow USDC, long or short BTC, ETH, SOL, TSLA or META on Phoenix | A view, without selling the stocks |
| Delta-neutral basis | Borrow USDC, buy SOL on Jupiter or Titan, short the same size on Phoenix | Funding, with price moves cancelling |
| Basis without managing it | Deposit borrowed USDC into a Vanna basis vault (relisting as above) | Funding; the vault runs the hedge |
| Hedge a holding | Post JitoSOL or TSLAx, short the same asset on Phoenix | Keeps the asset (and staking yield), removes the price risk |
| Yield carry | Borrow USDC, lend it on Kamino or hold Perena USD* | The yield above the borrow rate, when it is positive |
| Covered call | Hold SOL, sell calls; or a long perp plus calls for ETH and BTC | Premium; upside capped |
| Protective put, put-spread cover, collar | Hold SOL, buy puts (and sell calls for a collar) | A floor under the holding |
| Volatility | Long straddle or strangle; gamma scalp with a perp hedge | A large move either way |
| Range and premium | Iron condor, iron butterfly, calendar; short strangle with a perp delta hedge | Premium in a quiet market; some of these have uncapped losses and say so before signing |
| Mixed book | $10K USDC posted, $12K borrowed: $6K in Perena USD*, $5K in a SOL basis trade, $1K in options. Health about 1.5 (our calculation at today's weights) | One account, one health factor, several sources of return |
| Earn while you bet | Buy YES or NO on World, add it to Vanna's pool | Lending yield on the matched side |

Sizing, projected health and the liquidation price are shown before the trader signs. Positions are closed from one Portfolio page, and a guided unwind closes perps, redeems farms, swaps and repays step by step.

### 5.5 Options
Solana traders get Derive's options liquidity from the same account. A trader pays USDC into Vanna's options program escrow on Solana; Vanna's bot hedges each order 1:1 on Derive and fills it on-chain at Derive's price plus or minus Vanna's $0.20 per contract; expired series settle on a Pyth price. Traders can buy or write calls and puts. Options count in the liquidation health factor, conservatively (a bought option without a fresh price counts only its intrinsic value), and add nothing to borrowing power. On testnet, orders fill on the Solana fork and the hedge runs against Derive's testnet book.
- **Easy:** "What do you expect for ETH?" Rise, Fall, Big move, Protect or Earn. Vanna picks the best payoff for the budget and shows the most that can be lost.
- **Intermediate:** 27 named strategies in six groups (bullish, bearish, neutral, volatile, hedge, income), ranked by yield, lowest risk, most protection or lowest cost, each with its health factor before and after.
- **Pro:** the full chain, book, Greeks and a leg builder.
- Multi-leg books can include a Phoenix perp leg. The whole book is checked before anything is sent (funds, borrow line, slots); the perp leg is placed only after every option leg has filled. Written options are fully secured today (a put by its strike in USDC; a call by its price plus 25% of spot), so a spread locks more than its risk.

How much of the escrow stays on Solana versus moves to Derive (a reserve, like a bank's, so withdrawals and liquidations are paid instantly) is a business decision still open. We do not claim that user USDC never leaves Solana: on mainnet part of the escrowed funds is bridged to Derive over Circle's CCTP to fill orders.

### 5.6 Prediction markets: automated liquidity provisioning for our credit pools
A bet can be locked for months and earns nothing meanwhile. A holder of YES or NO tokens puts them in Vanna's pool; the pool matches YES with NO, merges each pair into $1 (World's CASH, swapped to USDC) through the market's own program, and lends it in the USDC credit pool. The bet stays open and matched bets earn (the fully matched side earns the full rate; the surplus side is diluted). The pool is market neutral: a YES and a NO redeem for $1 together at any odds, it never uses an outcome price, and each market's pool is isolated.

Why it matters: people who would never supply a lending pool bring liquidity to it. More trader borrowing lifts the yield, which draws more bettors, who deepen the pool. It is early: on 24 Nov 2026 the testnet had 79 pools, 11 earning, with $3,164 merged and lent. The dollar carries the credit pool's own risk and that of CASH, and a withdrawal can wait if that pool is fully used.

**World** runs on Solana, on our testnet from the trader's wallet balance, with Vanna's own test market maker filling the trades; **Polymarket** follows the Derive design: a trader bets from Vanna, and Vanna's bot places it on Polygon with Vanna's own liquidity. Bringing bets into the margin account, so that credit can fund them, is the next step of both. Open risk: Vanna funds the position on the venue side, which costs us the yield on that capital.

### 5.7 Agents
No agent can override the on-chain health check, and none holds a user's key.

**Vanna Copilot: "Claude for traders".** A trader writes a goal in plain English: "Deposit 10 JitoSOL, borrow USDC at 3x, go long BTC with 100 USDC", "lever my SOL 2x", "what happens if SOL drops 20%?", "where does my USDC earn most?", "close everything". Copilot reads the account, proposes a plan, and runs it once the trader approves.
1. **Firewall:** rules refuse out-of-scope requests (other wallets, arbitrary programs, admin actions) before the model sees them.
2. **Investigate:** Gemini 3.8 Flash on Google Vertex AI reads the live account with 30 read-only tools (health, capacity, prices, pool rates, perps, vaults, prediction markets, what-if simulation).
3. **Size:** the model never picks an amount. Vanna's code turns the request into exact amounts with the protocol's own maths.
4. **Review:** a frozen plan of up to 8 transactions with each step, its amount, warnings and health before and after. Valid for 5 minutes.
5. **Execute:** every step is re-checked against live data, built, simulated, and signed by the trader's own wallet. A borrow, withdrawal, swap or farm step that would take health below 1.15 pauses the plan; perp steps follow the contract's own line.
6. **Confirm:** a step counts as done only when the chain confirms it.

Copilot covers lending, margin, leverage, spot, farm, perps and prediction markets. Options are placed from the options builder. It does not place stop-losses, limit or scheduled orders, predict prices, or act without approval.

**Vanna MCP: the same engine for other people's agents.** A hosted Model Context Protocol server for Claude, Cursor, Codex, ChatGPT or any MCP client, on Solana and Stellar. The wallet is the login (OAuth); access can be read-only. 20 tools on Solana: portfolio, margin trades, risk and what-if, multi-step plans, lending, swaps, Kamino, vaults, Phoenix perps, prediction markets, oracle, history. Writes return an unsigned, simulated transaction and a signing link; the wallet approves the plan and signs each step, and the server checks that what was signed is byte for byte what it built. Server-enforced guardrails: a 1.15 health floor on borrowing, withdrawals and swaps, own wallet only, $5,000 per action and $25,000 per day, 8 steps per plan, exact amounts, each step sent once. For funds and quant desks, this means their own trading agents can use Vanna credit without custom integration work, inside the account's limits. Guide: https://docs.vanna.finance/solana/guides/mcp

**Risk Guardian: keeps the protocol solvent.** It watches collateral prices, liquidity on each venue, oracle gaps, pool utilization and every account's distance from liquidation. When risk rises it lowers an asset's collateral value, caps new borrowing in it and tightens leverage on new positions, inside bounds the protocol sets.

**Credit Underwriter: credit limits from behaviour.** Everyone starts at a conservative limit. The Underwriter then sets each trader's own leverage from how they trade: leverage used, time spent close to liquidation, drawdowns, how quickly they add margin. It works like a card issuer setting a credit limit. Limits change over time, never on an open position. For an AI agent this becomes its credit history.

### 5.8 Leverage as a service: credit inside other companies' products
Building a lending pool, a risk engine and a liquidation engine from scratch is the hard part of offering leverage. Vanna is that engine, offered as an API.
- **Who:** wallets, exchanges, prediction markets, brokerages and fintech apps, and issuers of tokenized assets. Wallets already partner rather than build: Phantom has earned $20M+ routing perp trades to Hyperliquid, and Coinbase has originated $2.3B+ in Morpho-powered loans.
- **What their customer sees:** leverage in the app they already use. A prediction market lets a bettor borrow USDC against JitoSOL or a tokenized stock and bet without selling; a perp exchange lets a user fund margin from spot holdings; a wallet offers a credit line against the whole portfolio.
- **An issuer's case:** holders of tokenized Treasuries, private credit or commodities hold an asset that is safe but stuck. Built on Vanna, the issuer lets its own holders borrow USDC against it without selling, under the issuer's rules (who qualifies, how it is priced, what haircut applies), and use that USDC across every connected market. The issuer gets more holders; in return it commits redemption liquidity so liquidations always clear one to one.
- **How:** a business plugs in by API or SDK and writes a **rule set**: which collateral and at what value, which venues, the leverage cap, the liquidation line. It borrows from Vanna's shared pools under its own debt ceiling, so one product's risk stays with that product.
- **Economics:** interest is split with the business, plus a platform fee. Each business brings borrowers to the same pools, which raises lender yield and deepens the liquidity the next business gets.

### 5.9 Credit APIs for funds, desks and banks
A fund posts collateral once and trades across on-chain venues instead of pre-funding each one. A desk posts tokenized Treasuries, keeps the yield and borrows stablecoins to trade. Access is through the SDK and MCP, with the institution's own collateral and user-level underwriting rules: the prime-brokerage relationship, on-chain and non-custodial.

### 5.10 Markets and venues
A venue gets deposits and volume from Vanna credit without running a lending desk: borrowed dollars become lending deposits on Kamino, spot volume on Jupiter, open interest on Phoenix, options flow on Derive. As the credit becomes where traders start, new venues and new markets want to be listed in it. Adding one means adding oracle and validator rules; the core does not change.

### 5.11 Mobile
React Native (Expo) Android app for Solana's Seeker phone with Mobile Wallet Adapter: the same account and health factor.

### 5.12 Status in one place (24 Nov 2026)
Nothing is on mainnet. Running on private testnet: the unified margin account, credit pools, oracle and validator, spot, Phoenix perps, Derive options, Kamino, Perena, World prediction markets (wallet balance), liquidation bot, risk dashboard, Vanna Copilot, Vanna MCP, web app. Built and unlisted: basis vaults. Next: the assets in 5.1, Polymarket, Risk Guardian, Credit Underwriter, programmable credit rules with the business API, then credit APIs.

## 6. Why we win
- **Leverage belongs to the account, not the venue.** Lending markets lend less than you deposit; perp venues margin only inside themselves; Vanna's credit follows the trader into every venue type.
- **We are complementary to the venues.** Lending markets, perp exchanges, options and prediction markets are where our credit goes to work. Each integration makes the credit more useful and gives the venue borrowed volume.
- **Derivatives are in the risk model.** Most credit protocols can only hold positions that are already tokens. Vanna prices open perps and option legs, and its bot closes perps before seizing anything else, which is what makes a hedge count as a hedge.
- **The engine is reusable.** The same pools, risk engine and liquidation serve our app, Copilot, MCP and every business that plugs in. Adding a venue means adding oracle and validator rules; the core program does not change.
- **The record compounds.** Code can be forked. An underwriting record of how accounts behave on credit, solvency through drawdowns, and integrations inside other products cannot.
- **The team fits the risk.** Credit protocols fail on security and risk design. Our CTO is an Immunefi All-Star; both founders are traders.

## 7. Customers today
There are no paying customers, by design: Vanna will not hold real deposits before external audits, an independent economic risk review and a live crash drill. Invited testers (traders, including hedge-fund traders, and some investors) have used the private testnets on Stellar since June 2026 and on Solana since September 2026. Their feedback has been positive; we do not yet have retention or usage cohorts that separate invited testers from our own stress-test accounts, so we do not quote any.

## 8. Go-to-market
1. Traders first: Opinder's 20K+ followers (X 7,875, LinkedIn 9,300, YouTube 3,960, Instagram 1,603, checked 24 Nov 2026), plus 849 on his Telegram channel; the 1,515-person waitlist; trader creators and trading communities planning launch AMAs; Phoenix, Titan, Soroswap, Superteam India and Canada, and the Solana and Stellar teams have agreed to promote the mainnet launch (verbal agreements, 2026).
2. Testnet points campaign: invites to the top 100 traders worldwide, then new invite waves every week, each testing the next release. Referrals earn points; the points formula is not published.
3. Prediction markets as a user and liquidity channel (5.6).
4. Seeker app on the Solana dApp Store.
5. Businesses offering Vanna credit to their own customers; each brings borrowers to the same pools.

## 9. Business model and pricing
- Borrowers pay interest; lenders earn most of it and Vanna keeps a share. Our plan is about 15% of borrow interest, near Aave and Kamino's reserve factors. The testnet reserve factor is set to 10%. The on-chain rate curve today gives 2.8% at 80% utilization and 7.9% at 95%; it will be re-set before mainnet.
- Plus: 20% of the liquidation bonus (bonus 5%), a performance fee on delta-neutral vaults (plan: 10%), routing fees on trades made with the credit, platform fees from businesses, and Copilot and MCP fees.
- Scenario, not a forecast: at about a 6% average borrow rate, $1B of loans earns about $18M a year and $5B about $80M. Close to half of that comes from routing, business and agent revenue on terms we have not yet tested. $1B is about 4% of today's DeFi lending.

## 10. Competition (live features only, as of 23 Nov 2026)
**Complementary: the venues our credit goes to work in.** Lending protocols (Kamino, Aave, Morpho), perp exchanges (Phoenix, Hyperliquid, Drift), options (Derive), spot (Jupiter, Titan) and prediction markets (World, Polymarket) are markets, and Vanna is the credit that spans them. We integrate some today and can integrate the others. They appear in the table only because investors compare them: each gives leverage or credit inside itself.

**Closest in approach:** Gearbox and Project 0, and off-chain, exchange portfolio margin.

| | Lends more than you deposit | Credit usable across other protocols' venues | Derivatives in one health factor | Non-custodial |
|---|---|---|---|---|
| Aave, Morpho, Kamino (complementary) | No | No | No | Yes |
| Drift, Hyperliquid (complementary) | Partly (within their own venue) | No | Yes | Yes |
| Gearbox (EVM) | Yes | Partly (lending and spot venues) | No | Yes |
| Aave V4 | No | Partly (spokes within Aave) | No | Yes |
| Project 0 (Solana) | No | Partly (Solana lending markets, not perps) | No | Yes |
| Exchange portfolio margin (Binance, Deribit, Coinbase Prime) | Yes | No | Yes | No |
| Vanna | Yes, on testnet | Yes, on testnet | Yes, on testnet | Yes |

- **Gearbox** lends above collateral over positions a venue has already tokenized. On 16 Nov 2026 it announced automated leverage on tokenized real-world assets through lending markets, which confirms the demand; perps, options and prediction markets are not in its risk model.
- **Aave V4** lets others set credit rules on shared liquidity inside Aave. **Project 0** unifies margin across Solana lending markets.
- **Coinbase Prime and Binance** margin a client's whole book, but only for assets in their custody, so the credit cannot follow the client on-chain.
- **Earlier attempts are the warning.** Mango Markets lost about $110M in 2022 to manipulated collateral. DeltaPrime, which ran cross-market credit accounts, was exploited twice in 2024, through a leaked admin key and an unvalidated external call. So every external call goes through one entry point to allowlisted venues, main prices fall back to a second oracle, and a multisig with a timelock is required before mainnet. We walked away from two ecosystems where we could not price positions safely.

All of these are live with real volume; Vanna is on testnet. We have not found a live protocol whose credit covers derivatives across venues.

## 11. Vision
Off-chain, a fund does not ask a futures exchange for credit, then an options exchange, then a lender. It has one prime broker: one collateral pool, one margin number, credit it can take into any market. That is how hedge funds carry about $8 trillion of borrowing. On-chain, every venue still starts from zero, so capital piles into perps and everything else stays thin, and each new chain launches another perp exchange to find volume.

We think the bigger game is the credit itself. In the order we build it:
1. **Traders.** One account that brings the tooling of centralized exchanges, and more, on-chain: real credit, hedges that count, risk shown in one number.
2. **Agents.** Trading agents become borrowers. They need credit with hard limits and a history; MCP, Copilot and the Underwriter give them both.
3. **Businesses and issuers.** Wallets, exchanges and the institutions bringing Treasuries, private credit, commodities and equities on-chain plug into the same engine. Their assets stop being stuck: holders borrow against them and use the money across every connected market.
4. **Markets.** When traders start from their credit line, not from a venue, the credit layer becomes where new markets want to be listed, because it decides where borrowed liquidity goes.

**Multi-chain, then cross-chain.** Solana and Stellar run as separate systems in one app today, because liquidating across messaging delays is a risk we will not take early. Options show the pattern: liquidity from another chain, used from Solana. Monad is next, as the home of our EVM version: our first contracts were Solidity, sub-second finality shortens the time between a breach and a liquidation, and much of DeFi's lending liquidity is EVM. Later, remote venues join one at a time, each under its own debt ceiling.

The future of credit is composable: leveraged credit that moves between markets the way it moves between banks, hedge funds and markets off-chain, for humans and their agents.

## 12. Team, history and funding

**Why us, and why this.** We each hit the problem from a different side. At Koinfox, 100K+ traders split capital across exchanges that could not see each other's positions. Vatsal built on-chain credit at Spectral and hedging vaults at Polynomial and kept meeting the same gap: credit that stops at the edge of one protocol.

**Opinder Preet Singh, Co-founder and CEO** (technical product founder; Toronto). Three-time founder with one exit; 14 years building tech products, the last ten in crypto. Led ETHLend's (now Aave) go-to-market and fundraising in India in 2017. Cofounded Koinfox, a multi-exchange trading terminal that grew to 100K+ traders, became Southeast Asia's first Binance Broker Partner and was acquired in 2020. Has traded since 2016 and runs his own AI trading agents and quant strategies. Certified in zero-knowledge cryptography; built ShieldLend, a private-lending prototype, and led product on ZTips, which won RISC Zero's integrations prize at ZK Hack Montreal 2024. Has trained 10,000+ developers, students and professionals, judged ETHGlobal Delhi (2025) and ETHDenver (2026), and backed 50+ early crypto startups since 2016. At Vanna leads product and risk design: collateral, leverage limits, liquidation thresholds, and the specs engineers build from. https://www.linkedin.com/in/opinderpreet

**Vatsal Salkiya, Co-founder and CTO** (Ahmedabad). Immunefi All-Star: 27 vulnerability reports in live DeFi protocols, 6 critical. 30+ smart-contract audits with firms including Cantina, Halborn, Pashov and Oak Security; security researcher with Halborn from August 2025 to June 2026. Nearly two years building on-chain credit at Spectral; derivatives and hedging (delta-neutral) vaults at Polynomial; delta-neutral options quant at a prop trading firm. Wrote Vanna's core programs on Solana and Stellar. https://www.linkedin.com/in/vatsal-h-salkiya

The founders met in 2023 through a friend from Koinfox, worked together for a few weeks, and started Vanna in November 2023. They split the risk: Opinder sets what collateral counts, at what leverage and when it is liquidated; Vatsal turns it into contracts and tries to break it. Team: 6 full-time including the founders (engineers in smart contracts, AI/ML, mobile and full-stack). Both founders work full-time on Vanna; we want New York as our operating hub.

History: Vanna was first written in Solidity on EVM chains (Arbitrum, Base, Optimism), rebuilt on Stellar (Soroban, Rust) in 2025, and on Solana (Rust, Anchor) since August 2026, because Solana has every market our credit needs. Both chains now run in one app. We learned two things the slow way: we spent years being filed as "another perp exchange" when the value was the credit underneath, and a credit protocol should not take deposits before its risk has been checked by others, which is why we are still on testnet. Solana builds since August went through Stocklana, Colosseum's World's Fair (CertiK and Adevar Labs track prizes) and Clock In (2nd of 659 teams).

Funding: no equity or tokens sold; the two founders own 100%. Nine grants and prizes, over $230K: $145K Stellar Community Fund (SCF #38, 2025); $25K Google Cloud grant; $25K, 2nd place at Solana Mobile's Clock In hackathon (Nov 2026); $22K Draper University (July 2025); $10K CertiK Security Audit Track and $4K Adevar Labs pre-audit track at Colosseum's World's Fair (Oct 2026); about $2.5K from a Gitcoin Grants round (May 2025); 20K OP from Derive; $1K Certora audit grant.

## 13. What is not built or not proven yet
- **No external audit yet.** Internal security review only. External audits and an independent economic risk assessment are the main blockers before mainnet and the first use of incubator support.
- **The live liquidation path is unproven under stress.** No liquidations appear in the testnet's indexed history; the bot's scenarios pass in fork tests, and our stress numbers are simulations and backtests. A live crash drill on a mainnet fork comes before mainnet.
- **Many loans would liquidate at once.** In the worst hours since 2020, 34% to 74% of one kind of loan would have been liquidated in the same hour. At the planned launch caps that could need stablecoins worth about half of all loans in one hour. Direction caps and flash liquidation are planned, not built.
- **One admin key on testnet.** A multisig with a timelock is required before mainnet; our own internal audit of 15 Oct 2026 rates it High. That audit found 0 critical, 2 high, 3 medium issues and no way for an outsider to take funds; the stale-price high is fixed in the current source.
- **Existing positions cannot be brought in.** They must be opened again from the Vanna account, because the program has to control liquidation.
- **Testnet accounts are not users.** Many are our own stress-test accounts (section 4).
- **Options and prediction markets need Vanna's own capital on other chains** (Derive, Polygon). The reserve level and treasury limits are still being decided.
- **Stellar runs on public testnet, not a mainnet fork**, because we have not found a host for a Stellar fork node; some test assets there carry testnet names.
- **Prediction-market bets use the wallet balance.** They are not in the margin account or its health factor yet.
- **Status of every product is in 5.12.**
- **10x is the maximum, not the opening limit.** The app opens at about 4x; contract settings allow up to 5x.
- **Earlier mistake we corrected:** in October 2026 we publicly quoted testnet account counts and average leverage as if they were usage; an on-chain review showed they were inflated by our own scripted accounts, and we stopped quoting them that way.

### Security reviews and tests so far (all internal)
| Scope | Date | Result |
|---|---|---|
| Solana core, oracle, validator (6,846 lines) | 15 Oct 2026 | 0 critical, 2 high, 3 medium, 7 low. 239 of 239 tests passed that day. Later source fixes the borrow-limit medium and the stale-price high; the admin-key high stays open until a multisig |
| Basis vault program | 6 Oct 2026 | 2 high and 9 of 10 medium fixed; 1 medium open (Phoenix withdraw limits) |
| Multi-strategy basis vault and keeper bot | 16 Oct 2026 | No critical. Program 6 medium, 4 low; bot 3 high, 5 medium, 4 low, all bot findings fixed |
| Stellar credit layer (12 crates, 3,305 lines) | Nov 2026 | 3 high, 6 medium, 19 low. 2 high and 4 medium fixed; 1 high kept by design (full-debt liquidation, no write-off). 291 tests, 270,000 random operations, six fuzz targets, 93.5% line coverage. Submitted to Stellar's Audit Bank on 14 Nov 2026 |
| Load test, Stellar | 3 Nov 2026 | 500 simulated accounts: 499 created, 83% of steps succeeded, about 4.5 s a step |
| Full test of both chains, 24 Nov 2026 | 24 Nov 2026 | Solana scripts 10 of 11 pass (options matrix 22 of 24: the bot cancelled one buy-back); Stellar scenarios all pass; 10 app bugs found and fixed. Stress: 100 browsing users plus 32 wallets at once, 1 failed page request in 5,551; Solana 88 of 99 transactions, Stellar 40 of 41 (most Solana failures were correct refusals or fork limits) |
| Internal economic risk assessment (67 pages) | 2026 | Set collateral rules, leverage limits and solvency guardrails and led to a round of contract changes; its references are being re-checked before we share it. The measured results in section 18 stand on their own |
| Load test, Solana fork | 3 Nov 2026 | About 100% success to 10 at once, 78% at 20: the fork is the limit. Not ready for large public load |

## 14. Roadmap and the ask
Now: private testnet on Solana and Stellar for select accounts. Next: testnet points campaign with invites to the top 100 traders worldwide, then weekly invite waves, each testing the next release. Before mainnet: external audits, an independent economic risk review and a live crash drill. Then: a capped mainnet whose limits rise as the book proves itself.

From the Solana Incubator, in order: funding support for audits and the economic risk assessment; a Solana Labs engineering review of the account and CPI design and of liquidations under congestion; introductions to funds holding tokenized stocks and other real-world assets; liquidity providers for the launch pools.

## 15. The technology, layer by layer
*For technical diligence, human or AI.*

### 15.1 Core credit program (`vanna_credit_layer`, Solana)
- **What it is:** lending pools (USDC, USDT, SOL), margin accounts (one PDA per user), borrowing, health checks and liquidation.
- **How it works:** every external call goes through `margin_execute`: (1) `vanna_validator.review_call` checks the target program, the accounts, and that the call spends no more than it states; (2) the core CPIs into the venue, signed by the margin PDA; (3) `vanna_oracle.get_price` re-prices the whole account; (4) the transaction reverts if the account is unhealthy. Liquidation is open to anyone below health 1.10.
- **Main technologies:** Rust, Anchor 1.1.2; tests in LiteSVM against mainnet program dumps; runs on a Surfpool mainnet fork.
- **Scale:** 843 accounts, 6,758 transactions on the fork (24 Nov 2026); 625 test functions in the current branch.
- **Proprietary vs open:** written by Vanna. Repository private today (available to reviewers on request); program IDs: core `H37YVBG3eGtz89ofd7iDLc2PJgn12778392XeU2QJcGC`, oracle `FXY5DRfekMUTbUp4uyCFpCZmCccrp6kPq3hTM4GRihnc`, validator `6fND3vhtstp486iE6rsSNVUox3kcjNNRsSLAN7ZPs7th` (testnet fork deployments).

### 15.2 Oracle (`vanna_oracle`)
- **What it is:** values every holding: tokens, vault shares, lending receipts, open Phoenix perps, options legs.
- **How it works:** Kamino Scope prices with Pyth as fallback; venue-specific valuation modules per integration.
- **Proprietary vs open:** written by Vanna; private repo (on request). Uses open oracles (Scope, Pyth).

### 15.3 Validator (`vanna_validator`)
- **What it is:** the allowlist: which programs and instructions a margin account may call and how much each call may spend. Adding a venue means adding a validator and an oracle module; the core does not change.
- **Proprietary vs open:** written by Vanna; private repo (on request).

### 15.4 Options program (`vanna_options`) and RFQ bot
- **What it is:** a standalone options venue on Solana: users submit intents (buy, sell, write, cover) with USDC in escrow; an operator hedges each on Derive by RFQ and fills it; expired series settle on Pyth. Any wallet or protocol PDA can hold a position; Vanna integrates it like any other venue. Program ID `9QcaqHmBZ86wsu1PFGYUSJEvdWjWq2UJTscvA5i3py9V` (testnet).
- **Off-chain:** TypeScript bot for RFQ, fills, marking and settlement; treasury moves over Circle CCTP V2 between Solana and Ethereum (Derive). DRY_RUN against Derive testnet today.
- **Proprietary vs open:** written by Vanna; private repo (on request).

### 15.5 Vaults and prediction markets
- **Basis vaults (unlisted since the November upgrade):** delta-neutral vaults (SOL, ETH, BTC, TSLA, META), each holding an asset and an equal short on Phoenix to earn funding. Written by Vanna; private repo (on request).
- **Prediction earn vault:** lets holders of World YES/NO tokens earn Vanna's USDC lending yield while keeping their position. Written by Vanna; private repo (on request).

### 15.6 Liquidation
- **What it is:** a bot that repays up to half of an unhealthy account's debt per call, or all of it when the account is close to insolvent, closing Phoenix positions first (liquidator bonus 5%; 7% for xStocks is still set on the testnet, the current code caps it at 5%). It does not close options yet. Private repo (on request).

### 15.7 AI layer
- **Vanna Copilot:** Gemini on Google Vertex AI; intent to plan to checked execution with guardrails (health floor, 5-minute plan validity, live re-check, user approval and signature). Proprietary.
- **Vanna MCP:** MCP server on Google Cloud Run; reads positions, prepares transactions; never signs. Written by Vanna; private repo (on request).
- **Risk Guardian, Credit Underwriter:** in development; private.

### 15.8 Apps
- **Web app:** Next.js. Written by Vanna; private repo (on request).
- **Seeker app:** React Native (Expo), Mobile Wallet Adapter. Written by Vanna; private repo (on request).

### 15.9 Stellar
- Soroban (Rust) protocol: one credit layer, one margin account contract per trader, a reserve per asset, an oracle (two Reflector feeds) and a validator per venue (Blend, Soroswap, Aquarius). Its health factor is assets divided by debt, without per-asset weights; the admin can set the borrow and liquidation limits between 1.1 and 1.2. Both start at 1.2 in the mainnet build; on testnet both are 1.1, so an account opened at the limit sits on the liquidation line. Launch assets XLM and USDC. Private repo (on request). 

### 15.10 Code access (24 Nov 2026)
All Vanna product code is private. Read access is given to named reviewers on request. By area: Solana core, oracle and validator; options program and RFQ bot; liquidation bots (Solana and Stellar); risk agents; Stellar (Soroban) protocol; basis vaults; prediction earn vault; MCP server; web app; Seeker app; indexers. Documentation is public: https://docs.vanna.finance

### 15.11 Security model
- Margin accounts are PDAs: no private key exists for them; only the Vanna program can sign, and only through `margin_execute` with validator and health checks.
- Borrowed funds can move only to allowlisted programs, and a call cannot spend more than it states.
- Admin keys: protocol admin on testnet is a single team key; a multisig and timelock are required before mainnet.
- Copilot and MCP never hold keys; the user's wallet signs every transaction.
- Not yet externally audited (section 13).

## 16. How to verify what this file says
- Waitlist count, live: https://vanna.finance/api/waitlist/v1/stats
- Testnet analytics: https://test.vanna.finance (access code on request), analytics page.
- Code and commit history: read access on request.
- Grants: Stellar Community Fund #38 results; Colosseum World's Fair track winners (CertiK, Adevar Labs); Solana Mobile Clock In results.
- Market figures: OFR Hedge Fund Monitor; DefiLlama.

**What is in the data room (view-only folder, on request from op@vanna.finance):** risk memo (PDF), risk model (spreadsheet, every row of section 18.2), backtest code and raw results, internal security reports (Solana core, basis vaults, Stellar), test and load reports, the deck, and read access to the code for named reviewers. Company documents (cap table, entity, finances, legal) are shared at diligence.

## 17. Frequently asked questions

### Product
1. **What is Vanna in one line?** Composable credit infrastructure for DeFi: one unified margin account whose credit works across lending, spot, perps, options and yield vaults, with prediction markets feeding its credit pools.
2. **Is the borrowed USDC synthetic?** No. It is real USDC, USDT or SOL lent from Vanna's credit pools.
3. **How can you lend more than the deposit?** The funds are held by an account only Vanna's program can sign for. They can go only to allowlisted venues, a call cannot spend more than it states, the whole account is re-priced after every action, and an action that leaves it below the borrow line reverts.
4. **Can a borrower withdraw the loan?** Not the leveraged part. A withdrawal is allowed only while what remains covers the debt at its loan-to-value (50% to 80% by asset), which is an ordinary overcollateralized loan. Everything beyond that works only inside connected venues.
5. **Why not just use a perp DEX's leverage?** That leverage exists only inside that venue. Vanna's credit can hold spot on one venue and a short on another, so a hedge is one position in one health factor.
6. **What does borrowing cost?** A borrow APR set by pool utilization, not a funding fee. Testnet USDC on 24 Nov 2026: 7.9% at 95% utilization. If the credit is used on perps, that venue's funding applies to the perp leg.
7. **Can I bring positions I already hold elsewhere (Derive, Kamino, Phoenix)?** Not today. You connect your wallet, but positions must be opened from the Vanna account, because the program has to be able to liquidate them.
8. **Does credit move across chains?** No. Solana and Stellar accounts are separate. Options are the exception in form: they are traded on Solana and filled on Derive through our options program.
9. **Which venues are integrated?** Solana testnet: Kamino, Jupiter, Titan, Phoenix, Perena, World and Derive options; Vanna basis vaults are built and unlisted. Stellar testnet: Blend, Soroswap, Aquarius. Next: Polymarket, then Monad and its venues. Hyperliquid and others can follow the Derive pattern once the liquidation path is safe.
10. **Do you need more venues, or is it enough to have each instrument?** Depth and risk tooling matter more than the count. We add a venue when it has the liquidity to liquidate into; each needs oracle and validator rules, not a new core.

### Prediction markets
11. **How does a bet earn yield while it is open?** YES and NO holders put their tokens in a pool. Matched pairs merge into $1 through the market's own program, and that dollar is lent in our USDC credit pool. The bet stays open; matched bets earn, and the surplus side earns less.
12. **Is that safe?** It does not depend on who wins: a YES and a NO redeem for $1 together at any odds, and the pool never uses an outcome price. It does carry the credit pool's own lending risk, and a withdrawal can wait if that pool is fully used.
13. **Is the loop self-reinforcing?** By design: more trader borrowing raises utilization and the yield, which should draw more bettors, who deepen the pool. It is early: $3,164 of the testnet's USDC pool came from it on 24 Nov 2026. The loop also runs the other way if borrowing falls.
14. **What if Polymarket pays yield itself?** The bet-side yield would be less special. Our yield comes from traders borrowing from our pools, which a betting venue does not have.

### Risk
15. **How is the health factor calculated?** 1.1 x the sum of each asset's value times its liquidation threshold, divided by debt. At 1.10 that weighted value equals the debt and the account can be liquidated. Weights: stablecoins 85%, SOL and LSTs 80%, xStocks 65%, receipts 60%.
16. **How much of my deposit can I lose before liquidation?** The more you borrow, the less. With SOL posted and the borrowed USDC held as cash: about 81% of the deposit at 2x, 62% at 3x, 44% at 4x, 34% at 4.5x. With stablecoins posted: 82% at 2x, 65% at 3x, 47% at 4x, 29% at 5x (18.1).
17. **How much leverage is possible?** Up to 10x. The app opens at about 4x: 4.3x against stablecoins, 3.9x against SOL and staking tokens, 3.2x against xStocks. Contract settings today allow 5x, 4.5x and 3.75x. Higher limits come per trader through the Credit Underwriter and for the most liquid collateral.
18. **Has the risk engine been backtested?** Yes, on 3.3 million SOL minute prices since August 2020 and 11 years of stock prices (18.2). No bad debt when liquidations land within a minute; directional loans lose about 0.07% per 30 days if they land an hour late.
19. **What about correlated risk?** It is the main constraint. In the worst hours since 2020, 34% to 74% of one kind of loan would have been liquidated together. At the planned launch caps that could need stablecoins worth about half of all loans in one hour. Direction caps and flash liquidation are planned, not built (18.3).
20. **How do you control collateral depeg?** Today: liquid assets only, per-asset thresholds, price freshness and TWAP checks, and stale collateral is not counted. Risk Guardian will cut collateral values and new leverage. Depegs are not in the backtest.
21. **What is the biggest risk?** Liquidations not landing fast enough when many accounts fail together.
22. **What happens to bad debt?** Solana: once an account has $1 or less left, the remaining debt is written off, first against uncollected protocol fees and then against the pool's lenders. A reserve funded from fees is designed, not built; there is no insurance fund today.
23. **Do you set leverage per user?** Today the limit is per asset. The Credit Underwriter will set it per trader from how they use credit, the way a card issuer sets a limit.
24. **Can a venue liquidate its own position first?** Yes. Phoenix can liquidate a perp. Vanna sees the value change and acts on the account.
25. **Who holds the admin key?** One team key on testnet. A multisig with a timelock is required before mainnet.

### Stage, market and company
26. **Are you audited?** No external audit yet. Internal reviews are listed in section 13. Stellar's Audit Bank has our submission of 14 Nov 2026.
27. **What has to happen before mainnet?** External audits, an independent economic risk review, a live crash drill, a multisig, and launch liquidity. Then a capped mainnet.
28. **What are the main blockers?** Audit and risk-review funding, and liquidity for the credit pools.
29. **What is the go-to-market?** Traders first (waitlist, founder audience, invite-only points campaign), prediction markets as a liquidity and user channel, then businesses offering our credit to their own customers.
30. **Who are the competitors?** Lending protocols and perp exchanges are complementary: they are where our credit is used. The closest in approach are Gearbox (lends above collateral, not across derivatives) and Project 0 (spans Solana lending markets); exchange portfolio margin is custodial. We have not found a live protocol that covers derivatives across venues. They are live with real volume; we are on testnet.
31. **How do you make money?** A share of borrow interest, part of liquidation bonuses, vault performance fees, routing and partner fees, and Copilot and MCP usage. Nothing is charged yet.
32. **How would an institution or issuer use Vanna?** It writes its own rule set (which holders qualify, how the asset is priced, the haircut, the leverage cap), gets its own debt ceiling on shared pools, and its customers borrow USDC against the assets they hold. The issuer commits redemption liquidity so liquidations clear one to one (5.8).
33. **Do you have real users?** No paying users, by design. Testnet accounts are invited testers plus our own stress-test accounts.
34. **Have you raised?** No equity or tokens sold. Nine grants and prizes, over $230K. In early conversations with investors.
35. **Is the code open?** Private. Read access for named reviewers on request.
36. **Can US persons use it?** Nothing is live with real funds. Eligibility by country for options, prediction markets and tokenized stocks will follow legal advice before mainnet.

### More questions investors and their agents ask
37. **Is this undercollateralized lending?** The loan can be larger than the deposit, but it is secured: the leveraged funds stay in the account and what they buy backs the loan. It is not credit on a promise.
38. **Can a trader buy something illiquid with the loan and leave lenders with it?** No. Funds go only to allowlisted venues and tokens, each with a price source and its own weight. There are no per-account concentration caps yet; they are part of the launch settings.
39. **Why would lenders supply?** Traders borrow at leverage, so utilization and supply yield can run higher than in overcollateralized markets, and the leveraged part cannot leave the account. Testnet USDC on 24 Nov 2026: 6.8% supply APR. The risk they take is bad debt, smart-contract failure and waiting for liquidity when a pool is fully used.
40. **What stops Gearbox, Kamino or Hyperliquid adding this?** Nothing in principle. Gearbox would rebuild its risk core around positions that are not tokens; lending markets would have to lend above collateral; a perp venue would have to become a lender to other venues. Our lead is the integrations, the risk engine and, in time, the underwriting record.
41. **If the code can be forked, what is the moat?** Not the code. The record of how accounts behave on credit, a history of staying solvent, and integrations inside other products.
42. **Why are you still on testnet after three years?** We rebuilt twice to reach chains with the markets our credit needs, and we will not hold deposits before external audits and an economic review. We also stopped two integrations where positions could not be priced safely.
43. **Why Solana, Stellar and Monad?** Solana has every market type and a program-owned account for each user. Stellar funded the first build and has deep links to issuers of real-world assets. Monad is next, as the home of the EVM version.
44. **Is there a token?** No. Revenue and a risk record come first.
45. **Can Copilot or MCP move my money?** No. They build and simulate transactions; your wallet signs. They refuse other wallets and unknown programs, and hold a 1.15 health floor on borrowing, withdrawals and swaps.
46. **What if the AI is wrong?** It never sets an amount: code does, from live data. The plan is shown with health before and after, expires in 5 minutes and is re-checked at every step, and the contract rejects anything unhealthy. It can still misread a request, so the user reviews the plan.
47. **Does Copilot trade options or act on its own later?** Options are placed from the options builder. It does not place stop, limit or scheduled orders.
48. **What happens if a connected venue fails?** The position there can lose value or be frozen; the account is re-priced and can be liquidated from its other assets. Venues are added one at a time; per-venue exposure caps are part of the launch settings and are not set on testnet.
49. **What happens if prices are stale or manipulated?** SOL, staking tokens and the main stablecoins use Kamino Scope with Pyth as fallback, with freshness, confidence and time-average checks. Some assets have one source (xStocks: Scope; JupUSD and the ETH and BTC perps: Pyth; Perena USD*: its net asset value, so a market depeg of USD* would not show). Collateral that fails a check counts as zero for new borrowing. On the testnet fork a keeper refreshes prices.
50. **Are Phoenix and Derive partners?** Phoenix is integrated and has agreed to promote the mainnet launch; Derive awarded us a grant and its order book fills our options. Neither has audited or endorsed our risk.
51. **Are tokenized stocks real shares?** It depends on the issuer: some are price exposure only, and several cannot be held by US persons. Vanna takes them as collateral with lower weights and does not issue them.
52. **Can Vanna be used without Copilot?** Yes. The app, the options builder and the Portfolio page do everything by hand.
53. **How many people work on it, and who owns it?** Six full-time including two founders, who own 100%. No equity or tokens have been sold.
54. **What can the admin key do today?** On testnet one team key can change limits, oracles, allowlists, fees and modes at once. A multisig and a timelock are required before mainnet.
55. **Who funds liquidations?** The liquidator's own wallet, holding the debt tokens; anyone can liquidate. A flash-liquidation path that sells the seized collateral in the same transaction is on the launch list.
56. **What about stocks when markets are closed?** Stock prices must be fresh; stale stock collateral counts as zero for new borrowing, and an account with more than 5% stale collateral cannot be liquidated until prices return. That is why stock weights are lower.
57. **Can an issuer freeze collateral?** Yes, for some tokens (stablecoins and tokenized stocks). Frozen tokens count as zero.
58. **How many assets can an account hold?** The Solana contract has 24 asset slots and 30 positions; the mainnet configuration is smaller so that a liquidation fits in one transaction.

## 18. Risk engine: rules, backtest and stress

### 18.1 How it works (measured from the deployed program)

Source: `vanna_credit_layer`, commit 624c6a6 (16 Nov 2026). Per-asset settings read from the fork's accounts on 24 Nov 2026.

- **Two lines, not one.** To borrow, withdraw or trade: sum(LTV x value) must exceed debt. To be liquidated: sum(liquidation threshold x value) is at or below debt. The app shows this as a health factor, with liquidation at 1.10.
- **Everything counts.** Tokens, lending receipts, vault shares, Phoenix perp equity and option legs are re-priced together after every action. An action that leaves the account below the borrow line reverts.
- **The leveraged part stays in the account.** Funds can only go to allowlisted programs, and a call cannot spend more than it states. Withdrawals must leave the account above the borrow line.
- **Not yet in the contract:** per-account concentration caps, and a reduce-only exemption (an account between the two lines can deposit or repay, but a partial close reverts unless it restores the borrow line).

| Collateral | LTV | Liquidation threshold | Liquidator bonus | Max leverage, borrowed USDC kept as USDC | Max leverage, all in the same asset |
|---|---|---|---|---|---|
| USDC, USDT, JupUSD | 80% | 85% | 5% | 5.00x | 5.00x |
| SOL, JitoSOL, JupSOL | 70% | 80% | 5% | 4.50x | 3.33x |
| NVDAx, TSLAx, AAPLx, GOOGLx | 55% | 65% | 7% (code now caps at 5%) | 3.75x | 2.22x |
| kUSDC, kSOL, USD* (receipts) | 50% | 60% | 5% | 3.50x | 2.00x |

**Up to 10x, opening at about 4x.** With the parameters above the contracts let an account draw at most 5x; the app's own safety buffer (health 1.15) makes that 4.3x, 3.9x and 3.2x. The formula reaches 10x at an LTV of about 90%, with no code change. At 10x an account is liquidated after losing roughly 10% of the deposit, so it is meant for hedged books, the most liquid collateral and traders with a record. Perps opened with that credit carry the venue's own leverage (up to 5x on SOL, ETH and BTC in the mainnet config), which counts through the perp account's equity.

**How much of the deposit can be lost before liquidation at 1.10.** It depends on leverage. Checked on 24 Nov 2026 against a live testnet account: $139.34 of SOL x 0.88 + $324.53 of USDC x 0.935, divided by $389.10 of debt, gives 1.095, the number the app shows.

| Share of the deposit lost at liquidation | 2x | 3x | 4x | Maximum at contract settings |
|---|---|---|---|---|
| Solana, stablecoins posted, borrowed USDC as cash | 82% | 65% | 47% | 29% (5x) |
| Solana, SOL posted, borrowed USDC as cash | 81% | 62% | 44% | 34% (4.5x) |
| Solana, xStocks posted, borrowed USDC as cash | 77% | 54% | above the limit | 37% (3.75x) |
| Stellar, limit 1.2 (mainnet build's default) | 80% | 60% | 40% | |
| Stellar, limit 1.1 (testnet setting since 18 Nov 2026) | 90% | 80% | 70% | 10% (10x) |

By strategy, the fall in the asset that causes liquidation:

| Strategy (full / 75% / 50% of max borrow) | Fall to liquidation | Fall to insolvency |
|---|---|---|
| SOL collateral, borrowed USDC held as cash | 34% / 51% / 67% | none while the cash stays in the account |
| SOL collateral, borrowed USDC in a yield vault | 30% / 47% / 65% | none unless the vault itself loses value |
| SOL collateral, borrowed USDC swapped into more SOL | 13% / 20% / 33% | 30% / 36% / 46% |
| xStock collateral, borrowed USDC held as cash | 37% / 52% / 68% | none while the cash stays in the account |
| xStock collateral, swapped into more of it | 15% / 26% / 42% | 45% / 52% / 62% |

**Liquidation.** Anyone can liquidate. A call repays up to 50% of the debt, or all of it when solvency is at or below 1 + bonus or the debt is $100 or less. The bonus can never exceed what the account has left, and an underwater account pays none. A call that would turn a solvent account insolvent is refused. The bot loops every 15 seconds and closes Phoenix positions before seizing. Stale collateral prices are excluded, and liquidation is refused if more than 5% of collateral value is stale.

**Rate curve (on chain).** 2.8% APR at 80% utilization, 3.4% at 90%, 7.9% at 95%, 112% at 100%. Reserve factor 10%. **Launch caps (mainnet config):** 4M USDC, 4M USDT and 24,000 SOL borrowable.

### 18.2 Backtest (measured on real prices)

Method: every 6 hours from 11 Aug 2020 to 23 Nov 2026 a new loan opens and is held 30 days (9,060 loans per row, 3.3M SOL minute candles). Interest is charged up front at 8% APR. A liquidation executes at the **lowest** price between crossing the line and crossing plus the delay. Results at 75% of maximum borrow:

| Strategy | Liquidated within 30 days | Bad debt, 1 min delay | 5 min | 60 min | 4 hours | Worst single loan, 4h |
|---|---|---|---|---|---|---|
| Cash credit | 6.4% | 0 | 0 | 0 | 0 | 0 |
| Yield carry | 7.7% | 0 | 0 | 0 | 0 | 0 |
| Directional long | 44.4% | 0 | 0.26 bps | 7.4 bps | 13.6 bps | 24% of the loan |
| Delta-neutral basis | 7.2% | 0 | 0 | 0.6 bps | 2.0 bps | 10% of the loan |

Bad debt is in basis points of everything lent in that row, per 30-day loan. In the basis row, Phoenix closed the short early in 2,089 of 9,060 loans (23%) when its margin was never topped up. All 60 combinations (50%, 75%, 100% of max borrow; five delays) are in the risk model, on request. At 100% of max borrow the directional row stays at 0 with a 1-minute delay and reaches 11.5 bps at 4 hours.

Stocks, daily bars since 2015 for NVDA, TSLA, AAPL and GOOGL, liquidating **one full trading day late at the worst print**: no bad debt in any of 16 rows. This uses the listed stock; token depeg and weekend token trading are not modelled.

Read this honestly: the model shows liquidation *speed* is what protects lenders. It does not show that liquidations will always land. Not modelled: liquidator inventory running out, price impact of our own liquidations, chain congestion beyond the fixed delay, oracle failure, LST or stablecoin depeg, smart-contract failure, options greeks.

### 18.3 Correlated risk (measured)

Loans of one kind fail together. Share of a steady 30-day book liquidated in the single worst hour since 2020, at 75% of max borrow: directional 74% (19 May 2021), yield carry 68% and cash credit 64% (11 May 2022), basis 34% (3 Jan 2024).

What that means: for the base mix in 18.4, about 53% of the book could need liquidating in one hour, if every slice had its worst hour at once. At the launch caps the liquidator would need stablecoins worth **about half of all outstanding loans in that hour**, or liquidations that sell the seized collateral in the same transaction. This is the constraint we will size caps around, and it is why launch is capped. Planned controls, not built: per-asset and net-direction open-interest caps, a flash-liquidation path, and Risk Guardian cutting new leverage when the book leans one way.

Instant shock on the real testnet book (776 accounts; SOL, LSTs and xStocks fall together; nobody is allowed to liquidate on the way down):

| Shock | Liquidatable accounts (of 385 borrowers) | Insolvent | Bad debt | % of debt |
|---|---|---|---|---|
| 0% (today) | 1 | 0 | $0 | 0 |
| -20% | 15 | 0 | $0 | 0 |
| -30% | 20 | 0 | $0 | 0 |
| -40% | 21 | 0 | $0 | 0 |
| -50% | 21 | 16 | $98 | 0.08% |
| -70% | 27 | 20 | $711 | 0.61% |
| -90% | 47 | 32 | $2,186 | 1.89% |

SOL had already fallen 31% (from $100.92 on 29 Oct to $69.60 on 24 Nov) before this test. The 16 insolvent accounts at -50% are small (14 near-identical ones of about $200 debt each). On 29 Oct the same -50% test on the dashboard showed $0. 67 accounts with venue positions are excluded, so perp and option accounts are not covered by this table.

### 18.4 Projected margin book by instrument (assumption, not data)

| Instrument type | Hedged mix | Base mix | Directional mix |
|---|---|---|---|
| Delta-neutral basis (spot + perp short) | 45% | 30% | 10% |
| Yield carry (lending, stable vaults) | 30% | 25% | 10% |
| Directional spot and perps | 5% | 20% | 50% |
| Options (modelled as directional) | 5% | 10% | 20% |
| xStock-backed credit | 10% | 10% | 5% |
| Cash credit and prediction markets | 5% | 5% | 5% |
| **Loans liquidated within 30 days** | 10% | 18% | 33% |
| **Expected bad debt per year (5-minute liquidation)** | 0.003% | 0.009% | 0.022% |
| **Share of book liquidated in the worst hour** | 46% | 53% | 65% |

Registered on the testnet today (24 Nov 2026): 24 assets, receipts included. The assets and pairs in the right-hand column of 5.1 are not in any number here.

There is no real usage behind these shares: testnet collateral today is 42% USDC, 34% SOL, 7% xStocks, 4% USDT, 4% JitoSOL, with perps and options under 4% of value. We will replace the assumption with measured shares from the points campaign.

## Changelog
- 24 Nov 2026 (fourth update): product section rewritten with every connected venue, asset, strategy, Copilot, MCP, leverage as a service and the vision; deposit-loss table verified against a live account; competition split into complementary venues and closest approaches; 22 questions added; every product and FAQ claim checked against the source code by a separate review.
- 24 Nov 2026 (third update): one file only; risk data and 36 FAQs moved in from the second file.
- 24 Nov 2026 (second update): market, audience and waitlist figures re-checked at source; internal audits, load tests and the prediction-market mechanism added.
- 24 Nov 2026: code is private (on request); testnet, waitlist, leverage and risk figures re-measured; backtest and correlated-liquidation risk added.
- 23 Nov 2026: first version, synced with deck v7.
