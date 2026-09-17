"""
Deterministic EPR Obligation and Penalty Calculator for Indian PIBOs.

Grounded in Schedule II of the Plastic Waste Management Rules, 2016
(notified under G.S.R. 133(E) and subsequent amendments).

Calculates:
  1. Mandatory recycling target tonnage by plastic packaging category (I, II, III, IV)
  2. Mandatory recycled plastic content usage obligations
  3. Estimated EPR certificate procurement costs (current market price ranges)
  4. Environmental Compensation (EC) penalty liability and 3-year refund schedule
"""

from typing import Dict, Any, Optional

# Statutory recycling target percentages as a fraction of introduced packaging
RECYCLING_TARGETS = {
    "2024-25": {"cat_1": 50, "cat_2": 30, "cat_3": 30, "cat_4": 100},
    "2025-26": {"cat_1": 60, "cat_2": 40, "cat_3": 40, "cat_4": 100},
    "2026-27": {"cat_1": 70, "cat_2": 50, "cat_3": 50, "cat_4": 100},
    "2027-28": {"cat_1": 80, "cat_2": 60, "cat_3": 60, "cat_4": 100},
    "2028-29": {"cat_1": 80, "cat_2": 60, "cat_3": 60, "cat_4": 100},
}

# Statutory minimum recycled content percentages in packaging
RECYCLED_CONTENT_TARGETS = {
    "2024-25": {"cat_1": 0, "cat_2": 0, "cat_3": 0, "cat_4": 0},
    "2025-26": {"cat_1": 30, "cat_2": 10, "cat_3": 5, "cat_4": 0},
    "2026-27": {"cat_1": 40, "cat_2": 20, "cat_3": 10, "cat_4": 0},
    "2027-28": {"cat_1": 50, "cat_2": 30, "cat_3": 10, "cat_4": 0},
    "2028-29": {"cat_1": 60, "cat_2": 30, "cat_3": 10, "cat_4": 0},
}

# Category descriptive metadata
CATEGORY_METADATA = {
    "cat_1": {
        "name": "Category I: Rigid Plastics",
        "description": "Bottles, jars, caps, containers, crates, drums",
        "cert_price_range_inr": (3500, 8000),
    },
    "cat_2": {
        "name": "Category II: Flexible Plastics",
        "description": "Single or multilayer plastic-only pouches, sachets, sheets, bags",
        "cert_price_range_inr": (6000, 14000),
    },
    "cat_3": {
        "name": "Category III: Multilayered Plastics (MLP)",
        "description": "Packaging with plastic + non-plastic layer (e.g. foil/paperboard)",
        "cert_price_range_inr": (8000, 20000),
    },
    "cat_4": {
        "name": "Category IV: Compostable Plastics",
        "description": "IS/ISO 17088 certified biodegradable sheets & carry bags",
        "cert_price_range_inr": (4000, 10000),
    },
}

# Standard Environmental Compensation rate (CPCB guideline baseline per MT of deficit)
DEFAULT_EC_RATE_INR = 5000

ANNUAL_RETURN_DEADLINE = {
    "statutory_date": "June 30",
    "typical_extended_date": "September 30 / October 31 (subject to annual CPCB circular)",
    "note": (
        "Statutory filing deadline under Rule 11.3 is June 30 following the financial year. "
        "CPCB frequently notifies transitional extension windows up to September 30. "
        "Non-filing attracts automatic Environmental Compensation penalties and customs holds."
    ),
}


def get_target(fiscal_year: str) -> dict:
    """Return category-wise statutory targets for a specific fiscal year."""
    if fiscal_year in RECYCLING_TARGETS:
        return {
            "fiscal_year": fiscal_year,
            "found": True,
            "recycling_targets_pct": RECYCLING_TARGETS[fiscal_year],
            "recycled_content_pct": RECYCLED_CONTENT_TARGETS.get(fiscal_year, {}),
            "source": "Schedule II, Clause 7 of PWM Rules (MoEFCC Notification G.S.R. 133(E))",
        }
    return {
        "fiscal_year": fiscal_year,
        "found": False,
        "message": (
            f"No verified target matrix in database for {fiscal_year}. "
            f"Supported years are: {', '.join(RECYCLING_TARGETS.keys())}."
        ),
    }


def get_annual_return_deadline() -> dict:
    return ANNUAL_RETURN_DEADLINE


def calculate_liability(
    pibo_type: str,
    fiscal_year: str,
    tonnages: Dict[str, float],
) -> Dict[str, Any]:
    """
    Computes statutory obligations, certificate costs, and penalty liabilities.

    Args:
        pibo_type: "Producer", "Importer", "Brand Owner", or "Seller"
        fiscal_year: Target fiscal year, e.g. "2026-27"
        tonnages: {"cat_1": float, "cat_2": float, "cat_3": float, "cat_4": float} in Metric Tonnes
    """
    fy = fiscal_year if fiscal_year in RECYCLING_TARGETS else "2026-27"
    recycle_rates = RECYCLING_TARGETS[fy]
    recycled_content_rates = RECYCLED_CONTENT_TARGETS.get(fy, {})

    categories_breakdown = {}
    total_introduced_mt = 0.0
    total_recycling_target_mt = 0.0
    total_recycled_content_target_mt = 0.0
    min_cert_cost_inr = 0.0
    max_cert_cost_inr = 0.0

    for cat_key, meta in CATEGORY_METADATA.items():
        qty_mt = float(tonnages.get(cat_key, 0.0) or 0.0)
        total_introduced_mt += qty_mt

        recycle_pct = recycle_rates.get(cat_key, 0)
        recycle_target_mt = (qty_mt * recycle_pct) / 100.0
        total_recycling_target_mt += recycle_target_mt

        content_pct = recycled_content_rates.get(cat_key, 0)
        recycled_content_mt = (qty_mt * content_pct) / 100.0
        total_recycled_content_target_mt += recycled_content_mt

        p_min, p_max = meta["cert_price_range_inr"]
        cost_min = recycle_target_mt * p_min
        cost_max = recycle_target_mt * p_max
        min_cert_cost_inr += cost_min
        max_cert_cost_inr += cost_max

        categories_breakdown[cat_key] = {
            "name": meta["name"],
            "introduced_mt": round(qty_mt, 2),
            "recycling_target_pct": recycle_pct,
            "recycling_obligation_mt": round(recycle_target_mt, 2),
            "recycled_content_mandate_pct": content_pct,
            "recycled_content_required_mt": round(recycled_content_mt, 2),
            "cert_market_rate_inr_per_mt": f"Rs {p_min:,} - Rs {p_max:,}",
            "estimated_cert_cost_range_inr": [round(cost_min), round(cost_max)],
        }

    # Environmental Compensation exposure if 100% of recycling obligation is missed
    ec_exposure_inr = total_recycling_target_mt * DEFAULT_EC_RATE_INR

    return {
        "pibo_type": pibo_type,
        "fiscal_year": fy,
        "total_introduced_packaging_mt": round(total_introduced_mt, 2),
        "total_recycling_obligation_mt": round(total_recycling_target_mt, 2),
        "total_recycled_content_required_mt": round(total_recycled_content_target_mt, 2),
        "estimated_cert_procurement_cost_range_inr": {
            "min": round(min_cert_cost_inr),
            "max": round(max_cert_cost_inr),
            "formatted": f"Rs {round(min_cert_cost_inr):,} - Rs {round(max_cert_cost_inr):,}",
        },
        "potential_ec_penalty_exposure_inr": round(ec_exposure_inr),
        "ec_refund_schedule": {
            "year_1_fulfillment": f"85% refund (Rs {round(ec_exposure_inr * 0.85):,})",
            "year_2_fulfillment": f"60% refund (Rs {round(ec_exposure_inr * 0.60):,})",
            "year_3_fulfillment": f"30% refund (Rs {round(ec_exposure_inr * 0.30):,})",
            "after_year_3": "0% refund (forfeited permanently)",
        },
        "categories": categories_breakdown,
        "governing_rules": "Schedule II of PWM Rules, 2016 (MoEFCC)",
    }
