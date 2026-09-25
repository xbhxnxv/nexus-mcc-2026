"""Annual operating cost."""
from __future__ import annotations

import pandas as pd

from .assumptions import load_assumptions


def opex_table(assumptions: dict | None = None) -> pd.DataFrame:
    """Return the revised OPEX breakdown (Executive Summary figure)."""
    a = assumptions or load_assumptions()
    df = pd.DataFrame(a["opex"]["breakdown_revised"])
    total = df["amount_gbp"].sum()
    df["share_pct"] = (df["amount_gbp"] / total * 100).round(1)
    return df.sort_values("amount_gbp", ascending=False).reset_index(drop=True)


def opex_annual(case: str = "revised", assumptions: dict | None = None) -> int:
    """Return the annual OPEX for a named case: 'revised' or 'early'.

    'revised' is the £4.5m Executive Summary figure and the default.
    'early' is the £1.9m Layout Plan / Pitch Deck estimate, kept for comparison.
    """
    a = assumptions or load_assumptions()
    if case == "early":
        return a["opex"]["early_estimate_gbp"]
    if case == "revised":
        return a["opex"]["revised_estimate_gbp"]
    raise ValueError("case must be 'revised' or 'early'")
