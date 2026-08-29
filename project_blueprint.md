# PackSahi: System Architecture & Master Feature Blueprint
**Problem Statement ID:** SIH26034
**Problem Statement Title:** Software System to check compliance of Packaged Commodities under Legal Metrology (Packaged Commodities) Rules, 2011 by scanning products, images and labels.
**Nodal Ministry:** Department of Consumer Affairs (DoCA), Ministry of Consumer Affairs, Food & Public Distribution, Govt. of India.
**Team Name:** InnovX

## 1. Executive Summary & Problem-Solution Fit
**The Problem**
- **Manual Bottlenecks:** Manual Legal Metrology inspections take 15–30 minutes per product, leaving millions of physical packages and fast-moving e-commerce listings un-audited.
- **Detection Challenges:** Existing systems fail to detect missing declarations, incorrect MRP formatting, non-standard units, unreadable text, and curved/reflective label surfaces.
- **Enforcement Delays:** Paper-based inspection trails result in slow fine recovery and inadequate digital proof overlays for court proceedings.

**The PackSahi Solution**
- An AI-powered, deterministic Legal Metrology compliance system designed for DoCA administrators, field inspectors, e-commerce marketplaces, and brand QA teams.
- Combines OpenCV 3D cylindrical label dewarping and PaddleOCR with a zero-hallucination deterministic legal engine to enforce Rules 6, 7, 9, 18, and 32 across physical stores and digital marketplaces.

## 2. Comprehensive End-to-End Feature Breakdown (A to H)

### A. Computer Vision & Preprocessing Features
- **Image Quality Normalization:** Auto-adjusts contrast, grayscaling, and adaptive thresholding for noisy retail photos.
- **OpenCV Auto-Deskewing:** Detects packaging orientation and auto-aligns tilted label angles.
- **3D Cylindrical Surface Unwarping:** Flattens curved packaging labels (cans, bottles, jars) using point-cloud algorithms prior to OCR text extraction.
- **Multi-Image Fusion:** Merges separate static packaging photos and dynamic inkjet stamp photos (MRP, Batch, Expiry) into a unified inspection record.
- **Pixel-to-Millimeter Spatial Calibration Engine:** Calculates real-world text height ($\text{mm}$) using image resolution and user reference inputs.

### B. Deterministic Legal Engine (Rules 6, 7, 9, 18 & 32)
**Rule 6: Statutory Mandatory Declarations Module**
- **Rule 6(1)(a):** Validates Manufacturer/Packer/Importer Name, Address, and 6-digit Indian PIN Code.
- **Rule 6(1)(b):** Extracts and verifies the Generic/Common Commodity Name.
- **Rule 6(1)(c):** Checks Net Quantity & mandatory metric unit formatting ($\text{g}$, $\text{kg}$, $\text{ml}$, $\text{l}$, $\text{N}$).
- **Rule 6(1)(d):** Parses Month & Year of Manufacture/Packing/Import in standard $\text{MM/YYYY}$ format.
- **Rule 6(1)(e):** Validates MRP syntax to ensure it strictly includes "inclusive of all taxes".
- **Rule 6(1)(f):** Checks mandatory Consumer Care details (valid phone number or email).
- **Rule 6(1)(g):** Verifies Country of Origin for imported items.

**Rule 7: Font Height Threshold Engine**
- Compares calculated text height ($\text{mm}$) against mandatory Principal Display Panel (PDP) area tables ($\text{PDP} < 100\text{ cm}^2 \rightarrow \ge 1.0\text{ mm}$; $100\text{--}500\text{ cm}^2 \rightarrow \ge 2.0\text{ mm}$; $> 500\text{ cm}^2 \rightarrow \ge 4.0\text{ mm}$).

**Rule 9: Principal Display Panel (PDP) Geometry Engine**
- Computes total canvas dimensions and validates whether statutory declarations occupy the mandatory PDP geometric surface area ratio.

**Rule 18: Overcharging & Pricing Protection Engine**
- Audits retail and online seller listings to ensure displayed checkout prices do not exceed declared package Maximum Retail Prices (MRP).

**Rule 32: Statutory Compounding Fee Engine**
- Auto-computes compounding penalty fee structures based on statutory violation categories and repeat offender history.

### C. E-Commerce Monitoring & Scraping Features
- **Marketplace Listing Scraper:** Scrapes product display card images and text metadata continuously from quick-commerce and marketplace portals (Blinkit, Amazon, Zepto).
- **Digital Violation Detector:** Identifies online product listings that obscure, omit, or misrepresent mandatory packaging declarations in display images.
- **Push Auto Takedown API:** Generates and dispatches automated API listing takedown flags to marketplace seller APIs to suspend non-compliant product listings in real time.

### D. Legal Evidence & Court-Ready Notice Features
- **Form A Legal Seizure Notice Generator:** Auto-drafts official government Form A legal seizure notices upon detecting retail violations.
- **Bounding-Box Proof Overlay:** Renders visual green (PASS) and red (FAIL) bounding boxes over product images in generated PDFs.
- **Geotag & Timestamp Stamp:** Embeds GPS location coordinates and exact time metrics directly into legal inspection records.
- **SHA-256 Cryptographic Hashing:** Encrypts inspection data, timestamps, and GPS coordinates into tamper-proof legal evidence.
- **Post-Reporting Resolution Loop:** Tracks case states (Paid & Corrected $\rightarrow$ Case Closed; Unpaid $\rightarrow$ Court Summons).

### E. Brand Pre-Market Clearance Features
- **Pre-Print Vector Artwork Upload:** Accepts vector design files ($\text{PDF}/\text{AI}$) from FMCG manufacturers before mass physical factory printing.
- **Layout Coordinate Checker:** Simulates Rule 6, 7, and 9 audits on packaging artwork, highlighting exact canvas coordinates that violate font size or margin requirements.
- **Pre-Market Certificate Generator:** Issues downloadable compliance clearance certificates for packaging designs that pass simulation.

### F. Database, Storage & Offline Features
- **Central DoCA Enforcement Repository:** Tracks state-wide inspection trends, heatmaps, court backlogs, and historical scan retrievals.
- **Offline-First SQLite Local Buffer:** Saves inspection scans locally on field devices when internet connectivity is lost, auto-syncing when network connectivity restores.
- **Real-Time Data Search & Indexing:** Filter historical scans by Brand Name, Batch Number, Store Location, Date, or Verdict (PASS/FAIL).

### G. User Portal & Dashboard Features
- **Interactive Image Canvas Overlay:** Renders interactive green (PASS) and red (FAIL) SVG bounding boxes directly over packaging label images.
- **National Compliance Dashboard:** Displays metrics including total scans conducted, non-compliance rates, violation type progress bars, and state-wide enforcement heatmaps.
- **Grievance Ticket Integrator:** Enables direct submission of non-compliance tickets to the National Consumer Helpline (NCH).

### H. Dynamic 4-Role Access Control (RBAC) System
- **Consumer / Citizen Persona:** Mobile scan view, simplified pass/fail badges, public scan repository search, and one-tap grievance filing to National Consumer Helpline (NCH).
- **DoCA Field Inspector Persona:** Offline retail raid scanner, spatial scale input, Form A seizure notice drafting, and inspection history.
- **District Controller / Admin Persona:** District raid tracking, violation heatmaps, e-commerce audit streams, and Rule 32 compounding approvals.
- **Brand QA Lead / Manufacturer Persona:** Pre-print packaging artwork auditor, notice alert receiver, and compounding fee payment portal.

## 3. Technology Stack Summary
- **Frontend:** React.js (Web Command Portal), Flutter (Offline Mobile App), Tailwind CSS.
- **Backend:** FastAPI (Microservices), Express.js / Node.js.
- **Database:** PostgreSQL (Central Data Warehouse), SQLite (On-Device Inspector Sync).
- **AI, CV & NLP Core:** OpenCV (3D Surface Dewarping), PaddleOCR (Text Extraction), SpaCy (NER Statutory Parsing), SpatialVLM (Pixel-to-MM Metrics).
