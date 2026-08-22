#!/usr/bin/env python3
"""Calculate transparent penny-stock dilution, liquidity, and runway metrics."""

from __future__ import annotations

import argparse
import json
import sys
from decimal import Decimal, InvalidOperation
from pathlib import Path


ZERO = Decimal("0")

EXAMPLE_INPUT = {
    "ticker": "XYZ",
    "as_of": "2026-07-21T16:00:00-04:00",
    "inputs_are_user_verified": True,
    "share_price": 0.5,
    "shares_outstanding": 100000000,
    "public_float": 60000000,
    "daily_share_volume": 12000000,
    "authorized_shares": 500000000,
    "warrant_shares": 20000000,
    "options_rsus_shares": 5000000,
    "convertible_preferred_shares": 30000000,
    "other_committed_shares": 0,
    "registered_capacity_dollars": 25000000,
    "cash_and_equivalents": 8000000,
    "quarterly_operating_cash_burn": 4000000,
    "debt_due_12m": 6000000,
}


def decimal_value(data: dict, key: str, warnings: list[str]) -> Decimal | None:
    value = data.get(key)
    if value is None or value == "":
        return None
    try:
        parsed = Decimal(str(value))
    except InvalidOperation as exc:
        raise ValueError(f"{key} must be numeric") from exc
    if parsed < ZERO:
        raise ValueError(f"{key} must be non-negative")
    return parsed


def output_number(value: Decimal | None) -> float | None:
    if value is None:
        return None
    return float(value.quantize(Decimal("0.0001")))


def calculate(data: dict) -> dict:
    warnings: list[str] = []
    shares = decimal_value(data, "shares_outstanding", warnings)
    if not shares or shares == ZERO:
        raise ValueError("shares_outstanding must be greater than zero")

    share_price = decimal_value(data, "share_price", warnings)
    public_float = decimal_value(data, "public_float", warnings)
    daily_volume = decimal_value(data, "daily_share_volume", warnings)
    authorized = decimal_value(data, "authorized_shares", warnings)
    warrants = decimal_value(data, "warrant_shares", warnings) or ZERO
    awards = decimal_value(data, "options_rsus_shares", warnings) or ZERO
    converts = decimal_value(data, "convertible_preferred_shares", warnings) or ZERO
    committed = decimal_value(data, "other_committed_shares", warnings) or ZERO
    registered_capacity = decimal_value(data, "registered_capacity_dollars", warnings)
    cash = decimal_value(data, "cash_and_equivalents", warnings)
    burn = decimal_value(data, "quarterly_operating_cash_burn", warnings)
    debt_due = decimal_value(data, "debt_due_12m", warnings)

    known_dilutive = warrants + awards + converts + committed
    fully_diluted = shares + known_dilutive
    known_dilution_pct = known_dilutive / shares * Decimal("100")

    market_cap = share_price * shares if share_price is not None else None
    fully_diluted_market_cap = share_price * fully_diluted if share_price is not None else None
    daily_dollar_volume = share_price * daily_volume if share_price is not None and daily_volume is not None else None
    float_turnover_multiple = daily_volume / public_float if daily_volume is not None and public_float else None
    if public_float == ZERO:
        warnings.append("public_float is zero; check the source and definition")
    if public_float is not None and public_float > shares:
        warnings.append("public_float exceeds shares outstanding; reconcile dates and vendor definitions")

    authorized_headroom = None
    if authorized is not None:
        authorized_headroom = authorized - fully_diluted
        if authorized < shares:
            warnings.append("authorized shares are below current shares outstanding; reconcile split adjustments and source dates")
        if authorized_headroom < ZERO:
            warnings.append("known fully diluted shares exceed authorized shares; inspect reservations, assumptions, and instrument terms")

    capacity_shares = None
    capacity_dilution_pct = None
    if registered_capacity is not None:
        if share_price is None or share_price == ZERO:
            warnings.append("registered_capacity_dollars requires a positive share_price to estimate capacity shares")
        else:
            capacity_shares = registered_capacity / share_price
            capacity_dilution_pct = capacity_shares / shares * Decimal("100")
            warnings.append("registered capacity is not issued dilution and actual net shares depend on price, fees, limits, and terms")
            if authorized_headroom is not None and capacity_shares > max(authorized_headroom, ZERO):
                warnings.append("estimated capacity shares exceed naive authorized headroom; issuance may require a split, vote, amendment, or a different price")

    runway_quarters = None
    if cash is not None and burn is not None:
        if burn == ZERO:
            warnings.append("quarterly burn is zero; runway is not meaningful without normalized cash flow")
        else:
            runway_quarters = cash / burn

    cash_after_debt = None
    if cash is not None and debt_due is not None:
        cash_after_debt = cash - debt_due
        if cash_after_debt < ZERO:
            warnings.append("cash is below debt due within 12 months before considering operations or refinancing")

    if public_float is None:
        warnings.append("public_float missing; liquidity and float-turnover analysis remains incomplete")
    if share_price is None:
        warnings.append("share_price missing; market-cap metrics were not calculated")

    return {
        "ticker": data.get("ticker"),
        "as_of": data.get("as_of"),
        "inputs_are_user_verified": bool(data.get("inputs_are_user_verified", False)),
        "current": {
            "shares_outstanding": output_number(shares),
            "public_float": output_number(public_float),
            "market_cap": output_number(market_cap),
        },
        "known_dilution": {
            "known_dilutive_shares": output_number(known_dilutive),
            "fully_diluted_shares": output_number(fully_diluted),
            "known_dilution_pct_of_current": output_number(known_dilution_pct),
            "fully_diluted_market_cap_at_input_price": output_number(fully_diluted_market_cap),
        },
        "financing_capacity": {
            "estimated_capacity_shares_at_input_price": output_number(capacity_shares),
            "estimated_capacity_pct_of_current": output_number(capacity_dilution_pct),
            "authorized_headroom_after_known_dilution": output_number(authorized_headroom),
        },
        "liquidity": {
            "daily_share_volume": output_number(daily_volume),
            "daily_dollar_volume": output_number(daily_dollar_volume),
            "float_turnover_multiple": output_number(float_turnover_multiple),
        },
        "solvency": {
            "cash_runway_quarters": output_number(runway_quarters),
            "cash_less_debt_due_12m": output_number(cash_after_debt),
        },
        "warnings": warnings,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("input", nargs="?", help="JSON file; omit or use - to read stdin")
    parser.add_argument("--example", action="store_true", help="print an example input object and exit")
    args = parser.parse_args()
    if args.example:
        print(json.dumps(EXAMPLE_INPUT, indent=2, sort_keys=True))
        return 0
    try:
        if args.input and args.input != "-":
            data = json.loads(Path(args.input).read_text())
        else:
            data = json.load(sys.stdin)
        print(json.dumps(calculate(data), indent=2, sort_keys=True))
    except (OSError, json.JSONDecodeError, ValueError) as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
