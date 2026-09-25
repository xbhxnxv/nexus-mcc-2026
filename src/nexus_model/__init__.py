"""NEXUS financial model.

A small, auditable model that rebuilds the CAPEX cost plan, OPEX, revenue
scenarios and ROI for the NEXUS consultancy proposal from a single YAML
assumptions file.
"""
from .assumptions import load_assumptions
from .capex import capex_table, capex_check
from .opex import opex_table
from .revenue import revenue_table, revenue_totals
from .roi import roi_scenarios, payback_period

__all__ = [
    "load_assumptions",
    "capex_table",
    "capex_check",
    "opex_table",
    "revenue_table",
    "revenue_totals",
    "roi_scenarios",
    "payback_period",
]

__version__ = "1.0.0"
