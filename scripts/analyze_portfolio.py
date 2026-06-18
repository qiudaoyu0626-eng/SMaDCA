#!/usr/bin/env python3
"""Calculate personal cash-flow and portfolio allocation metrics from JSON."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path


def load_data(path: str) -> dict:
    if path == "-":
        return json.load(sys.stdin)
    with Path(path).open("r", encoding="utf-8") as handle:
        return json.load(handle)


def number(data: dict, key: str, default: float = 0.0) -> float:
    value = float(data.get(key, default))
    if value < 0:
        raise ValueError(f"{key} must not be negative")
    return value


def analyze(data: dict) -> dict:
    income = number(data, "monthly_income")
    essential = number(data, "essential_expenses")
    flexible = number(data, "flexible_budget")
    debt = number(data, "debt_payments")
    emergency = number(data, "emergency_fund")
    target_months = number(data, "emergency_months_target", 6)
    surplus = income - essential - flexible - debt
    holdings = data.get("holdings", [])
    if not isinstance(holdings, list):
        raise ValueError("holdings must be a list")

    total = sum(float(item.get("value", 0)) for item in holdings)
    if any(float(item.get("value", 0)) < 0 for item in holdings):
        raise ValueError("holding values must not be negative")

    rows = []
    warnings = []
    for item in holdings:
        value = float(item.get("value", 0))
        weight = value / total * 100 if total else 0
        target = item.get("target_pct")
        drift = weight - float(target) if target is not None else None
        rows.append({
            "name": str(item.get("name", "Unnamed")),
            "category": str(item.get("category", "unspecified")),
            "value": round(value, 2),
            "weight_pct": round(weight, 2),
            "target_pct": float(target) if target is not None else None,
            "drift_pp": round(drift, 2) if drift is not None else None,
        })
        if weight >= 40:
            warnings.append(f"{item.get('name', 'Unnamed')} is highly concentrated at {weight:.1f}%")
        elif weight > 30:
            warnings.append(f"{item.get('name', 'Unnamed')} is concentrated at {weight:.1f}%")

    target_emergency = essential * target_months
    coverage = emergency / essential if essential else None
    emergency_gap = max(0.0, target_emergency - emergency)
    if emergency_gap > 0:
        warnings.append(f"Emergency fund is short by CNY {emergency_gap:.2f}")
    if surplus < 0:
        warnings.append("Monthly cash flow is negative")

    return {
        "cash_flow": {
            "monthly_surplus": round(surplus, 2),
            "savings_rate_pct": round(surplus / income * 100, 2) if income else None,
            "emergency_coverage_months": round(coverage, 2) if coverage is not None else None,
            "emergency_target": round(target_emergency, 2),
            "emergency_gap": round(emergency_gap, 2),
        },
        "portfolio": {
            "total_value": round(total, 2),
            "holdings": sorted(rows, key=lambda row: row["weight_pct"], reverse=True),
            "stress_loss": {
                "20_pct_decline": round(total * 0.20, 2),
                "30_pct_decline": round(total * 0.30, 2),
                "40_pct_decline": round(total * 0.40, 2),
            },
        },
        "warnings": warnings,
    }


def human(result: dict) -> str:
    cash = result["cash_flow"]
    portfolio = result["portfolio"]
    lines = [
        f"Monthly surplus: CNY {cash['monthly_surplus']:.2f}",
        f"Savings rate: {cash['savings_rate_pct']}%",
        f"Emergency coverage: {cash['emergency_coverage_months']} months",
        f"Emergency gap: CNY {cash['emergency_gap']:.2f}",
        f"Portfolio total: CNY {portfolio['total_value']:.2f}",
        "Holdings:",
    ]
    for row in portfolio["holdings"]:
        drift = "" if row["drift_pp"] is None else f", drift {row['drift_pp']:+.2f}pp"
        lines.append(f"- {row['name']}: CNY {row['value']:.2f}, {row['weight_pct']:.2f}%{drift}")
    if result["warnings"]:
        lines.append("Warnings:")
        lines.extend(f"- {warning}" for warning in result["warnings"])
    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("input", help="UTF-8 JSON file, or - for stdin")
    parser.add_argument("--format", choices=("human", "json"), default="human")
    args = parser.parse_args()
    try:
        result = analyze(load_data(args.input))
    except (OSError, ValueError, TypeError, json.JSONDecodeError) as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 2
    if args.format == "json":
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        print(human(result))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
