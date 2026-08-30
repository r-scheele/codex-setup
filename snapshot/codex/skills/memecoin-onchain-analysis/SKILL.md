---
name: memecoin-onchain-analysis
description: Assess memecoins and onchain token setups using liquidity, contract, deployer, holder, wallet, volume, narrative, timing, and risk evidence. Use for token due diligence, new-pair reviews, wallet-flow analysis, launch or migration checks, revival candidates, trade post-mortems, and reusable memecoin checklists. Do not use for generic crypto news or automatic trade execution.
---

# Memecoin Onchain Analysis

Turn a chaotic token setup into a short, evidence-led decision. Treat the source guide as a collection of heuristics, not verified market law.

## Operating rules

- For a concrete token, establish the chain and exact contract address before analysing it. Tickers and names are not unique.
- For live or time-sensitive claims, inspect current data and include the observation time. Never present remembered or guide-derived data as current.
- Separate every material claim into: `verified current evidence`, `observed but incomplete`, `guide heuristic`, or `unknown`.
- Never infer safety from a chart, social activity, locked liquidity, or one scanner alone. Corroborate critical checks.
- Never request or expose seed phrases or private keys. Do not connect wallets, sign transactions, send funds, or execute trades.
- Stop the positive thesis when a critical safety gate fails. More bullish signals do not cancel a sell restriction, dangerous authority, removable liquidity, or controlled supply.
- Do not convert incomplete data into a numeric safety score. Use a gate-based verdict.

## Workflow

1. Confirm identity: chain, contract address, launch venue, pair/pool, token age, and requested analysis time.
2. Run safety gates: sellability, mint/freeze or equivalent authorities, liquidity ownership/lock/burn, deployer history, contract privileges, and obvious honeypot or transfer restrictions.
3. Inspect market structure: liquidity depth, volume quality, fees where comparable, slippage, holder concentration, linked wallets, snipers, bundles, and the first transactions.
4. Inspect participants: deployer funding, early accumulators, whales, smart-money behavior, distribution, and holder-count direction. Treat wallet labels and clusters as probabilistic.
5. Inspect attention: narrative stage, social authenticity, wallet participation, volume persistence, and whether attention is emerging, peaking, or fading.
6. Describe the setup only after the gates: new pair, bonding, migration, revival, narrative rotation, momentum, or no clean setup.
7. Define invalidation and risk: what evidence would break the thesis, liquidity or exit constraints, concentration risk, and missing data.

Read [references/playbook.md](references/playbook.md) for the detailed checks, guide-derived thresholds, strategy patterns, tool roles, and known contradictions.

## Verdicts

- `Avoid`: a critical gate fails or manipulation/control risk is material.
- `Insufficient evidence`: the contract, pool, or required current data cannot be verified.
- `Watch`: gates pass so far, but confirmation or market structure is incomplete.
- `Speculative setup`: gates pass and multiple independent signals align; this is not a promise of profit or a safety guarantee.

## Response shape

Lead with the verdict and the strongest reason. Then give:

1. identity and timestamp
2. safety gates
3. liquidity, holders, wallets, and volume
4. narrative/setup stage
5. invalidation and missing evidence

Keep guide heuristics visibly labelled. If the user asks for an entry or exit plan, frame it as a conditional scenario with explicit invalidation, not a directive or guaranteed outcome.
