"""
Knowledge base for the EPR Compliance Copilot prototype.

*** READ THIS BEFORE YOU USE THIS FOR ANYTHING REAL ***

Every chunk below is a PARAPHRASED SUMMARY built from secondary reporting
(news articles, law-firm blogs, compliance-consultant blogs) about India's
Plastic Waste Management Rules and its amendments. It is NOT the verbatim
legal text, and it has NOT been reviewed by an environmental compliance
professional or lawyer.

Chunks are tagged with a `confidence` field:
  - "reported"      -> multiple independent secondary sources describe this
                        consistently, but it has not been checked against the
                        actual gazette notification.
  - "needs_verify"  -> information is partial, potentially incomplete, or
                        only appeared in one source. Treat as a placeholder.

Before this touches a real customer:
  1. Replace every chunk's `text` with content sourced directly from the
     official MoEFCC gazette notifications and CPCB circulars.
  2. Have a CPCB-empanelled EPR consultant or environmental lawyer review
     the full knowledge base.
  3. Keep a changelog of which notification each chunk maps to, since these
     rules amend every year.

This file exists to demonstrate the RAG architecture end-to-end, not to
give anyone real compliance advice.
"""

KNOWLEDGE_BASE = [
    {
        "id": "kb001",
        "title": "EPR framework origin",
        "citation": "Plastic Waste Management Rules, 2016 (as subsequently amended)",
        "confidence": "reported",
        "text": (
            "India's Extended Producer Responsibility (EPR) framework for plastic "
            "packaging originates in the Plastic Waste Management Rules, 2016, and "
            "has been amended multiple times since. EPR shifts responsibility for "
            "post-consumer plastic packaging waste from local governments onto the "
            "businesses that place that packaging on the market -- producers, "
            "importers, and brand owners, collectively referred to as PIBOs."
        ),
    },
    {
        "id": "kb002",
        "title": "EPR made mandatory (2022 amendment)",
        "citation": "Plastic Waste Management (Amendment) Rules, 2022",
        "confidence": "reported",
        "text": (
            "The 2022 amendment made EPR compliance mandatory for PIBOs across all "
            "plastic packaging categories. PIBOs must register on the CPCB's "
            "centralized EPR portal before selling or importing packaged products "
            "in India, and must meet annual recycling/reuse targets based on the "
            "quantity and category of plastic they place on the market."
        ),
    },
    {
        "id": "kb003",
        "title": "Packaging categories I and II",
        "citation": "CPCB EPR Guidelines",
        "confidence": "reported",
        "text": (
            "Plastic packaging is divided into categories for EPR purposes. "
            "Category I covers rigid plastic packaging. Category II covers "
            "flexible plastics, single or multi-layer, including plastic sheets, "
            "covers, carry bags, sachets, or pouches."
        ),
    },
    {
        "id": "kb004",
        "title": "Multi-layered plastic packaging (category III?) -- INCOMPLETE",
        "citation": "unconfirmed -- needs official source",
        "confidence": "needs_verify",
        "text": (
            "Secondary sources reference an additional category (commonly labelled "
            "Category III) for multi-layered plastic (MLP) packaging, distinct from "
            "Category II. The exact boundary between Category II and Category III, "
            "and whether a Category IV exists, was NOT reliably confirmed from "
            "available reporting. DO NOT rely on this chunk for a real category "
            "determination -- pull the exact definitions from the CPCB EPR "
            "Guidelines document directly."
        ),
    },
    {
        "id": "kb005",
        "title": "New EPR for Packaging Rules, 2024 (effective April 2026)",
        "citation": "Environment Protection (EPR for Packaging) Rules, 2024",
        "confidence": "reported",
        "text": (
            "The EPR for Packaging Rules, 2024, came into force on April 1, 2026. "
            "They extend lifecycle EPR responsibility beyond plastics alone to "
            "paper, glass, metal, and sanitary products, and separately expand EPR "
            "to cover non-ferrous metal scrap (aluminium, copper, zinc and their "
            "alloys) and construction & demolition waste, also effective April 1, "
            "2026."
        ),
    },
    {
        "id": "kb006",
        "title": "Mandatory QR/barcode labeling (2025 amendment)",
        "citation": "Plastic Waste Management (Amendment) Rules, 2025, Rule 11",
        "confidence": "reported",
        "text": (
            "From July 1, 2025, PIBOs must provide plastic packaging information "
            "via an on-pack barcode, QR code, or unique number, and notify the "
            "Central Pollution Control Board (CPCB) accordingly, under Rule 11 of "
            "the amended rules."
        ),
    },
    {
        "id": "kb007",
        "title": "March 2026 amendment: recycled content, Sellers, traceability, auditors",
        "citation": "Plastic Waste Management (Amendment) Rules, 2026 (notified 31 March 2026)",
        "confidence": "reported",
        "text": (
            "The Plastic Waste Management (Amendment) Rules, 2026, notified 31 "
            "March 2026 by the MoEFCC, introduce four significant changes: (1) "
            "mandatory recycled-content and reuse percentages for PIBOs, not just "
            "collection targets; (2) a new 'Sellers' category covering suppliers of "
            "raw plastic materials such as resins and pellets, who must now "
            "register and report sales so virgin plastic use can be tracked from "
            "the source; (3) mandatory QR codes or barcodes enabling real-time "
            "tracking of origin and recycled content across the value chain; and "
            "(4) Registered Environment Auditors as third-party verifiers, intended "
            "to eliminate paper-only compliance and fake certificates."
        ),
    },
    {
        "id": "kb008",
        "title": "Recycling/reuse targets timeline",
        "citation": "Reported industry summaries of PWM Rules targets",
        "confidence": "needs_verify",
        "text": (
            "Multiple industry sources state that PIBOs must recycle or reuse at "
            "least 70% of the plastic waste they generate by FY 2026-27, rising to "
            "100% by FY 2028-29. The exact year-by-year graduated schedule prior to "
            "2026-27, and whether targets differ by category (I vs II vs III), was "
            "NOT fully confirmed -- verify the precise schedule against the "
            "official CPCB target notification for the specific category before "
            "quoting a number to a client."
        ),
    },
    {
        "id": "kb009",
        "title": "EPR Certificates -- mechanism and pricing",
        "citation": "CPCB EPR Portal mechanics, reported market pricing",
        "confidence": "reported",
        "text": (
            "An EPR Certificate is a tradeable digital document issued by a "
            "CPCB-registered recycler confirming that a specific quantity of "
            "plastic waste, in a specific category, has been processed. PIBOs "
            "meet their annual obligation either by recycling their own waste or "
            "by purchasing EPR Certificates from registered recyclers or through a "
            "Producer Responsibility Organisation (PRO), directly via the CPCB "
            "portal marketplace. Reported market prices for these certificates "
            "range from roughly Rs 4,000 to Rs 20,000 per metric tonne, depending "
            "on the plastic category -- and certificates from non-compliant or "
            "unregistered recyclers do not count toward the legal obligation."
        ),
    },
    {
        "id": "kb010",
        "title": "Producer Responsibility Organisation (PRO)",
        "citation": "CPCB EPR framework",
        "confidence": "reported",
        "text": (
            "A Producer Responsibility Organisation (PRO) is a third-party entity "
            "registered with the CPCB that helps PIBOs meet their EPR obligations "
            "through organized waste collection and recycling networks, acting as "
            "an intermediary between brand owners and certified recyclers."
        ),
    },
    {
        "id": "kb011",
        "title": "Annual EPR return -- filing deadline",
        "citation": "CPCB EPR Portal filing requirements",
        "confidence": "needs_verify",
        "text": (
            "PIBOs must file an annual EPR return, commonly reported as due by "
            "September 30 for the preceding financial year. Missing this deadline "
            "is treated as zero fulfilment, meaning Environmental Compensation "
            "penalties apply to the FULL annual obligation, regardless of actual "
            "recycling performed. Always confirm the exact current-year deadline "
            "against the live CPCB portal notification, since filing dates can "
            "shift year to year."
        ),
    },
    {
        "id": "kb012",
        "title": "Registration process on the CPCB EPR portal",
        "citation": "CPCB EPR Portal process, reported by compliance-consultant sources",
        "confidence": "reported",
        "text": (
            "The reported registration flow is: (1) create an account on the CPCB "
            "EPR portal; (2) select the correct category -- Producer, Importer, or "
            "Brand Owner -- since choosing incorrectly is a common cause of "
            "rejection; (3) upload supporting documents (valid, unexpired consents "
            "are required); (4) declare plastic packaging data -- type, weight, "
            "annual estimate; (5) the application goes through CPCB review, which "
            "may raise queries that must be answered within a specified timeline; "
            "(6) once approved, the registration certificate is issued, with "
            "compliance continuing through annual return filings and yearly "
            "renewal."
        ),
    },
    {
        "id": "kb013",
        "title": "Penalties for non-compliance",
        "citation": "Environment (Protection) Act, 1986, as reported in compliance guides",
        "confidence": "reported",
        "text": (
            "Reported penalties for EPR non-compliance include: monetary fines "
            "starting around Rs 1 lakh plus Rs 5,000 per day of continued delay, "
            "escalating to Environmental Compensation (EC) of up to Rs 1 crore for "
            "major breaches such as missed recycling targets; operational "
            "shutdowns, where the CPCB can halt production or imports until "
            "compliance is restored; blacklisting from government tenders for 1 "
            "to 5 years; and, for willful evasion, imprisonment of up to 5 years "
            "under the Environment (Protection) Act, 1986."
        ),
    },
    {
        "id": "kb014",
        "title": "Real enforcement examples (for illustrating stakes, not legal precedent)",
        "citation": "News reporting on specific enforcement actions",
        "confidence": "reported",
        "text": (
            "Reported enforcement examples: Bharat Petroleum Corporation Limited "
            "(BPCL) was reportedly given a Rs 1 crore Environmental Compensation "
            "for EPR lapses in used-oil management, with operations paused for 30 "
            "days. A Delhi-based importer reportedly faced cumulative fines of "
            "Rs 19.82 crore across states for plastic waste non-compliance. A "
            "Karnataka firm reportedly lost Rs 20 crore in government contracts "
            "after a Rs 35 lakh Environmental Compensation penalty led to "
            "blacklisting. These are illustrative of enforcement severity, not a "
            "substitute for case-specific legal research."
        ),
    },
]
