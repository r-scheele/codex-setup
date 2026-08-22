---
name: research-penny-stocks
description: Research low-priced, microcap, small-cap, mid-cap, OTC, distressed, and asymmetric-growth stocks with an evidence-first, manipulation-aware workflow and no default share-price ceiling. Use when Codex is asked to discover opportunities without a ticker, investigate a named company, screen themes such as memory chips, defense, drones, robotics, automation, mining, or energy, vet social-media DD, analyze dilution or cash runway, compare speculative stocks, build a catalyst watchlist, rank opportunities, or allocate a small budget across a diversified research basket.
---

# Research Speculative and Asymmetric Stocks

## Core rule

Treat Reddit and social media as idea flow and sentiment evidence, never as proof. Verify every material claim with the newest available primary source. Keep research separate from personalized financial advice or trade execution.

Do not equate a low share price with a small or inexpensive company. Unless the user explicitly sets a price limit, keep the screen price-unrestricted and compare market capitalization, enterprise value, fully diluted share count, liquidity, valuation, solvency, and catalyst quality.

## Choose the research mode

- **Ticker supplied:** Resolve the issuer and perform single-company diligence.
- **No ticker supplied:** Run discovery mode. Build a candidate funnel across at least five relevant themes before ranking, unless the user narrows the sectors. Prioritize micro-, small-, and mid-cap asymmetric opportunities; do not drift into an all-large-cap list merely because the share-price ceiling was removed.
- **Opportunity search:** Balance the shortlist across distinct themes where evidence supports it. Check memory and semiconductors, defense and drones, robotics and automation, commodities and energy, and other timely sectors; do not let one familiar sector dominate by default.
- **Budget supplied:** Produce a diversified 3-5 company research basket by default. Show dollar amounts, percentages, the fractional-share assumption, and the role and principal risk of each holding. Allow one larger-cap operating-quality anchor when it materially improves durability, but preserve the asymmetric focus. Recommend a single company only when the user explicitly requests concentration.

Always write the full company name followed by the ticker on first mention and in recommendation tables, for example `Everspin Technologies, Inc. (MRAM)`. Never present a ticker alone when naming a company.

## Start every run

1. Record either the supplied ticker or the discovery-screen definition, plus venue, jurisdiction, security type, research timestamp, quoted-price timestamp, and intended horizon.
2. Resolve ticker collisions, renames, mergers, ADS ratios, and reverse splits before using historical data.
3. State whether live browsing and live market data are available. Never present stale prices, share counts, short interest, catalysts, rankings, or subreddit sentiment as current.
4. Read [references/research-protocol.md](references/research-protocol.md) for the full workflow.
5. Read only the additional references needed for the request:
   - Reddit or social claim: [references/reddit-signals.md](references/reddit-signals.md)
   - SEC filings, dilution, financing, ownership, or splits: [references/filing-guide.md](references/filing-guide.md)
   - Biotech, mining, energy, technology, or distressed issuer: [references/sector-checklists.md](references/sector-checklists.md)
   - Source selection: [references/source-map.md](references/source-map.md)

## Apply hard gates before scoring

Mark the case `insufficient evidence` when the issuer or security cannot be resolved, current filings are unavailable, or the key claim cannot be traced to a source.

Mark a prominent `critical risk` when any of these appear:

- SEC suspension, regulator warning, OTC Caveat Emptor or shell warning, delinquent reporting, or unresolved auditor resignation
- serial reverse splits plus repeated dilution, toxic variable-price convertibles, or financing capacity that can overwhelm the current share count
- going-concern warning, inadequate cash runway, near-term debt default, bankruptcy, delisting, or liquidation risk
- no verifiable operations, abrupt unrelated business pivots, undisclosed promotion, or promotional claims that conflict with filings
- unusable liquidity, extreme spread, or a catalyst thesis that requires selling into a market too thin to support the position

Do not let a high composite score hide a critical risk.

## Research in this order

1. **Identity and status:** Confirm issuer, CIK or foreign identifier, venue, reporting status, corporate actions, and regulatory flags.
2. **Capital structure:** Reconcile authorized, issued, outstanding, float, preferred, convertibles, warrants, options, shelves, ATMs, resale registrations, and recent offerings across dated sources.
3. **Solvency and business:** Calculate cash runway, debt maturity pressure, working capital, revenue quality, margins, cash flow, customer concentration, related parties, and going-concern language.
4. **Catalyst and market:** Verify exact catalyst source, date or window, prerequisites, prior delays, financing needs, price/volume reaction, spread, dollar volume, and float turnover.
5. **People and promotion:** Check management history, compensation, related-party deals, insider transactions, promoter compensation, subreddit account behavior, copied posts, and counterarguments.

Use `scripts/calculate_metrics.py` when exact share-count or runway inputs are available. Keep known dilution separate from registered financing capacity, and never double-count an ATM already included in a shelf.

## Evidence discipline

- Prefer regulator filings and agency records over company releases; prefer company releases over media; prefer media over anonymous posts.
- Attach a source URL and publication or filing date on the same bullet, table row, or paragraph as every material fact. If no source can be attached, label the fact unresolved or omit it.
- Label each statement `verified fact`, `company claim`, `community claim`, `calculation`, or `inference` when the distinction is not obvious.
- Quote sparingly. Paraphrase the evidence and preserve the source's actual level of certainty.
- Search for disconfirming evidence before writing the conclusion.
- Distinguish absence of evidence from evidence of absence.
- Separate research timestamp from event date and market-data timestamp.

## Rate the case without false precision

Assign `strong`, `mixed`, `weak`, or `unknown` to:

- evidence quality
- capital structure safety
- liquidity and solvency health
- operating proof and management alignment
- catalyst quality
- market integrity and tradability

Finish with one of: `researchable`, `watch only`, `highly speculative`, `avoid pending new evidence`, or `insufficient evidence`. This is a research disposition, not a buy or sell instruction.

## Produce the brief

Follow [references/output-template.md](references/output-template.md). Lead with the disposition and the single most important risk. Include exact unknowns, the strongest counter-thesis, and the next primary-source event that could change the result.

For ranked screens, show why each company outranks the next one and state whether the ranking is risk-adjusted, catalyst-driven, or upside-seeking. Do not silently mix those objectives.

For watchlists, apply the same minimum identity, filings, dilution, runway, catalyst, and liquidity checks to every company. Record the exact filing, results release, construction update, approval, contract milestone, or other primary-source event that would preserve, promote, demote, or remove it. Do not rank a company with missing fatal-risk data above a fully researched company.
