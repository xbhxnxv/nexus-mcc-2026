"""CAPEX cost plan and the checks that keep it honest."""
from __future__ import annotations

import pandas as pd

from .assumptions import load_assumptions


def capex_table(assumptions: dict | None = None) -> pd.DataFrame:
    """Return the CAPEX components as a table with pounds and percentage share."""
    a = assumptions or load_assumptions()
    rows = a["capex"]["components"]
    df = pd.DataFrame(rows)
    total = df["amount_gbp"].sum()
    df["share_pct"] = (df["amount_gbp"] / total * 100).round(1)
    df = df.sort_values("amount_gbp", ascending=False).reset_index(drop=True)
    return df[["name", "amount_gbp", "share_pct", "note"]]


def capex_check(assumptions: dict | None = None) -> dict:
    """Confirm the cost plan balances against the £50m ceiling.

    Returns the total, the ceiling, the variance and a pass/fail flag. The
    proposal lives or dies on staying under the ceiling, so this is the first
    thing the model verifies.
    """
    a = assumptions or load_assumptions()
    ceiling = a["capex"]["ceiling_gbp"]
    total = sum(c["amount_gbp"] for c in a["capex"]["components"])
    variance = ceiling - total
    return {
        "total_gbp": total,
        "ceiling_gbp": ceiling,
        "variance_gbp": variance,
        "within_ceiling": total <= ceiling,
    }


def blended_construction_rate(assumptions: dict | None = None) -> dict:
    """Rebuild the 60/40 spatial split that produces the blended build rate.

    High-specification lab space and lower-cost support space are costed at
    different rates, then combined. Reproducing this shows the headline
    build rate is a consequence of the space mix rather than a discount.
    """
    a = assumptions or load_assumptions()
    b = a["construction_benchmark"]
    gia = a["project"]["gia_m2"]

    high_area = gia * b["high_spec_fraction"]
    support_area = gia * b["support_fraction"]
    high_cost = high_area * b["high_spec_rate_per_m2"]
    support_cost = support_area * b["support_rate_per_m2"]
    base_cost = high_cost + support_cost
    blended_rate = base_cost / gia
    with_breeam = base_cost * (1 + b["breeam_premium_pct"])

    return {
        "high_spec_area_m2": high_area,
        "support_area_m2": support_area,
        "base_construction_gbp": base_cost,
        "blended_rate_per_m2": round(blended_rate, 0),
        "breeam_premium_pct": b["breeam_premium_pct"],
        "construction_with_breeam_gbp": round(with_breeam, 0),
        "bcis_range_per_m2": (b["bcis_low_per_m2"], b["bcis_high_per_m2"]),
    }
