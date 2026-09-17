"""
Knowledge base for the EPR Compliance Copilot.

Ground truth sourced from official statutory texts and notifications:
  - Plastic Waste Management Rules, 2016 (MoEFCC)
  - Guidelines on Extended Producer Responsibility for Plastic Packaging (Schedule II),
    notified via MoEFCC Notification G.S.R. 133(E) dated 16 February 2022
  - PWM (Amendment) Rules, 2024 & 2025 (Rule 11 Labeling Mandates)
  - PWM (Amendment) Rules, 2026 (Sellers, Traceability, Registered Environment Auditors)
  - CPCB Centralized EPR Portal Operational Circulars

Confidence tags:
  - "verified"     -> Transcribed directly from official Gazette notifications / CPCB guidelines.
  - "reported"     -> Multiple consistent official reports and legal industry summaries.
  - "needs_verify" -> Transitional dates or pending portal notifications.
"""

KNOWLEDGE_BASE = [
    {
        "id": "kb001",
        "title": "EPR Statutory Framework Origin & PIBO Scope",
        "citation": "Plastic Waste Management Rules, 2016; MoEFCC Notification G.S.R. 133(E) (Schedule II)",
        "confidence": "verified",
        "text": (
            "India's Extended Producer Responsibility (EPR) for plastic packaging is governed "
            "under Schedule II of the Plastic Waste Management Rules, 2016 (as amended in 2022, 2024, "
            "and 2026). EPR shifts lifecycle responsibility for post-consumer plastic packaging "
            "waste onto four categories of entities: Producers (P), Importers (I), Brand Owners (BO), "
            "collectively known as PIBOs, and Plastic Waste Processors (PWPs). Entities must obtain "
            "registration on the centralized CPCB portal before selling or importing any packaged product."
        ),
    },
    {
        "id": "kb002",
        "title": "Obliged Entities: Producer, Importer, Brand Owner, and Sellers",
        "citation": "PWM Amendment Rules 2022 (Clause 4) & PWM Amendment Rules 2026",
        "confidence": "verified",
        "text": (
            "Under the CPCB EPR framework: (1) 'Producer' means a person engaged in the manufacture "
            "or import of carry bags or multi-layered packaging or plastic sheets or like, and "
            "includes persons using plastic packaging for packaging goods. (2) 'Importer' means a person "
            "who imports plastic packaging products or products with plastic packaging. (3) 'Brand Owner' "
            "means a person or company who sells any commodity under a registered brand label or trade mark, "
            "including e-commerce marketplaces and modern trade retailers. (4) Under the 2026 amendment, "
            "'Sellers' of raw virgin plastic materials (granules, resins, pellets) must also register on the "
            "portal to track virgin resin flow from the source."
        ),
    },
    {
        "id": "kb003",
        "title": "The Four Official Packaging Categories (Categories I, II, III, IV)",
        "citation": "Schedule II, Clause 5.1 of PWM Rules (MoEFCC Notification Feb 16, 2022)",
        "confidence": "verified",
        "text": (
            "Schedule II formally establishes four distinct plastic packaging categories: "
            "Category I: Rigid plastic packaging (containers, bottles, jars, crates, buckets, caps). "
            "Category II: Flexible plastic packaging of single layer or multilayer (more than one layer with "
            "different types of plastic), plastic sheets or covers, carry bags, sachets or pouches where "
            "all layers are made of plastic. "
            "Category III: Multilayered plastic packaging (MLP) having at least one layer of plastic and at "
            "least one layer of material other than plastic (such as paper, aluminium foil, cardboard, etc.). "
            "Category IV: Plastic sheets or carry bags made of compostable plastics conforming to IS/ISO 17088."
        ),
    },
    {
        "id": "kb004",
        "title": "Category II (Flexible) vs Category III (Multi-layered MLP) Boundary",
        "citation": "Schedule II, Clause 5.1 (Category II & III Definitions)",
        "confidence": "verified",
        "text": (
            "The statutory legal boundary between Category II and Category III is strictly determined by "
            "layer composition: If a multilayer packaging consists EXCLUSIVELY of plastic polymers "
            "(e.g., LDPE laminated with HDPE or BOPP), it falls under Category II (Flexible). If the packaging "
            "contains at least ONE NON-PLASTIC layer (e.g., aluminium foil in chip pouches, paperboard in "
            "beverage cartons, metallized paper), it is classified as Category III (Multilayered Plastic Packaging). "
            "Recycling targets and credit trading prices differ significantly between these two categories."
        ),
    },
    {
        "id": "kb005",
        "title": "Category IV Compostable Plastic Requirements",
        "citation": "Schedule II, Clause 5.1 (Category IV) & PWM Rule 4(h)",
        "confidence": "verified",
        "text": (
            "Category IV covers packaging and carry bags made exclusively from compostable plastics. "
            "To qualify, manufacturers and brand owners must obtain a certificate from the Central "
            "Pollution Control Board (CPCB) certifying compliance with Indian Standard IS/ISO 17088 "
            "('Specifications for Compostable Plastics'). Compostable packaging has a 100% end-of-life "
            "disposal mandate via industrial composting facilities rather than standard mechanical recycling."
        ),
    },
    {
        "id": "kb006",
        "title": "Annual EPR Collection Obligation Formula",
        "citation": "Schedule II, Clause 7 (EPR Target Calculation)",
        "confidence": "verified",
        "text": (
            "The EPR collection obligation for a PIBO is calculated based on the average weight of plastic "
            "packaging introduced into the market in the preceding two financial years (plus imported plastic). "
            "The graduated national collection targets are: 35% for FY 2021-22, 70% for FY 2022-23, and "
            "100% for FY 2023-24 and all subsequent financial years (including FY 2024-25, 2025-26, 2026-27 onwards). "
            "PIBOs must fulfill 100% of their introduced plastic packaging weight through recycling or credits."
        ),
    },
    {
        "id": "kb007",
        "title": "Mandatory Recycling Target Schedule (% of EPR Obligation)",
        "citation": "Schedule II, Clause 7.2 (Recycling Targets by Category)",
        "confidence": "verified",
        "text": (
            "Out of the total EPR obligation, PIBOs must ensure minimum mechanical recycling by category: "
            "For Category I (Rigid): 50% in FY 2024-25, 60% in FY 2025-26, 70% in FY 2026-27, and 80% in FY 2027-28 onwards. "
            "For Category II (Flexible): 30% in FY 2024-25, 40% in FY 2025-26, 50% in FY 2026-27, and 60% in FY 2027-28 onwards. "
            "For Category III (MLP): 30% in FY 2024-25, 40% in FY 2025-26, 50% in FY 2026-27, and 60% in FY 2027-28 onwards. "
            "Any leftover obligation not capable of recycling must go to authorized End-of-Life disposal "
            "(Waste-to-Energy, cement co-processing, or road construction)."
        ),
    },
    {
        "id": "kb008",
        "title": "Mandatory Use of Recycled Plastic Content (Schedule II, Clause 7.3)",
        "citation": "Schedule II, Clause 7.3 & PWM Amendment 2026",
        "confidence": "verified",
        "text": (
            "Brand Owners and Producers must incorporate a statutory minimum percentage of recycled plastic "
            "content in their packaging: "
            "Category I (Rigid): 30% in FY 2025-26, 40% in FY 2026-27, 50% in FY 2027-28, and 60% in FY 2028-29 onwards. "
            "Category II (Flexible): 10% in FY 2025-26, 20% in FY 2026-27, and 30% in FY 2027-28 onwards. "
            "Category III (MLP): 5% in FY 2025-26, and 10% in FY 2026-27 onwards. "
            "Failure to meet recycled content thresholds is independently penalized under Environmental Compensation."
        ),
    },
    {
        "id": "kb009",
        "title": "EPR Certificates, Trading Portal & Market Pricing",
        "citation": "CPCB EPR Portal Guidelines & Trading Mechanism",
        "confidence": "reported",
        "text": (
            "PIBOs satisfy their obligation by generating recycling credits or buying digital EPR Certificates "
            "issued online by CPCB-registered Plastic Waste Processors (PWPs) via the centralized portal marketplace. "
            "Certificates are category-specific: Category I certificates cannot be used to offset Category II or III "
            "obligations. Market prices fluctuate based on category complexity: Category I typically trades at "
            "Rs 3,500 - Rs 8,000 per MT; Category II trades at Rs 6,000 - Rs 14,000 per MT; Category III trades at "
            "Rs 8,000 - Rs 20,000 per MT. Non-registered recycler certificates are void and subject to audit cancellation."
        ),
    },
    {
        "id": "kb010",
        "title": "Producer Responsibility Organisation (PRO) Role & Limits",
        "citation": "Schedule II, Clause 12 (Role of PRO)",
        "confidence": "verified",
        "text": (
            "A Producer Responsibility Organisation (PRO) may be engaged by PIBOs to assist with collection, "
            "logistics, and recycler coordination. However, under statutory rules, the legal liability for "
            "compliance and filing remains solely with the PIBO. A PRO cannot register on behalf of a PIBO as the "
            "obligated entity, nor can contractual indemnity protect a PIBO from CPCB prosecution or fines."
        ),
    },
    {
        "id": "kb011",
        "title": "Annual EPR Return Filing Deadlines & Extension Circulars",
        "citation": "Schedule II, Clause 11.3 & CPCB Filing Circulars",
        "confidence": "verified",
        "text": (
            "Under statutory Rule 11.3, PIBOs must file an Annual EPR Return for the preceding financial year "
            "on the CPCB portal by June 30. In practice, CPCB has issued periodic extension circulars extending "
            "the deadline to September 30 or October 31 for specific portal verification windows. "
            "Filing an annual return requires audited procurement invoices, category-wise production/import figures, "
            "and matched EPR certificate numbers. Failure to file on time triggers automatic notice issuance."
        ),
    },
    {
        "id": "kb012",
        "title": "Mandatory QR Code and Barcode Labeling Mandate (Rule 11)",
        "citation": "PWM (Amendment) Rules, 2025, Rule 11 & March 2026 Notification",
        "confidence": "verified",
        "text": (
            "Under Rule 11 of the Plastic Waste Management Rules, all PIBOs must print a scannable on-pack "
            "QR code, barcode, or unique digital identifier on each packaging unit. The code must encode: "
            "(1) CPCB EPR Registration number, (2) Plastic packaging category (Cat I/II/III/IV), (3) Virgin vs recycled "
            "plastic percentage, and (4) Recycler/Manufacturer credentials. Enforcement commenced July 1, 2025."
        ),
    },
    {
        "id": "kb013",
        "title": "Environmental Compensation (EC) Regime & Refund Formula",
        "citation": "Schedule II, Clause 10 & Environment (Protection) Act, 1986",
        "confidence": "verified",
        "text": (
            "Under Section 15 of the EPA 1986 and Schedule II Clause 10, CPCB levies Environmental Compensation (EC) "
            "on non-compliant entities. Crucially, payment of EC does NOT waive the EPR target: unfulfilled targets "
            "carry forward for up to three consecutive years. If the deficit target is fulfilled: within 1 year, "
            "85% of the levied EC is refunded; within 2 years, 60% is refunded; within 3 years, 30% is refunded. "
            "After 3 years, the entire compensation is permanently forfeited to the National Environmental Relief Fund."
        ),
    },
    {
        "id": "kb014",
        "title": "Penalties, Plant Closures and Registered Environmental Auditors",
        "citation": "PWM Amendment 2026 & EPA 1986 Section 15",
        "confidence": "verified",
        "text": (
            "Penalties for willful evasion, fraudulent EPR certificates, or operating without CPCB registration include: "
            "(1) Monetary EC fines typically assessed at Rs 5,000 per MT of unfulfilled obligation plus daily delay fines; "
            "(2) Revocation of Consent to Operate (CTO) and customs clearance seizure for importers; (3) Mandatory audit "
            "inspections by CPCB-empanelled Registered Environment Auditors (introduced in March 2026 amendment); and "
            "(4) Criminal prosecution under Section 15 of EPA 1986 with imprisonment up to 5 years for repeated defiance."
        ),
    },
    {
        "id": "kb015",
        "title": "EPR for Packaging Rules, 2024: Non-Plastic Expansion (Effective April 2026)",
        "citation": "Environment Protection (EPR for Packaging) Rules, 2024",
        "confidence": "verified",
        "text": (
            "The Environment Protection (EPR for Packaging) Rules, 2024 expand EPR obligations beyond plastics. "
            "Effective April 1, 2026, brand owners and manufacturers packaging goods in paper, glass, and metal "
            "must register and report on a unified portal. Separate EPR frameworks also apply to scrap non-ferrous "
            "metals (copper, aluminium, zinc) and construction/demolition waste, creating a unified industrial packaging regime."
        ),
    },
    {
        "id": "kb016",
        "title": "CPCB EPR Portal Step-by-Step Registration Checklist",
        "citation": "CPCB SOP for PIBO Registration (Form I)",
        "confidence": "verified",
        "text": (
            "PIBO registration on the centralized CPCB portal requires: (1) Company PAN, GST, and CIN; "
            "(2) Valid Consent to Establish (CTE) and Consent to Operate (CTO) issued by State Pollution Control Board "
            "(SPCB/PCC) for production facilities; (3) IEC (Import Export Code) for Importers; (4) Process flow diagrams "
            "and declared packaging specifications; (5) District Industries Centre (DIC) / MSME registration if claiming "
            "small-scale status. Operating without registration attracts immediate customs holds and portal blacklisting."
        ),
    },
]
