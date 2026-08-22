# Research protocol

## 1. Define the case

- Capture ticker, legal issuer, CIK or foreign identifier, exchange/OTC tier, country of incorporation and operations, security class, ADS ratio, currency, timestamp, and horizon.
- If no ticker is supplied, define a price-unrestricted discovery universe using market capitalization, liquidity, jurisdictions, excluded security types, intended horizon, and risk objective. Do not invent a sub-$5 ceiling. Default to micro-, small-, and mid-cap asymmetric opportunities; include at most one larger-cap anchor in a small diversified basket unless the user requests a broader quality screen.
- For broad searches, scan multiple themes before ranking. Include memory/semiconductors, defense/drones, robotics/automation, commodities/energy, and other current opportunity sets unless the user narrows the scope.
- Ask what the user wants to know only when it materially changes the work: long-horizon fundamentals, catalyst watch, dilution audit, Reddit-claim verification, or comparative screen.
- Preserve point-in-time data. A later filing must not silently replace what was knowable on the requested date.

## 2. Resolve identity and reporting status

- Match ticker to legal issuer and regulator record.
- Check symbol/name changes, mergers, reverse splits, bankruptcy, delisting notices, reporting delinquency, shell status, trading suspensions, and auditor changes.
- For OTC issuers, identify SEC-reporting, Regulation A, bank-reporting, international-reporting, or alternative-reporting status.

## 3. Build a dated capital-structure table

Record source date and source URL for:

- authorized, issued, outstanding, and public float
- voting/control preferred shares and conversion ratios
- warrants, options, RSUs, convertible notes, and price-protection or repricing clauses
- shares reserved for conversion, employee plans, acquisitions, and resale holders
- active S-1/F-1/S-3 shelves, 424B prospectuses, ATMs, equity lines, private placements, and offering history
- reverse-split history and post-split issuance

Reconcile conflicts by date and definition. Do not call authorized headroom “dilution” until issuance is possible; do not ignore it as financing capacity. Model known dilution separately from registered capacity.

## 4. Test solvency and operating proof

- Calculate quarterly operating cash burn and cash runway. Adjust for one-off working-capital swings when material and show both raw and normalized assumptions.
- Map debt, lease, milestone, redemption, and preferred obligations by due date.
- Read going-concern, subsequent-events, related-party, commitments, contingencies, and legal-proceedings notes.
- Trace revenue to products, customers, contracts, or operating units. Check gross margin, receivables, deferred revenue, backlog quality, customer concentration, and cash collection.
- Compare management claims with reported KPIs across at least three periods when available.

## 5. Validate the catalyst

- Name the event, exact date/window, primary source, remaining prerequisites, responsible third party, and expected financial impact.
- Check whether the catalyst is binding, conditional, preliminary, non-binding, subject to financing, or already completed.
- Search prior guidance for delays or quiet changes.
- Ask what can happen before the catalyst: offering, warrant exercise, lock-up expiry, vote, split, compliance deadline, or cash shortfall.
- Separate binary events from repeatable operating progress.

## 6. Inspect market structure

- Timestamp price, market cap, volume, dollar volume, spread, float, float turnover, volatility, halts, and recent gaps.
- Use split-adjusted charts, but separately reconstruct dilution and reverse-split history; an adjusted chart can make old prices look misleadingly enormous.
- Treat short interest and short-sale volume as different datasets. Record reporting date and source.
- Avoid targets based on share price alone. Use current and fully diluted share counts in valuation scenarios.

## 7. Audit people and promotion

- Check executive/director history, prior issuers, bankruptcies, enforcement, litigation, compensation, related parties, and open-market insider purchases versus grants or option exercises.
- Map Reddit/social claims to primary sources. Search for copied wording, same-ticker-only accounts, sudden account revival, synchronized posting, undisclosed positions, paid promotion, blocked bearish questions, and unsupported urgency.
- Record credible counterarguments and factual corrections from comments; verify those too.

## 8. Form scenarios

- **Bull:** Specify verified milestones and capital required.
- **Base:** Use conservative operating and dilution assumptions.
- **Bear:** Include financing failure, dilution, delay, delisting, litigation, clinical/technical failure, and liquidity exit risk as applicable.
- State invalidators for every scenario. Do not assign probabilities without an evidence-based model.

## 9. Rank and allocate

- Write every company as `Full Company Name (TICKER)`; never use a bare ticker as the company label.
- State whether the ranking optimizes risk-adjusted quality, catalyst upside, or maximum speculation.
- For a supplied budget, default to a 3-5 company basket across distinct business drivers. Show dollars and percentages, assume fractional shares only when stated, and explain each holding's role.
- Keep the largest weight in the company with the strongest solvency and operating proof. Keep the smallest weight in the highest-dilution, pre-profit, binary, or execution-dependent company.
- State plainly when the proposed holdings diversify themes but remain one risky asset class.

## 10. Complete the adversarial pass

- Search the newest filings after the promoted news date.
- Search the filing for `going concern`, `substantial doubt`, `warrant`, `convertible`, `variable`, `floor price`, `reset`, `anti-dilution`, `ATM`, `equity line`, `related party`, `material weakness`, `default`, `delisting`, and `reverse split`.
- Recalculate per-share outcomes using fully diluted shares.
- List missing documents and stale data explicitly.
