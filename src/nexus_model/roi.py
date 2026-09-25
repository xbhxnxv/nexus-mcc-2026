"""ROI: operating position per scenario, societal payback and a cash runway view."""
from __future__ import annotations

import pandas as pd

from .assumptions import load_assumptions
from .opex import opex_annual
from .revenue import revenue_totals


def roi_scenarios(opex_case: str = "revised", assumptions: dict | None = None) -> pd.DataFrame:
    """Annual operating position (revenue - OPEX) for each revenue scenario."""
    a = assumptions or load_assumptions()
    totals = revenue_totals(a)
    opex = opex_annual(opex_case, a)
    rows = []
    for scenario, rev in totals.items():
        rows.append(
            {
                "scenario": scenario,
                "annual_revenue_gbp": rev,
                "annual_opex_gbp": opex,
                "net_annual_gbp": rev - opex,
                "operating_ratio": round(rev / opex, 2),
            }
        )
    return pd.DataFrame(rows)


def societal_payback(assumptions: dict | None = None) -> dict:
    """Payback period on the capital investment measured in societal value."""
    a = assumptions or load_assumptions()
    capital = a["project"]["capital_ceiling_gbp"]
    annual = a["societal_value"]["annual_gbp"]
    years = capital / annual
    return {
        "capital_gbp": capital,
        "annual_societal_value_gbp": annual,
        "payback_years": round(years, 1),
        "jobs_supported": a["societal_value"]["jobs_supported"],
    }


def payback_period(net_annual_gbp: float, capital_gbp: float) -> float | None:
    """Simple payback period in years, or None if the net position is negative."""
    if net_annual_gbp <= 0:
        return None
    return round(capital_gbp / net_annual_gbp, 1)


def cash_runway(opex_case: str = "revised", scenario: str = "base",
                assumptions: dict | None = None) -> pd.DataFrame:
    """Year-by-year reserve balance through the ramp-up window.

    The working capital reserve is drawn down each year by any operating
    deficit. This shows whether the reserve lasts the planned ramp-up period.
    """
    a = assumptions or load_assumptions()
    reserve = next(
        c["amount_gbp"] for c in a["capex"]["components"]
        if "working capital" in c["name"].lower()
    )
    rev = revenue_totals(a)[scenario]
    opex = opex_annual(opex_case, a)
    net = rev - opex
    horizon = a["roi"]["horizon_years"]

    rows = []
    balance = reserve
    for year in range(1, horizon + 1):
        balance += net if net < 0 else 0  # reserve only funds deficits
        rows.append(
            {
                "year": year,
                "net_operating_gbp": net,
                "reserve_balance_gbp": round(balance, 0),
                "solvent": balance >= 0 or net >= 0,
            }
        )
    return pd.DataFrame(rows)
