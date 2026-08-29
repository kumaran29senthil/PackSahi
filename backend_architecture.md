# PackSahi: End-to-End Backend Architecture & Microservices Documentation

## 1. Architecture Overview & Core Stack
The PackSahi backend is a microservice-driven, high-throughput asynchronous execution layer built using Python FastAPI and Node.js/Express.js microservices. It orchestrates image preprocessing, 3D surface dewarping, spatial text extraction, deterministic legal validation (Rules 6, 7, 9, 18, and 32), PDF notice generation, and automated e-commerce web scrapers.

**Tech Stack Specifications**
- **Primary Framework:** FastAPI (Python 3.11) for CV, OCR, NLP, and high-concurrency async REST APIs.
- **Secondary Orchestration:** Node.js / Express.js microservice for webhook handling and real-time socket connections.
- **Database Systems:**
  - **PostgreSQL:** Production central data warehouse (Stores scans, rule checks, audit trails, and fine records).
  - **SQLite:** Embedded lightweight database used for local offline field-officer mobile synchronization.
- **Computer Vision & OCR Libraries:** OpenCV (opencv-python-headless), NumPy, PaddleOCR, PyTesseract, SpaCy (en_core_web_sm).
- **PDF Engine:** ReportLab (Python) for geotagged, cryptographically signed legal notice generation.
- **Web Scraping Engine:** Playwright / Selenium headless browser automation.

## 2. Backend Directory Structure
```text
packsahi-backend/
├── app/
│   ├── api/
│   │   ├── v1/
│   │   │   ├── endpoints/
│   │   │   │   ├── scan.py          # POST /api/v1/scan (Main image processing pipeline)
│   │   │   │   ├── scans.py         # GET /api/v1/scans (Repository search & filtering)
│   │   │   │   ├── ecommerce.py     # POST /api/v1/ecommerce/takedown (Webhook triggers)
│   │   │   │   ├── brand.py          # POST /api/v1/brand/clearance (Vector design audits)
│   │   │   │   └── pdf.py            # GET /api/v1/scans/{id}/report.pdf (Form A generator)
│   │   │   └── router.py            # API V1 router aggregation
│   ├── core/
│   │   ├── config.py                # Environment variables & system configuration
│   │   ├── database.py              # SQLAlchemy engine & session manager
│   │   └── security.py              # Cryptographic SHA-256 hash stamp utilities
│   ├── engine/
│   │   ├── cv_engine.py             # OpenCV CLAHE, deskewing & 3D cylindrical dewarping
│   │   ├── ocr_engine.py            # PaddleOCR extraction & spatial bounding box math
│   │   ├── nlp_rules.py             # SpaCy matcher & RegEx deterministic rule engine
│   │   ├── pdf_generator.py         # ReportLab Form A Seizure Notice PDF builder
│   │   └── scraper.py               # Playwright headless e-commerce audit scraper
│   ├── models/
│   │   ├── scan.py                  # SQLAlchemy model for scans
│   │   ├── violation.py             # SQLAlchemy model for rule violations
│   │   └── notice.py                # SQLAlchemy model for Form A legal notices
│   ├── schemas/
│   │   ├── scan.py                  # Pydantic schemas for request/response validation
│   │   └── ecommerce.py             # Pydantic schemas for takedown payloads
│   └── main.py                      # FastAPI application entrypoint & CORS setup
├── alembic/                         # Database migration scripts
├── tests/                           # Unit & integration test suites
├── Dockerfile                       # Container deployment definition
├── requirements.txt                 # Backend Python dependencies
└── README.md
```

## 6. End-to-End Execution Flow
```text
┌───────────────────────────┐
│ React UI / Mobile Client  │
└─────────────┬─────────────┘
              │ 1. POST /api/v1/scan (Image + package_width_mm)
              ▼
┌───────────────────────────┐
│ FastAPI Input Controller  │
└─────────────┬─────────────┘
              │ 2. Preprocess & 3D Dewarp (OpenCV)
              ▼
┌───────────────────────────┐
│ CV & Dewarping Microservice│
└─────────────┬─────────────┘
              │ 3. Extract Text & Spatial Bboxes [x, y, w, h]
              ▼
┌───────────────────────────┐
│ PaddleOCR Text Extractor  │
└─────────────┬─────────────┘
              │ 4. Validate Rules 6, 7, 9, 18 (Regex/SpaCy + Spatial Scaling)
              ▼
┌───────────────────────────┐
│ Deterministic Rule Engine │
└─────────────┬─────────────┘
              │ 5. Compile Verdict (PASS/FAIL) & SHA-256 Stamp
              ▼
┌───────────────────────────┐
│ Database & ReportLab PDF  │
└─────────────┬─────────────┘
              │ 6. Return JSON Response + Form A PDF Binary Download Link
              ▼
┌───────────────────────────┐
│ React UI / Mobile Client  │
└───────────────────────────┘
```
