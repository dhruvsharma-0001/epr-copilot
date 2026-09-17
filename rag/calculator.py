"""
Deterministic deadline/target lookup -- deliberately NOT an LLM.

This is intentionally thin. We only have two verified-from-reporting data
points on the recycling/reuse target schedule (see kb008 in
knowledge_base.py, flagged confidence="needs_verify"). Rather than have the
LLM (or a hardcoded table) invent a plausible-looking full year-by-year
schedule, this calculator only returns the specific data points we actually
have, and is explicit about what it doesn't know.

This is the correct failure mode for a compliance tool: say "I don't have
a verified figure for that" rather than fabricate one that looks
authoritative. Expand this table only as you verify each year/category
against the official CPCB target notification.
"""

KNOWN_TARGETS = {
    "2026-27": {
        "recycle_reuse_pct": 70,
        "source": "kb008 (needs_verify) -- reported industry summaries, not yet "
                   "checked against official CPCB notification",
    },
    "2028-29": {
        "recycle_reuse_pct": 100,
        "source": "kb008 (needs_verify) -- reported industry summaries, not yet "
                   "checked against official CPCB notification",
    },
}

ANNUAL_RETURN_DEADLINE = {
    "typical_date": "September 30",
    "note": (
        "Commonly reported as the annual EPR return deadline for the preceding "
        "financial year. NOT independently verified against the current-year "
        "CPCB portal notification -- confirm before relying on this date. "
        "Missing the deadline is reported to count as zero fulfilment for the "
        "full annual obligation."
    ),
}


def get_target(fiscal_year: str) -> dict:
    """Look up the recycle/reuse target for a given fiscal year, e.g. '2026-27'."""
    if fiscal_year in KNOWN_TARGETS:
        data = KNOWN_TARGETS[fiscal_year]
        return {
            "fiscal_year": fiscal_year,
            "found": True,
            "recycle_reuse_pct": data["recycle_reuse_pct"],
            "source": data["source"],
        }
    return {
        "fiscal_year": fiscal_year,
        "found": False,
        "message": (
            f"No verified target figure in this prototype's knowledge base for "
            f"{fiscal_year}. Known data points only cover 2026-27 (70%) and "
            f"2028-29 (100%). Check the CPCB EPR portal directly for the "
            f"authoritative figure for this year."
        ),
    }


def get_annual_return_deadline() -> dict:
    return ANNUAL_RETURN_DEADLINE
