# Vanna: company.md

*Everything about Vanna in one file, for people and their AI agents. Each figure carries its date and source; scenarios are labelled as scenarios. Figures as of 24 Nov 2026 unless dated otherwise.*

- This file: https://github.com/vannafinance/company/blob/main/company.md
- Data room: https://github.com/vannafinance/company/tree/main/data-room
- Product (private testnet): https://test.vanna.finance
- Website: https://vanna.finance
- Documentation: https://docs.vanna.finance
- 1-minute founder video: https://youtu.be/UApnnZ1-FiI
- X: https://x.com/vannaprotocol
- Contact: op@vanna.finance
- Status: private testnet

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
- **Why now.** About $39B of real-world assets are tokenized on-chain (rwa.xyz, Nov 2026) and liquid staking tokens hold about $40B more (DefiLlama, 2026). Holders keep them for yield or exposure and today can borrow only a fraction against them, inside a few lending markets, or sell. More capital is also run by AI agents, which have almost no credit rails built for them.
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
| Stellar testnet accounts / collateral / borrowed | 39 / $94K / $22K (test funds) | 24 Nov 2026 |
| Waitlist sign-ups | 1,515 (opened 10 Oct 2026; ~450 in the first two days; 840 by 2 Nov) | 24 Nov 2026 |
| @vannaprotocol X followers | 727 (378 on 13 Oct) | 24 Nov 2026 |
| Grants and prizes | 9, over $230K (section 12) | 23 Nov 2026 |
| Mobile | Native Android app for Solana's Seeker phone, 2nd of 659 teams at Solana Mobile's Clock In hackathon; launching on the Solana dApp Store in the coming days | 24 Nov 2026 |
| Founder audience | 27,862 followers: LinkedIn 9,300, X 7,875, Facebook 5,124, YouTube 3,960, Instagram 1,603; plus 849 on Telegram | 24 to 25 Nov 2026 |

Testnet balances are test funds; accounts are invited testers plus accounts we created to stress-test the risk engine. Source: the analytics dashboard at test.vanna.finance.

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
| Delta-neutral (farm) | Vanna basis vaults (built): SOL, ETH, BTC, TSLA, META | Each vault holds the asset and an equal 1x short on Phoenix to earn funding |
| Liquidity (farm) | Aquarius and Soroswap pools on Stellar | Provide XLM/USDC liquidity |
| Prediction markets | World; Polymarket next | Bet without selling collateral; separately, earn lending yield on long-dated bets (5.6) |

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

The right-hand column is the release scheduled for the days after this file was written; every risk figure in section 18 covers the middle column only. Each added asset gets its own limits: for example EURC moves with the euro, so it is not treated as a dollar.

### 5.2 Leverage and cost
- **Up to 10x.** The app opens at about 4x and the limit depends on the collateral: 4.3x against stablecoins, 3.9x against SOL and its staking tokens, 3.2x against xStocks (borrowed USDC kept as USDC, with the app's safety buffer at health 1.15). The contracts allow 5x, 4.5x and 3.75x at today's settings. Limits rise per trader through the Credit Underwriter (5.7) and per asset as liquidity allows; 10x is set by raising an asset's LTV to about 90%, which the program supports without a code change.
- Perps opened with the credit carry the venue's own leverage on top, inside the same health factor.
- **Cost:** a borrow APR set by pool utilization, not a perp funding fee. Testnet USDC pool on 24 Nov 2026: 95% utilization, 7.9% borrow APR, 6.8% supply APR. If the credit is used on perps, that venue's funding applies to the perp position, which is what makes funding strategies possible.

### 5.3 The unified health factor
One number for the whole account: 1.1 x the sum of each asset's value times its liquidation threshold, divided by debt. Collateral, borrowed cash, lending receipts, vault shares, perp equity and option legs are re-priced together after every action. Two lines use that: the liquidation line counts everything; the borrow line is stricter (options add nothing to borrowing power, an open perp counts as its collateral less the margin it uses). An action that would leave the account below its borrow line reverts on-chain. At 1.10 or below the account can be liquidated.

Why that matters: on separate venues each leg is margined alone, so a hedge can be liquidated leg by leg. In one account a $300 loss on spot and a $300 gain on the short that hedges it cancel, and the trader's other collateral stands behind both. Each venue keeps its own margin too, so a hedge leg is kept funded by the trader, Copilot or a vault.

### 5.4 Strategies traders can build
Each row uses the same account and the same health factor.

| Strategy | Legs | What it earns or protects |
|---|---|---|
| Leveraged long | Post JitoSOL, borrow USDC, swap into SOL | More SOL exposure, staking yield on the deposit |
| Leveraged directional perp | Post xStocks, borrow USDC, long or short BTC, ETH, SOL, TSLA or META on Phoenix | A view, without selling the stocks |
| Delta-neutral basis | Borrow USDC, buy SOL on Jupiter or Titan, short the same size on Phoenix | Funding, with price moves cancelling |
| Basis without managing it | Deposit borrowed USDC into a Vanna basis vault | Funding; the vault runs the hedge |
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
Solana traders get Derive's options liquidity from the same account. A trader pays USDC into Vanna's options program escrow on Solana; Vanna's bot hedges each order 1:1 on Derive and fills it on-chain at Derive's price plus or minus Vanna's $0.20 per contract; expired series settle on a Pyth price. Traders can buy or write calls and puts. Options count in the health factor, valued conservatively. On testnet, orders fill on the Solana fork and the hedge runs against Derive's testnet book.
- **Easy:** "What do you expect for ETH?" Rise, Fall, Big move, Protect or Earn. Vanna picks the best payoff for the budget and shows the most that can be lost.
- **Intermediate:** 27 named strategies in six groups (bullish, bearish, neutral, volatile, hedge, income), ranked by yield, lowest risk, most protection or lowest cost, each with its health factor before and after.
- **Pro:** the full chain, book, Greeks and a leg builder.
- Multi-leg books can include a Phoenix perp leg. The whole book is checked before anything is sent (funds, borrow line, slots); the perp leg is placed only after every option leg has filled. Written options are fully secured.

Treasury moves between Solana and Derive over Circle's CCTP, with a reserve kept on Solana so withdrawals and liquidations can be paid at once.

### 5.6 Prediction markets: two separate features
**A. Trade them with credit.** The same idea as every other market: borrow against collateral you already hold (JitoSOL, a tokenized stock) and use the USDC on prediction markets without selling anything. World is integrated on the Solana testnet, where bets use the wallet balance; funding bets from the margin account comes next. Polymarket follows the Derive design: the trader bets from Vanna, and Vanna's bot places the bet on Polygon with Vanna's own liquidity.

**B. Automated liquidity provisioning for our credit pools, from long-dated bets.** A bet can be locked for months and earns nothing meanwhile. A holder of YES or NO tokens puts them in Vanna's pool; the pool matches YES with NO, merges each pair into $1 through the market's own program, and lends that dollar in the USDC credit pool. The bet stays open and matched bets earn. The pool is market neutral: a YES and a NO redeem for $1 together at any odds, it never uses an outcome price, and each market's pool is isolated.

Why B matters: people who would never supply a lending pool bring liquidity to it. More trader borrowing lifts the yield, which draws more bettors, who deepen the pool. Running on testnet: 79 pools, with $3,164 of merged bets lent on 24 Nov 2026.

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
A native Android app for Solana's Seeker phone (React Native, Mobile Wallet Adapter): the same account and health factor, 2nd of 659 teams at Solana Mobile's Clock In hackathon. It launches on the Solana dApp Store in the coming days.

### 5.12 What runs today
On private testnet: the unified margin account, credit pools, oracle and validator, spot, Phoenix perps, Derive options, Kamino, Perena, World, the prediction earn pool, liquidation open to anyone (with our own bot), the risk dashboard, Vanna Copilot, Vanna MCP and the web app. Then: the assets in 5.1, Polymarket, Risk Guardian, Credit Underwriter, the business API with programmable credit rules, and credit APIs for institutions.

## 6. Why we win
- **Leverage belongs to the account, not the venue.** Lending markets lend less than you deposit; perp venues margin only inside themselves; Vanna's credit follows the trader into every venue type.
- **We are complementary to the venues.** Lending markets, perp exchanges, options and prediction markets are where our credit goes to work. Each integration makes the credit more useful and gives the venue borrowed volume.
- **Derivatives are in the risk model.** Most credit protocols can only hold positions that are already tokens. Vanna prices open perps and option legs, and its bot closes perps before seizing anything else, which is what makes a hedge count as a hedge.
- **The engine is reusable.** The same pools, risk engine and liquidation serve our app, Copilot, MCP and every business that plugs in. Adding a venue means adding oracle and validator rules; the core program does not change.
- **The record compounds.** Code can be forked. An underwriting record of how accounts behave on credit, solvency through drawdowns, and integrations inside other products cannot.
- **The team fits the risk.** Credit protocols fail on security and risk design. Our CTO is an Immunefi All-Star; both founders are traders.

## 7. Customers, in order
1. **Active on-chain traders** who already run strategies with more than one leg: a hedge, a basis trade, a staking loop. They feel the problem daily, because each venue holds its own margin and liquidates its own leg. Invited testers, including hedge-fund traders, have used the private testnets on Stellar since June 2026 and on Solana since September 2026.
2. **Traders and funds with their own agents.** Their product is Vanna MCP: the agent posts collateral, borrows and trades inside the account's credit rules.
3. **Businesses that already own users** and want to offer leverage without building it: wallets, exchanges, prediction markets, brokerages, fintech apps and issuers of tokenized assets.
4. **Institutions**: funds, desks and banks that want prime-brokerage-style credit across on-chain venues.

Traders come first because businesses and lenders want to see the engine hold through real volatility, and because every trader account adds to the underwriting record that makes the business offer better. Vanna is pre-revenue: real deposits open on mainnet, after external audits and an independent economic review.

## 8. Go-to-market
Built to be capital-efficient: product, distribution we already have, and scarcity. Paid growth is a later lever, not the plan.

**1. The Vanna Credit Monopoly campaign (Season 0, invite-only).** A nine-week trading game on the testnet, opening at the end of November 2026, on Solana and Stellar. Everyone collects the same test bankroll each week and decides what to build with it: borrow, hedge, trade, lend, farm, predict. Points are shared out every Friday, with ranks, badges, missions and a leaderboard.
- **The first 100:** 60 proven traders and 40 voices of the trading world, picked worldwide and invited by name. Trader-creators from the founder's own network take some of these seats.
- **Growth by scarcity:** each founding trader gets a handful of invites, and after that only active traders earn a few more each week. Vanna adds its own picks weekly: skilled traders, creators and their communities, and the waitlist. Early traders have the most to gain.
- **Earned access:** Vanna MCP and a limited number of Copilot seats unlock as the season goes on.
- **It rewards skill with credit, not raw volume.** Scoring is private, and linked accounts are folded together.
- **Capacity rises in steps** (2,500, then 5,000, then 10,000), each after its own stress test. Testers are also rewarded for accepted bug reports.
- **What it gives us:** strategy and health data for setting limits, retention by weekly cohort, proof that traders use credit across more than one market, and a community before mainnet. Season 0 points carry into the mainnet points programme; no token is promised.

**2. The founder's own distribution.** 27K+ followers across LinkedIn, X, Facebook, YouTube and Instagram, plus a Telegram channel: traders who already follow the strategy content (CutDNoise). Vanna is explained inside it.

**3. Trading creators and communities.** The founder knows many trading creators and influencers personally, with communities of 100K to 500K each. Some join as founding traders now and bring their communities through invites; the wider network is held for the mainnet launch. 10+ trading communities plan AMAs.

**4. Partners.** Phoenix, Titan, Soroswap, Superteam India and Canada, and the Solana and Stellar ecosystem teams have agreed to promote the mainnet launch. A venue gains volume from Vanna credit, so promoting it serves them too.

**5. Seeker.** The Android app launches on the Solana dApp Store in the coming days, in front of 150,000+ Seeker users. As a Clock In winner Vanna gets featured placement in the dApp Store and co-marketing and launch support from Solana Mobile (solanamobile.com/blog/clock-in-the-solana-mobile-hackathon).

**6. Prediction markets.** Bettors who hold positions for months arrive for yield on money that was earning nothing, bring liquidity to the pools, and meet the rest of the product (5.6).

**7. Agents.** Vanna MCP is found where agent builders already look: in Claude, Cursor and Codex, through listings, docs and working examples.

**What this sets up: businesses.** Traders prove the engine; the engine is then sold once and distributed many times. Each wallet, exchange or issuer that embeds Vanna credit brings its own users to the same pools, so after mainnet growth comes from partners' distribution rather than from our own spending (5.8).

## 9. Business model and pricing
- Borrowers pay interest; lenders earn most of it and Vanna keeps a share. Our plan is about 15% of borrow interest, near Aave and Kamino's reserve factors.
- Plus: 20% of the liquidation bonus (bonus 5%), a performance fee on delta-neutral vaults (plan: 10%), routing fees on trades made with the credit, platform fees from businesses, and Copilot and MCP fees.
- Scenario, not a forecast: at about a 6% average borrow rate, $1B of loans earns about $18M a year and $5B about $80M. The larger figure includes routing, business and agent revenue on terms to be set with partners. $1B is about 4% of today's DeFi lending.

## 10. Competition (live features, as of 23 Nov 2026)

### 10.1 The short answer
Most of DeFi is complementary to us: lending markets, perp exchanges, options and prediction markets are where our credit goes to work. The teams closest in approach are Gearbox and Project 0 on-chain, and exchange portfolio margin off-chain. We have not found a live protocol that does both halves at once: lend more than the deposit, and keep derivatives across venues in one health factor.

### 10.2 Who does what
| | Lends more than you deposit | Credit usable across other protocols' venues | Derivatives in one health factor | Non-custodial |
|---|---|---|---|---|
| Aave, Morpho, Kamino (complementary) | No | No | No | Yes |
| Drift, Hyperliquid (complementary) | Partly (within their own venue) | No | Yes | Yes |
| Gearbox (EVM) | Yes | Partly (lending and spot venues) | No | Yes |
| Aave V4 | No | Partly (spokes within Aave) | No | Yes |
| Project 0 (Solana) | No | Partly (Solana lending markets, not perps) | No | Yes |
| Exchange portfolio margin (Binance, Deribit, Coinbase Prime) | Yes | No | Yes | No |
| Vanna | Yes, on testnet | Yes, on testnet | Yes, on testnet | Yes |

| | What they do well | Where their credit stops | How Vanna relates |
|---|---|---|---|
| Aave, Morpho, Kamino | Deep, proven lending liquidity | Less than you deposit; loops lever one asset pair inside one protocol | Complementary: a place borrowed funds earn, and a source of demand for both |
| Hyperliquid, Drift, Phoenix | Fast perps, cross-margin inside the venue | Leverage is synthetic and stays on that venue | Complementary: Vanna brings them margin and hedged volume |
| Twyne | Frees unused borrowing power inside a lending market | The credit stays in that lending market | Complementary: a Twyne borrower could use Vanna to take credit further |
| Gearbox | Credit accounts that lend above collateral over tokenized positions | Perps, options and prediction markets are not in its risk model. On 16 Nov 2026 it announced leverage on tokenized real-world assets through lending markets | Closest on the credit side; its move confirms the demand |
| Project 0 | One margin view across Solana lending markets | Lending markets only, perps not yet | Closest on Solana |
| Aave V4 | Others can set credit rules on shared liquidity | Inside Aave's spokes; lending positions only | Proves programmable credit works |
| Coinbase Prime, Binance, Deribit | Whole-book margin for professionals | Only assets in their custody | Proves the need: unified cross margin launched at Coinbase Prime in March 2026 |

### 10.3 What we understand that others don't
1. **Leverage should belong to the account, not the venue.** Everyone else starts from a venue or a market and extends credit inside it. We start from the account and let credit follow it.
2. **The hard part is not lending, it is seeing and closing derivatives.** Once positions are open perps and option legs, the risk engine must price them after every action and be able to unwind them. That is why credit protocols stayed with tokenized positions, and it is the part we built.
3. **Hedges are the real customer.** More than half of hedge-fund borrowing goes to funds built on hedged trades (OFR, Q2 2026). On separate venues a hedge is liquidated leg by leg; in one account it is one position. Credit plus hedging is what brings professional size on-chain.
4. **The bigger customer already owns the users.** Wallets, exchanges and issuers would rather plug in than build lending, liquidation and risk: Phantom earned $20M+ routing perp trades to Hyperliquid; Coinbase originated $2.3B+ in loans on Morpho.
5. **Lenders don't have to be only LPs.** Money locked in long-dated bets can fund the pools (5.6).
6. **Credit should learn.** A fixed leverage cap treats every trader the same. The Credit Underwriter sets limits from behaviour, and agents get a credit history for the first time.

### 10.4 Why hasn't it been done, and why can't they just add it?
- **Earlier attempts failed on risk, not demand.** Mango Markets lost about $110M in 2022 to manipulated collateral. DeltaPrime, which ran cross-market credit accounts, was exploited twice in 2024, through a leaked admin key and an unvalidated external call. Our answer is structural: one entry point for every external call, allowlisted venues, the whole account re-priced after every action, oracle checks, and a CTO whose career is finding where such systems break. We walked away from two ecosystems where we could not price positions safely.
- **Each team is committed to its slice.** Gearbox would have to rebuild its risk core around positions that are not tokens. Lending markets would have to lend above collateral. A perp venue would have to become a lender to other venues, including its rivals. Exchanges would have to give up custody.
- **Nothing is impossible to copy.** Our lead is the integrations and the risk engine; what compounds is below.

### 10.5 The moat
1. **The underwriting record.** Every account builds a credit history with us: leverage taken, markets used, how it behaved near the line, repayment. Each loan improves the limits. A fork gets the code and none of the record, and a trader who has earned a higher limit has a reason to stay. For agents it is their only credit history.
2. **Where we sit.** We are a customer of every venue, not a rival, so each integration helps both sides. When a business embeds our credit, it becomes part of that product.
3. **Trust.** Lenders go where the engine has held through a drawdown. That record compounds and does not transfer.

### 10.6 Common questions
- **"Isn't Gearbox already doing this?"** It lends above collateral, over positions a venue has already tokenized. A perp or an option never enters its risk model; its liquidation sells tokens, ours also closes positions at venues.
- **"Hyperliquid has unified margin. Why not use that?"** It is excellent inside Hyperliquid. The margin cannot leave it, so it cannot back an option on Derive, a lending position on Kamino or a hedge elsewhere.
- **"Kamino loops already give leverage."** One asset pair, inside one protocol, below the value of the deposit. No derivatives, no hedge across venues.
- **"What if Coinbase or Binance does it?"** They already do, for assets they hold. The on-chain market is everyone who will not or cannot move into custody, and every business that wants the feature inside its own product.
- **"What stops Phoenix or Derive from adding credit?"** They could lend for their own market. Their traders would still be unable to use it anywhere else, which is the product.

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

**Opinder Preet Singh, Co-founder and CEO**, the technical product founder (Toronto). Three-time founder with one exit; 14 years building tech products, the last ten in crypto. Led ETHLend's (now Aave) go-to-market and fundraising in India in 2017. Cofounded Koinfox, a multi-exchange trading terminal that grew to 100K+ traders, became Southeast Asia's first Binance Broker Partner and was acquired in 2020. Has traded crypto since 2016 and runs AI trading agents and quant strategies across exchanges. Certified in zero-knowledge cryptography. At Vanna, leads product and risk design: market research, product strategy and positioning, user journeys and UX, and the risk parameters (which collateral is accepted, leverage limits, liquidation thresholds), and writes the specs the engineers build from. https://www.linkedin.com/in/opinderpreet

In the ecosystem: has backed 50+ early crypto startups since 2016; has trained 10,000+ developers, students and professionals, from ETHLend's developer workshops to programmes at the IITs and ICAI; judged ETHGlobal Delhi (2025) and ETHDenver (2026); mentors early-stage teams; runs CutDNoise, a trading-education channel (27K+ followers across channels). Built ShieldLend, a private-lending prototype where borrowers prove their collateral with zero-knowledge proofs, and led product and architecture on ZTips, which won RISC Zero's integrations prize at ZK Hack Montreal (2024).

**Vatsal Salkiya, Co-founder and CTO**, the lead smart-contract engineer (Ahmedabad). Immunefi All-Star security researcher with 27 vulnerability reports in live DeFi protocols, 6 of them critical, and 30+ smart-contract audits with firms including Cantina, Halborn, Pashov and Oak Security. Nearly two years building on-chain credit at Spectral; derivatives and delta-neutral vaults at Polynomial; delta-neutral options quant at a prop trading firm. Wrote Vanna's core programs on Solana and Stellar, including the unified margin account, the oracle and the liquidation engine, and led the internal security review. https://www.linkedin.com/in/vatsal-h-salkiya

The founders met in 2023 through a friend from Koinfox, worked together for a few weeks, and started Vanna in November 2023. They split the risk: Opinder sets what collateral counts, at what leverage and when it is liquidated; Vatsal turns it into contracts and tries to break it. Team: 6 full-time including the founders (engineers in smart contracts, AI/ML, mobile and full-stack). Both founders work full-time on Vanna; we want New York as our operating hub.

History: Vanna was first written in Solidity on EVM chains (Arbitrum, Base, Optimism), rebuilt on Stellar (Soroban, Rust) in 2025, and on Solana (Rust, Anchor) since August 2026, because Solana has every market our credit needs. Both chains now run in one app. We learned two things the slow way: we spent years being filed as "another perp exchange" when the value was the credit underneath, and a credit protocol should take deposits only after its risk has been checked by others. Solana builds since August went through Stocklana, Colosseum's World's Fair (CertiK and Adevar Labs track prizes) and Clock In (2nd of 659 teams).

Funding: no equity or tokens sold; the two founders own 100%. Nine grants and prizes, over $230K: $145K Stellar Community Fund (SCF #38, 2025); $25K Google Cloud grant; $25K, 2nd place at Solana Mobile's Clock In hackathon (Nov 2026); $22K Draper University (July 2025); $10K CertiK Security Audit Track and $4K Adevar Labs pre-audit track at Colosseum's World's Fair (Oct 2026); about $2.5K from a Gitcoin Grants round (May 2025); a 20K OP grant awarded by Derive; $1K Certora audit grant.

## 13. Security reviews, economic risk work and tests
Security and risk work is led in-house by an Immunefi All-Star CTO and runs before any outside audit. External audits and an independent economic review come before mainnet.

### 13.1 Security reviews
| Scope | Date | Result |
|---|---|---|
| Stellar protocol V1 (Soroban) | Jul 2026, fixes checked Oct 2026 | 27 findings. All 6 critical and all 8 high are fixed; 21 of 27 fully fixed, 5 partly, 1 rounding difference of negligible size open |
| Solana core, oracle, validator (6,846 lines) | 15 Oct 2026 | 0 critical, 2 high, 3 medium, 7 low; no way found for an outsider to take funds. 239 of 239 tests passed that day. The stale-price high is fixed in source; the admin high closes with the mainnet multisig |
| Basis vault program | 6 Oct 2026 | 2 high and 9 of 10 medium fixed |
| Multi-strategy basis vault and keeper bot | 16 Oct 2026 | No critical. All bot findings fixed |
| Stellar credit layer, new build (12 crates, 3,305 lines) | Nov 2026 | 3 high (2 fixed, 1 a design choice), 6 medium (4 fixed), 19 low. 291 tests, 270,000 random operations, six fuzz targets, 93.5% line coverage. Submitted to Stellar's Audit Bank on 14 Nov 2026 |

Won on security: CertiK's Security Audit Track ($10K, 10 winners of 177) and Adevar Labs' pre-audit track ($4K, 6 of 112) at Colosseum's World's Fair (Oct 2026); a $1K audit grant from Certora.

### 13.2 Economic risk assessment (67 pages)
Written by the founders on the July 2026 Stellar contracts (v1.1, October 2026). It models interest-rate and carry risk, leverage, liquidation, bank runs, contagion, oracle lag, incentives and governance, with correlated-GARCH price paths, flash-crash jumps and Monte Carlo tail estimates. Its simulated figures are illustrative (not calibrated to live market data). Its central result: the stress tail is decided by whether liquidation executes promptly, not by market volatility. What it asked for, and what the contracts do now:

| The assessment asked for | In the contracts now |
|---|---|
| Collateral factors per asset | Solana: every asset has its own LTV and liquidation threshold (18.1) |
| Reward for liquidators | Solana: 5% bonus, never more than the account has left |
| Partial liquidation | Solana: half the debt per call, or all of it when the account is close to insolvent |
| A reserve factor on interest | Solana: 10% on the testnet pools |
| Bounded interest-rate settings | Solana: rate coefficients capped. Stellar: no setting above a 1,000% annual rate |
| Time-averaged, staleness-checked prices | Solana: freshness, confidence and time-average checks. Stellar: two Reflector feeds with staleness and jump checks |
| Two-step admin transfer, then multisig and timelock | Two-step transfer in place; multisig and timelock for mainnet |
| Continuous monitoring | Live risk dashboard: utilization, health-factor distribution, accounts at risk, bad debt, price shocks |

### 13.3 Tests
| Test | Date | Result |
|---|---|---|
| Both chains end to end | 24 Nov 2026 | Solana: 10 of 11 scripts; options matrix 22 of 24. Stellar: every scenario passes, 58 of 58 in the newest |
| Stress, both chains at once | 24 Nov 2026 | 100 browsing users and 32 wallets transacting: 1 failed page request in 5,551; Stellar 40 of 41 transactions; Solana 88 of 99, where 9 of the 11 others were correct refusals |
| Load, Stellar | 3 Nov 2026 | 500 simulated accounts, 499 created |
| Market shock on the live testnet book | 24 Nov 2026 | $0 bad debt at an instant -40%, $98 (0.08% of debt) at -50%, with nobody allowed to liquidate on the way down |
| Backtest on real prices | 24 Nov 2026 | Section 18.2 |

## 14. Roadmap
1. **Now:** private testnet on Solana and Stellar; new collateral and markets; the Seeker app on the Solana dApp Store.
2. **Next:** the Vanna Credit Monopoly campaign, first 100 traders and weekly waves; Polymarket; Risk Guardian and Credit Underwriter on testnet.
3. **Before mainnet:** external audits, an independent economic risk review, a live crash drill, a multisig with timelock, launch liquidity.
4. **Mainnet:** a capped launch whose limits rise as the book proves itself; the first businesses on the API.
5. **After:** Monad as the home of the EVM version; credit APIs for institutions; more venues and chains.

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
- **Off-chain:** TypeScript bot for RFQ, fills, marking and settlement; treasury moves over Circle CCTP V2 between Solana and Ethereum (Derive).
- **Proprietary vs open:** written by Vanna; private repo (on request).

### 15.5 Vaults and prediction markets
- **Basis vaults:** delta-neutral vaults (SOL, ETH, BTC, TSLA, META), each holding an asset and an equal short on Phoenix to earn funding. Written by Vanna; private repo (on request).
- **Prediction earn vault:** lets holders of World YES/NO tokens earn Vanna's USDC lending yield while keeping their position. Written by Vanna; private repo (on request).

### 15.6 Liquidation
- **What it is:** a bot that repays up to half of an unhealthy account's debt per call, or all of it when the account is close to insolvent, closing Phoenix positions first. Anyone can liquidate; the liquidator earns a 5% bonus. Private repo (on request).

### 15.7 AI layer
- **Vanna Copilot:** Gemini on Google Vertex AI; intent to plan to checked execution with guardrails (health floor, 5-minute plan validity, live re-check, user approval and signature). Proprietary.
- **Vanna MCP:** MCP server on Google Cloud Run; reads positions, prepares transactions; never signs. Written by Vanna; private repo (on request).
- **Risk Guardian, Credit Underwriter:** risk agents that act only inside on-chain bounds; private.

### 15.8 Apps
- **Web app:** Next.js. Written by Vanna; private repo (on request).
- **Seeker app:** React Native (Expo), Mobile Wallet Adapter. Written by Vanna; private repo (on request).

### 15.9 Stellar
- Soroban (Rust) protocol: one credit layer, one margin account contract per trader, a reserve per asset, an oracle (two Reflector feeds) and a validator per venue (Blend, Soroswap, Aquarius). Its health factor is assets divided by debt, without per-asset weights; the admin can set the borrow and liquidation limits between 1.1 and 1.2. The mainnet build starts both at 1.2. Launch assets XLM and USDC. Private repo (on request). 

### 15.10 Code access (24 Nov 2026)
All Vanna product code is private. Read access is given to named reviewers on request. By area: Solana core, oracle and validator; options program and RFQ bot; liquidation bots (Solana and Stellar); risk agents; Stellar (Soroban) protocol; basis vaults; prediction earn vault; MCP server; web app; Seeker app; indexers. Documentation is public: https://docs.vanna.finance

### 15.11 Security model
- Margin accounts are PDAs: no private key exists for them; only the Vanna program can sign, and only through `margin_execute` with validator and health checks.
- Borrowed funds can move only to allowlisted programs, and a call cannot spend more than it states.
- Admin transfer is two-step; a multisig with timelock holds it on mainnet.
- Copilot and MCP never hold keys; the user's wallet signs every transaction.
- Reviews and tests: section 13.

## 16. Data room and how to verify this file
**Data room (open):** https://github.com/vannafinance/company/tree/main/data-room
| File | What it holds |
|---|---|
| RISK_MEMO.md | The risk engine in plain words, the backtest, correlated risk, the projected book, and what the model covers |
| Vanna_Risk_Model.xlsx | Every result, and assumptions you can change |
| sol_backtest.csv, xstock_backtest.csv, distance_table.csv, testnet_book_stress.csv | Raw results |
| backtest.py, book_stress.py | The code that produced them |

Code access, full audit reports and company documents (entity, cap table, finances, legal) are shared directly with named reviewers: op@vanna.finance.

**Check it yourself**
- Waitlist count, live: https://vanna.finance/api/waitlist/v1/stats
- Testnet analytics: https://test.vanna.finance, analytics page
- Grants: Stellar Community Fund #38 results; Colosseum World's Fair track winners (CertiK, Adevar Labs); Solana Mobile Clock In results
- Market figures: OFR Hedge Fund Monitor; DefiLlama; rwa.xyz

## 17. Frequently asked questions

### Product
1. **What is Vanna in one line?** Composable credit infrastructure for DeFi: one unified margin account whose credit works across lending, spot, perps, options and yield vaults, with prediction markets joining it.
2. **Is the borrowed USDC synthetic?** No. It is real USDC, USDT or SOL lent from Vanna's credit pools.
3. **How can you lend more than the deposit?** The funds are held by an account only Vanna's program can sign for. They can go only to allowlisted venues, the whole account is re-priced after every action, and an action that leaves it below the borrow line reverts.
4. **Can a borrower withdraw the loan?** Not the leveraged part. A withdrawal is allowed only while what remains covers the debt at its loan-to-value, which is an ordinary overcollateralized loan. Everything beyond that works only inside connected venues.
5. **Is it undercollateralized lending?** The loan can be larger than the deposit, but it is secured: what the loan buys stays in the account and backs it.
6. **Why not just use a perp DEX's leverage?** It exists only inside that venue. Vanna's credit can hold spot on one venue and a short on another, so a hedge counts as one position.
7. **What does borrowing cost?** A borrow APR set by pool utilization, not a funding fee. Testnet USDC on 24 Nov 2026: 7.9% at 95% utilization. If the credit is used on perps, that venue's funding applies to the perp leg.
8. **How much leverage?** Up to 10x. The app opens at about 4x, by collateral (5.2); limits then rise per trader.
9. **Can I bring positions I already hold elsewhere?** You connect your wallet and open positions from the Vanna account, because the program has to be able to close them.
10. **Which venues are integrated?** Solana testnet: Kamino, Jupiter, Titan, Phoenix, Perena, World and Derive options. Stellar testnet: Blend, Soroswap, Aquarius. Next: Polymarket, then Monad and its venues.
11. **Does it matter which venues you integrate?** Depth matters most, then risk tooling. We add a venue when it has the liquidity to liquidate into.
12. **Is it cross-chain?** Multi-chain: Solana and Stellar accounts are separate. Options show how other chains' liquidity arrives: traded on Solana, hedged on Derive.
13. **What can I build that I can't build today?** A delta-neutral trade across spot and perps, a covered call on SOL, a put under a holding, a carry trade on borrowed USDC, or all of them, with one collateral pool and one number to watch (5.4).

### Prediction markets
14. **How does a bet earn yield while it is open?** YES and NO tokens in our pool are matched, merged into $1 through the market's own program, and that dollar is lent in our USDC pool. The bet stays open.
15. **Does it depend on who wins?** No. A YES and a NO redeem for $1 together at any odds, and the pool never uses an outcome price.
16. **Where does the yield come from?** Traders borrowing from our credit pools. A betting venue has no such borrowers, so this holds even if a venue pays something itself.
17. **Is it self-reinforcing?** By design: more borrowing lifts the yield, which draws more bettors, who deepen the pool.

### Agents
18. **What does Vanna Copilot do that a chatbot can't?** It reads the live account, turns a goal into exact steps sized by the protocol's own maths, shows health before and after, re-checks every step live and runs only after approval.
19. **Can Copilot or MCP move my money?** No. They build and simulate; your wallet signs.
20. **What if the AI is wrong?** It never sets an amount: code does. The plan is shown before it runs, expires in five minutes, and the contract rejects anything unhealthy.
21. **How do funds use MCP?** Their own agents, in Claude, Cursor or Codex, read positions and trade on Vanna credit inside the account's limits, with no custom integration.
22. **How is Vanna AI-native?** Risk agents inside hard on-chain bounds; a Copilot that plans strategies; agents as first-class borrowers with a credit history.

### Risk
23. **How is the health factor calculated?** 1.1 x the sum of each asset's value times its liquidation threshold, divided by debt. Liquidation is at 1.10.
24. **How much can I lose before liquidation?** It depends on leverage (18.1). With SOL posted and USDC held as cash: 81% of the deposit at 2x, 62% at 3x, 44% at 4x.
25. **Has the risk engine been backtested?** Yes: 3.3 million SOL minute prices since August 2020 and 11 years of stock prices (18.2). No bad debt at any leverage tested when liquidations land within a minute.
26. **What about correlated risk?** Similar loans do reach their line together in a crash. We measured by how much in every hour since 2020 (18.3) and size launch caps for it.
27. **How do you handle a collateral depeg?** Liquid assets only, per-asset thresholds, price freshness and time-average checks; collateral that fails a check stops counting for new borrowing. Risk Guardian lowers collateral values and new leverage as markets thin.
28. **What happens if prices are stale?** The main assets use Kamino Scope with Pyth as fallback. Prices that fail freshness, confidence or time-average checks count as zero for new borrowing.
29. **Who liquidates?** Anyone. Our own bot checks accounts and closes perps first; every liquidator earns a bonus.
30. **What protects lenders?** Over-collateralization at liquidation, the bonus cap, caps per pool at launch, and a reserve funded from fees in the mainnet design.
31. **Do you set leverage per user?** Yes, through the Credit Underwriter: a conservative start, then limits from behaviour, as a card issuer sets a limit.
32. **Can issuers of tokenized assets freeze tokens?** Some can. Frozen tokens stop counting as collateral.

### Market, business and company
33. **Why does this need to exist?** Hedge funds borrow about $8 trillion across markets through prime brokers. All of DeFi lends $26B, and none of it follows a trader across venues.
34. **How do you know people need it?** Exchanges already sell one-account margin (Binance, Deribit, Coinbase Prime). On-chain, secured leverage is used wherever it exists ($167M against $217M of USDe in one Kamino market, 2 Oct 2026). Businesses want to offer credit without building it (Coinbase on Morpho, $2.3B+).
35. **Why now?** $39B of tokenized real-world assets and $40B of staking tokens need liquidity; agents need credit rails; exchanges have proved the product off-chain.
36. **Why you?** Security and risk are where credit protocols fail, and they are the founders' careers: an Immunefi All-Star who audits and built credit and derivatives systems, and a product founder and trader who has run a 100K-trader terminal and an exit.
37. **Who is your customer first, and then?** Traders; agents and funds; businesses; institutions (section 7).
38. **How do you get the first users?** The Vanna Credit Monopoly campaign, the founder's 27K+ followers, trading creators and communities, launch partners, Seeker (section 8).
39. **How do you make money?** A share of borrow interest, part of liquidation bonuses, vault performance fees, routing and partner fees, Copilot and MCP usage.
40. **How big can it be?** Scenario, not a forecast: $1B of loans, about 4% of today's DeFi lending, is about $18M a year; $5B is about $80M.
41. **Why would lenders supply?** Traders borrow at leverage, so utilization and yield can run higher than in overcollateralized markets. Testnet USDC: 6.8% supply APR.
42. **Who are the competitors, and what stops them?** Section 10.
43. **What is the moat if code can be forked?** The underwriting record, our place above the venues, and trust (10.5).
44. **How would a wallet or exchange use Vanna?** It plugs in by API, sets its own rules and debt ceiling, and its customers borrow inside its app; interest is shared (5.8).
45. **How would an issuer of tokenized assets use it?** Holders borrow USDC against the asset without selling, under the issuer's rules; the issuer commits redemption liquidity (5.8).
46. **Why would venues want you?** Borrowed dollars become their deposits, volume and open interest, with no lending desk of their own.
47. **Why Solana, Stellar and Monad?** Solana has every market type and a program-owned account for each user. Stellar funded the first build and is deep in real-world assets. Monad is the next home, for the EVM version.
48. **How long have you worked on it?** Since November 2023. Rebuilt twice to reach chains with the markets credit needs.
49. **Who writes the code?** Vatsal wrote the core programs on Solana and Stellar; engineers cover smart contracts, AI, mobile and full-stack; Opinder designs the product and the risk model.
50. **How did the founders meet, and how do they work?** In 2023, through a friend from Koinfox; they worked together for weeks before starting. Opinder owns product, risk design and go-to-market; Vatsal owns contracts and security.
51. **Who owns it, and have you raised?** The two founders own 100%. No equity or tokens sold. Nine grants and prizes, over $230K.
52. **Is there a token?** No. Revenue and a risk record come first.
53. **Are you audited?** In-house reviews are in section 13; external audits come before mainnet.
54. **Are there users?** Private testnet by invitation: traders, including hedge-fund traders. A waitlist of 1,515.
55. **What has to happen before mainnet?** External audits, an independent economic review, a crash drill, a multisig and launch liquidity. Then a capped launch.
56. **What would new funding be used for?** Audits and economic review first, then launch liquidity, then the team.
57. **Is the code open?** Private; read access for named reviewers.
58. **Who can use it?** Testnet, by invitation. Country eligibility for options, prediction markets and tokenized stocks is set before mainnet.

## 18. Risk engine

### 18.1 How it works
Source: `vanna_credit_layer`, commit 624c6a6 (16 Nov 2026), and settings read from the testnet's accounts on 24 Nov 2026.

- **One rule.** Vanna watches the whole account, collateral and borrowed assets together. When it is worth only 1.10 times the debt, after each asset's haircut, it can be liquidated. A loss counts wherever it happens.
- **Two lines.** A stricter line for new risk (borrowing, withdrawing, trading) and the liquidation line. The app shows the second as the health factor.
- **Everything counts.** Tokens, lending receipts, vault shares, Phoenix perp equity and option legs are re-priced together after every action.
- **Funds stay inside.** They can go only to allowlisted programs, and withdrawals must leave the account above the borrow line.

| Collateral | LTV | Liquidation threshold | Liquidator bonus | Max leverage, borrowed USDC kept as USDC |
|---|---|---|---|---|
| USDC, USDT, JupUSD | 80% | 85% | 5% | 5.00x |
| SOL, JitoSOL, JupSOL | 70% | 80% | 5% | 4.50x |
| NVDAx, TSLAx, AAPLx, GOOGLx | 55% | 65% | up to 7% | 3.75x |
| kUSDC, kSOL, USD* (receipts) | 50% | 60% | 5% | 3.50x |

The app adds a safety buffer (health 1.15), so it opens at about 4x. The formula reaches 10x at an LTV of about 90%, with no code change; 10x is meant for hedged books, the most liquid collateral and traders with a record.

**How much of the deposit can be lost before liquidation.** The more you borrow, the less. Example, SOL posted and USDC held as cash: with $1,000 posted and $1,000 borrowed, about $812; with $3,000 borrowed, about $437.

| Share of the deposit lost at liquidation | 2x | 3x | 4x | At the limit |
|---|---|---|---|---|
| Stablecoins posted, borrowed USDC as cash | 82% | 65% | 47% | 29% (5x) |
| SOL posted, borrowed USDC as cash | 81% | 62% | 44% | 34% (4.5x) |
| xStocks posted, borrowed USDC as cash | 77% | 54% | above the limit | 37% (3.75x) |

Checked on live data: the formula reproduces the app's health factor within 0.5% on all 382 borrower accounts we could test (those without perp or option positions).

**Liquidation.** Anyone can liquidate. A call repays up to half the debt, or all of it when the account is close to insolvent or owes $100 or less. The bonus can never exceed what the account has left, and a call that would make a solvent account insolvent is refused. Our bot is built to check every 15 seconds and close Phoenix positions first.

### 18.2 Backtest
*We wrote this backtest ourselves in November 2026. It replays the liquidation rules above on real prices. It is separate from the economic risk assessment in 13.2, which uses simulated prices on the July Stellar contracts.*

Every 6 hours from 11 Aug 2020 to 23 Nov 2026 a new loan opens and is held for 30 days: 9,060 loans per row on 3.3 million SOL minute prices (Binance). A liquidation is filled at the **lowest** price seen between crossing the line and crossing plus the delay, which is deliberately harsh. At 75% of the maximum borrow, losses in hundredths of a percent (basis points) of everything lent, per 30-day loan:

| Strategy | 1 minute | 5 min | 60 min | 4 hours |
|---|---|---|---|---|
| Cash credit | 0 | 0 | 0 | 0 |
| Yield carry | 0 | 0 | 0 | 0 |
| Delta-neutral basis | 0 | 0 | 0.6 | 2.0 |
| Directional long | 0 | 0.26 | 7.4 | 13.6 |

In plain words: if liquidations land within a minute, lenders lost nothing at any leverage tested, through every crash since 2020. If they land a full hour late, the riskiest strategy would have cost lenders 0.07%. Stocks (NVDA, TSLA, AAPL, GOOGL, daily since 2015), liquidated a full trading day late at the worst price: no losses in any of 16 cases. All 60 combinations, the code and what the model does not cover are in the data room.

### 18.3 Correlated risk, in plain words
When SOL falls hard, many similar loans reach their line in the same hour. A lender's real question is how many at once, because that is how much cash the liquidators need.

We counted it on the same 9,060 loans: in the single worst hour since 2020, 34% of delta-neutral loans, 64% of cash-credit loans, 68% of yield-carry loans and 74% of directional loans opened in the previous 30 days would have been liquidated. Hedged loans fail together about half as much as the others, which is why Vanna is built around hedging.

How we use it: each pool launches with a borrow cap that rises only as the book proves itself, limits by asset and by direction come with launch, and Risk Guardian lowers new leverage when the book leans one way. Details and the projected mix of the book by instrument are in the data room.
