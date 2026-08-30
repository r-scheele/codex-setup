# Memecoin Onchain Playbook Reference

This reference condenses the user-provided Google Doc, *The Memecoin Ultimate Guide for Beginners*, reviewed on 2026-08-30. Its claims were not independently validated. Use it as an investigation framework, not as proof or financial advice.

Source: https://docs.google.com/document/d/1-2AZqfQCnEb1qYdHQb073JqFOy0er_tII8pclNWw-JA/

## Contents

- Safety and manipulation checks
- Market and participant signals
- Setup patterns
- Tool roles
- Guide thresholds
- Contradictions and limits

## Safety and manipulation checks

### Token and pool

- Confirm the exact contract and canonical pool.
- Verify the token can be sold under current conditions; a visible chart is not a sellability test.
- Inspect mint, freeze, blacklist, transfer-tax, pause, upgrade, metadata, owner, and equivalent chain-specific privileges.
- Check liquidity amount, ownership, lock or burn state, expiry, and whether liquidity can move to another pool. A lock alone is not proof of safety.
- Estimate slippage and realistic exit capacity for the contemplated position.

### Deployer

- Review previous deployments, rugs, repeated code or liquidity patterns, funding sources, self-sniping, pre-buys, related contracts, and sudden funding before launch.
- Treat dev activity as a signal, never as proof of good intent.

### Holders and early transactions

- Inspect top holders, top-ten concentration, deployer holdings, linked wallets, equal-size wallets, same-source funding, and coordinated timing.
- Review the first 100 transactions when available. Look for varied human-sized entries versus identical amounts, fixed timing, bundled buys, dev-linked snipers, and immediate distribution.
- A clean-looking bubble map can miss concealed ownership. Exchange funding, relays, fresh wallets, bridges, and staged transfers weaken cluster conclusions.

### Volume quality

- Compare volume with liquidity, trade sizes, transaction rhythm, unique makers, fees, and price response.
- Suspicious patterns include huge turnover on shallow liquidity, identical repeated trades, perfectly spaced activity, mirrored buys after sells, smooth price ramps, and volume that disappears when promotion stops.
- Pool fees must be compared in consistent units and against the actual fee schedule. Do not use the guide's fee ratio as a universal formula.

## Market and participant signals

### Distribution

- Healthier: independent wallets, gradual holder growth, mixed position sizes, dips attracting new holders, and whales reducing rather than increasing concentration.
- Riskier: linked top holders, early-wallet domination, concentrated supply, sudden whale exits, falling holder count, or old holders distributing into new attention.

### Wallet behavior

- Early accumulators enter before obvious attention.
- Narrative whales enter after a theme begins to validate.
- Scalpers help explain short-term flow but may exit quickly.
- Deep holders tolerate volatility; systematic traders show repeated timing.
- Study a wallet across many trades. One winning entry does not establish skill.
- Build a private watchlist by reverse-engineering wallets that entered before coordinated promotions, then compare their timing, hold period, exits, narrative preferences, and repeat performance.

### Attention and narratives

- Treat mindshare as persistent market attention, not raw impressions.
- Emerging stage: repeated small mentions, related-token activity, quiet wallet accumulation, and rising holders.
- Peak stage: broad promotion, retail inflow, violent volume, overextension, and early-wallet distribution.
- Decline: falling holders and volume, fewer new wallets, quiet developers, smart-money exits, and fading discussion.
- Require wallet and market evidence alongside social signals. Promotion alone is not confirmation.

## Setup patterns

These patterns describe what to investigate; they do not predict outcomes by themselves.

### New pair

Check liquidity, authorities, deployer, first transactions, bundles, distribution, natural pullbacks, fee/volume quality, and genuine attention. Smooth one-way charts and identical buys are manipulation warnings.

### Bonding or graduation

The guide describes a common sequence: bonding spike, a roughly 40-60% dip, then either failure or reclaim. Investigate pre-bond accumulation, holder growth, whale behavior, distribution, dev activity, and post-bond liquidity. Do not assume a reclaim will occur.

### Pre-migration

Possible signals: deployer activation, new contract interactions, funding movements, slow accumulation, higher lows, rising holders, social anticipation, and early whales. Migration can also manufacture exit liquidity; confirm contract terms and whale behavior.

### Revival or old token

Look for a long quiet base followed by small organic volume, new wallets, rising holders, renewed dev/community activity, current narrative fit, retained liquidity, and improving distribution. Reject perfect ramps, farmed volume, or promotion without onchain participation.

### Smart-money confirmation

Use repeated wallet history, not public leaderboard status or one trade. Watch accumulation before hype and distribution into retail attention. Never copy a wallet blindly; capital size, hedges, private information, and exit ability may differ.

### Pattern layering

The strongest guide-derived setup combines independent narrative, wallet, volume, chart, and timing evidence. Correlated scanner labels do not count as independent confirmation.

### Martingale or controlled jeeting

The guide proposes buying pullbacks, selling bounces, increasing size after another dip, resetting after a win, and stopping after no more than three increases. Treat this as exceptionally high risk. Memecoins can fall without a reliable rebound, liquidity can vanish, and doubling creates nonlinear loss. Do not recommend it by default or portray it as loss recovery.

## Tool roles from the guide

- GMGN: new pairs, live trades, trends, fees, bundles, holders, and wallet activity.
- Axiom: deployer history, holder links, smart money, alerts, and deeper token analysis.
- Solscan: raw Solana contract, authority, and transaction verification.
- Bubblemaps: visual holder relationships and clusters.
- Dexscreener: charts, pairs, liquidity, volume, and alerts.
- DeBank: cross-chain wallet holdings and behavior.
- Arkham and Nansen: tagged or significant wallet flows.
- Telegram bots: alerts and scanning; treat bot signals as unverified leads.

Tool output can be stale, mislabeled, incomplete, or based on different definitions. Verify critical facts at the chain or contract level when possible.

## Guide-derived thresholds

These are heuristics from the document, not validated rules:

- New-pair liquidity above $5,000; under $1,000 described as unsafe.
- Liquidity locked for at least one week or burned.
- Caution when one wallet holds over 5%.
- Advanced filter: top ten holders under 20%.
- New-pair filters: more than 30 holders in the first minutes and organic early wallets.
- Written scanner limits: bundles 25%, insiders 10%, snipers 10%.
- Fee screens: 0.1 SOL for new pairs, 2 SOL near graduation, and 5 SOL after graduation.
- Martingale candidate conditions: liquidity above $10,000 and volume above $100,000.
- Guide position language: 3-10% per trade; this is aggressive unless actual loss at invalidation is much smaller.
- Guide portfolio example: 30% high conviction, 40% active trades, 30% reserves.
- Guide timing observations in WAT: 6-10 PM and 3-7 AM described as active, around 2 AM as early accumulation, and 11 AM-2 PM as lower volume.

Do not silently turn these numbers into recommendations. Show them only when relevant and label them as guide heuristics.

## Contradictions and limits

- The fee guidance conflicts: about 1% of volume, about 1/20, below 1/30, and a separate 25-60 SOL per $1M example. Units and pool fee schedules are mixed.
- The text says bundle 25%, insider 10%, and sniper 10%; the screenshot appears to use different limits, including roughly 15% snipers and 10% bundles.
- Liquidity thresholds vary between $1,000, $5,000, and $10,000 depending on the section.
- Holder rules mix a 5% single-wallet warning with a top-ten-under-20% filter.
- Time-window, rug-timing, predictability, and win-rate claims have no cited dataset or backtest.
- Screenshots are illustrative anecdotes, not performance evidence.
- The guide contains referral links for Axiom and GMGN, so tool recommendations may be commercially biased.
- It omits robust treatment of maximum drawdown, correlation, taxes, custody, key security, MEV, priority fees, execution failure, and statistically measured expectancy.

When these limitations matter, say so plainly and prefer current, chain-specific evidence over the guide.
