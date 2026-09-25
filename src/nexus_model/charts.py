"""Charts for the model. Each function saves an SVG to the assets folder."""
from __future__ import annotations

from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

from .assumptions import load_assumptions
from .capex import capex_table
from .revenue import revenue_table, revenue_totals
from .roi import roi_scenarios, cash_runway

ASSETS = Path(__file__).resolve().parents[2] / "assets"

# Colourblind-safe categorical palette (Okabe-Ito subset).
PALETTE = ["#0072B2", "#E69F00", "#009E73", "#D55E00", "#CC79A7",
           "#56B4E9", "#F0E442", "#999999", "#5D3A9B"]
GRID = "#d9d9d9"


def _style(ax):
    ax.spines[["top", "right"]].set_visible(False)
    ax.yaxis.grid(True, color=GRID, linewidth=0.8)
    ax.set_axisbelow(True)


def _fmt_millions(x, _pos=None):
    return f"£{x/1e6:.1f}m"


def chart_capex(assumptions: dict | None = None, out: Path | None = None) -> Path:
    a = assumptions or load_assumptions()
    df = capex_table(a)
    out = out or ASSETS / "capex_breakdown.svg"
    fig, ax = plt.subplots(figsize=(9, 5))
    ax.barh(df["name"][::-1], df["amount_gbp"][::-1], color=PALETTE[0])
    _style(ax)
    ax.xaxis.set_major_formatter(_fmt_millions)
    ax.set_title("NEXUS CAPEX cost plan (£50m ceiling)", loc="left", fontsize=13, weight="bold")
    for y, v in enumerate(df["amount_gbp"][::-1]):
        ax.text(v + 3e5, y, f"£{v/1e6:.1f}m", va="center", fontsize=9)
    fig.tight_layout()
    fig.savefig(out, dpi=130, bbox_inches="tight")
    plt.close(fig)
    return out


def chart_revenue_scenarios(assumptions: dict | None = None, out: Path | None = None) -> Path:
    a = assumptions or load_assumptions()
    df = revenue_table(a)
    out = out or ASSETS / "revenue_scenarios.svg"
    fig, ax = plt.subplots(figsize=(10, 6))
    bottoms = {"conservative": 0.0, "base": 0.0, "optimistic": 0.0}
    x = ["Conservative", "Base", "Optimistic"]
    keys = ["conservative_gbp", "base_gbp", "optimistic_gbp"]
    for i, (_, row) in enumerate(df.iterrows()):
        vals = [row[k] for k in keys]
        ax.bar(x, vals, bottom=[bottoms["conservative"], bottoms["base"], bottoms["optimistic"]],
               color=PALETTE[i % len(PALETTE)], label=row["stream"], edgecolor="white", linewidth=0.5)
        bottoms["conservative"] += vals[0]
        bottoms["base"] += vals[1]
        bottoms["optimistic"] += vals[2]
    _style(ax)
    ax.yaxis.set_major_formatter(_fmt_millions)
    ax.set_title("Annual revenue by stream and scenario", loc="left", fontsize=13, weight="bold")
    ax.legend(fontsize=8, bbox_to_anchor=(1.01, 1), loc="upper left", frameon=False)
    for xi, key in zip(x, ["conservative", "base", "optimistic"]):
        ax.text(xi, bottoms[key] + 1e5, f"£{bottoms[key]/1e6:.2f}m",
                ha="center", fontsize=10, weight="bold")
    fig.tight_layout()
    fig.savefig(out, dpi=130, bbox_inches="tight")
    plt.close(fig)
    return out


def chart_operating_position(opex_case: str = "revised", assumptions: dict | None = None,
                             out: Path | None = None) -> Path:
    a = assumptions or load_assumptions()
    df = roi_scenarios(opex_case, a)
    out = out or ASSETS / "operating_position.svg"
    fig, ax = plt.subplots(figsize=(9, 5))
    x = df["scenario"].str.capitalize()
    ax.bar(x, df["annual_revenue_gbp"], width=0.38, align="edge", color=PALETTE[2], label="Revenue")
    ax.bar(x, df["annual_opex_gbp"], width=-0.38, align="edge", color=PALETTE[3], label="OPEX")
    _style(ax)
    ax.yaxis.set_major_formatter(_fmt_millions)
    ax.axhline(0, color="#333", linewidth=0.8)
    ax.set_title(f"Revenue vs OPEX by scenario (OPEX case: {opex_case})",
                 loc="left", fontsize=13, weight="bold")
    ax.legend(frameon=False, fontsize=9)
    for i, (_, r) in enumerate(df.iterrows()):
        ax.text(i, r["annual_revenue_gbp"] + 1e5,
                f"net £{r['net_annual_gbp']/1e6:+.1f}m", ha="center", fontsize=9)
    fig.tight_layout()
    fig.savefig(out, dpi=130, bbox_inches="tight")
    plt.close(fig)
    return out


def chart_cash_runway(opex_case: str = "revised", scenario: str = "base",
                      assumptions: dict | None = None, out: Path | None = None) -> Path:
    a = assumptions or load_assumptions()
    df = cash_runway(opex_case, scenario, a)
    out = out or ASSETS / "cash_runway.svg"
    fig, ax = plt.subplots(figsize=(9, 5))
    ax.plot(df["year"], df["reserve_balance_gbp"], marker="o", color=PALETTE[0], linewidth=2)
    ax.fill_between(df["year"], df["reserve_balance_gbp"], 0,
                    where=df["reserve_balance_gbp"] >= 0, color=PALETTE[0], alpha=0.12)
    _style(ax)
    ax.axhline(0, color=PALETTE[3], linewidth=1, linestyle="--")
    ax.yaxis.set_major_formatter(_fmt_millions)
    ax.set_xlabel("Year")
    ax.set_title(f"Working capital reserve runway ({scenario} revenue, {opex_case} OPEX)",
                 loc="left", fontsize=13, weight="bold")
    fig.tight_layout()
    fig.savefig(out, dpi=130, bbox_inches="tight")
    plt.close(fig)
    return out


def build_all(assumptions: dict | None = None) -> list[Path]:
    ASSETS.mkdir(exist_ok=True)
    a = assumptions or load_assumptions()
    return [
        chart_capex(a),
        chart_revenue_scenarios(a),
        chart_operating_position("revised", a),
        chart_cash_runway("revised", "base", a),
    ]
