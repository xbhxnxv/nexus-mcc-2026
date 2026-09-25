#!/usr/bin/env python3
"""Run the full NEXUS model: print the tables, run the ceiling check, build charts.

Usage:
    python scripts/run_model.py

Add the src directory to the path so the package imports without installation.
"""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

import pandas as pd

from nexus_model import (
    load_assumptions,
    capex_table,
    capex_check,
    opex_table,
    revenue_table,
    revenue_totals,
    roi_scenarios,
)
from nexus_model.capex import blended_construction_rate
from nexus_model.roi import societal_payback, cash_runway
from nexus_model import charts

pd.options.display.float_format = lambda v: f"{v:,.0f}"


def money(x):
    return f"£{x:,.0f}"


def main() -> None:
    a = load_assumptions()
    p = a["project"]
    print("=" * 70)
    print(f"{p['name']} - {p['full_name']}")
    print(f"{p['client']} x {p['partner']} | {p['challenge']}")
    print("=" * 70)

    print("\nCAPEX COST PLAN")
    df = capex_table(a)
    for _, r in df.iterrows():
        print(f"  {r['name']:<45} {money(r['amount_gbp']):>12}  {r['share_pct']:>5}%")

    chk = capex_check(a)
    print(f"\n  Total: {money(chk['total_gbp'])}  |  Ceiling: {money(chk['ceiling_gbp'])}"
          f"  |  Variance: {money(chk['variance_gbp'])}")
    print(f"  Within ceiling: {chk['within_ceiling']}")

    print("\nBLENDED CONSTRUCTION RATE (60/40 split)")
    b = blended_construction_rate(a)
    print(f"  High-spec area: {b['high_spec_area_m2']:,.0f} m2 @ £4,000/m2")
    print(f"  Support area:   {b['support_area_m2']:,.0f} m2 @ £3,000/m2")
    print(f"  Blended base rate: £{b['blended_rate_per_m2']:,.0f}/m2"
          f"  (BCIS range £{b['bcis_range_per_m2'][0]:,}-£{b['bcis_range_per_m2'][1]:,})")

    print("\nOPEX (revised, £4.5m)")
    for _, r in opex_table(a).iterrows():
        print(f"  {r['name']:<40} {money(r['amount_gbp']):>12}  {r['share_pct']:>5}%")

    print("\nREVENUE BY SCENARIO")
    totals = revenue_totals(a)
    for k, v in totals.items():
        print(f"  {k.capitalize():<14} {money(v)}")

    print("\nOPERATING POSITION (revised OPEX £4.5m)")
    for _, r in roi_scenarios("revised", a).iterrows():
        print(f"  {r['scenario'].capitalize():<14} net {money(r['net_annual_gbp']):>14}"
              f"  (revenue/OPEX ratio {r['operating_ratio']})")

    print("\nSOCIETAL PAYBACK")
    sp = societal_payback(a)
    print(f"  {money(sp['capital_gbp'])} capital / {money(sp['annual_societal_value_gbp'])}"
          f" annual societal value = {sp['payback_years']} years")
    print(f"  Jobs supported across Tyseley GEID: {sp['jobs_supported']:,}")

    print("\nCASH RUNWAY (base revenue, revised OPEX)")
    for _, r in cash_runway("revised", "base", a).head(6).iterrows():
        print(f"  Year {r['year']}: reserve balance {money(r['reserve_balance_gbp'])}"
              f"  solvent={r['solvent']}")

    print("\nBuilding charts...")
    for path in charts.build_all(a):
        print(f"  saved {path.name}")

    print("\nDone.")


if __name__ == "__main__":
    main()
