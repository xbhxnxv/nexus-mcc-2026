"""Load the assumptions file that drives the whole model."""
from __future__ import annotations

from pathlib import Path
import yaml


DEFAULT_PATH = Path(__file__).resolve().parents[2] / "data" / "assumptions.yaml"


def load_assumptions(path: str | Path | None = None) -> dict:
    """Read data/assumptions.yaml and return it as a plain dict.

    The YAML uses underscores in numbers (e.g. 50_000_000) for readability;
    PyYAML parses these as integers, so no extra handling is needed.
    """
    path = Path(path) if path else DEFAULT_PATH
    if not path.exists():
        raise FileNotFoundError(f"Assumptions file not found: {path}")
    with open(path, "r", encoding="utf-8") as fh:
        return yaml.safe_load(fh)
