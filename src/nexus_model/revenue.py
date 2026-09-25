"""Revenue streams across conservative, base and optimistic scenarios."""
from __future__ import annotations

import pandas as pd

from .assumptions import load_assumptions

SCENARIOS = ("conservative", "base", "optimistic")


def revenue_table(assumptions: dict | None = None) -> pd.DataFrame:
    """Return one row per revenue stream with all three scenario columns."""
    a = assumptions or load_assumptions()
    rows = []
    for s in a["revenue"]["streams"]:
        rows.append(
            {
                "stream": s["name"],
                "conservative_gbp": s["conservative_gbp"],
                "base_gbp": s["base_gbp"],
                "optimistic_gbp": s["optimistic_gbp"],
                "basis": s["basis"],
            }
        )
    return pd.DataFrame(rows)


def revenue_totals(assumptions: dict | None = None) -> dict:
    """Return the total annual revenue for each scenario."""
    df = revenue_table(assumptions)
    return {
        "conservative": int(df["conservative_gbp"].sum()),
        "base": int(df["base_gbp"].sum()),
        "optimistic": int(df["optimistic_gbp"].sum()),
    }
