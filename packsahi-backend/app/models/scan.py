import uuid
from datetime import datetime
from sqlalchemy import Column, String, Float, DateTime, ForeignKey, Text, JSON
from sqlalchemy.orm import relationship
from app.core.database import Base

class ScanRecord(Base):
    __tablename__ = "scan_records"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    timestamp = Column(DateTime, default=datetime.utcnow)
    channel = Column(String(32), nullable=False)  # RETAIL_RAID, ECOM_SCRAPE, PREMARKET_AUDIT
    verdict = Column(String(16), nullable=False)  # PASS, FAIL, WARN
    overall_confidence = Column(Float, nullable=False)
    image_path = Column(String(255), nullable=False)
    dewarped_image_path = Column(String(255), nullable=True)
    package_width_mm_input = Column(Float, default=150.0)
    pdp_area_cm2 = Column(Float, nullable=True)
    evidence_hash = Column(String(64), nullable=False)  # SHA-256 Signature
    latitude = Column(Float, nullable=True)
    longitude = Column(Float, nullable=True)

    # Relationships
    violations = relationship("RuleViolation", back_populates="scan", cascade="all, delete-orphan")
    notices = relationship("FormANotice", back_populates="scan", cascade="all, delete-orphan")

class RuleViolation(Base):
    __tablename__ = "rule_violations"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    scan_id = Column(String(36), ForeignKey("scan_records.id"), nullable=False)
    rule_clause = Column(String(64), nullable=False)  # e.g., "Rule 6(1)(e)", "Rule 7"
    field_name = Column(String(64), nullable=False)
    status = Column(String(16), nullable=False)      # PASS, FAIL
    raw_text_detected = Column(Text, nullable=True)
    failure_reason = Column(Text, nullable=True)
    font_height_mm = Column(Float, nullable=True)
    bbox_json = Column(JSON, nullable=True)           # [x, y, w, h]

    scan = relationship("ScanRecord", back_populates="violations")

class FormANotice(Base):
    __tablename__ = "forma_notices"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    scan_id = Column(String(36), ForeignKey("scan_records.id"), nullable=False)
    notice_number = Column(String(64), unique=True, nullable=False)
    issued_at = Column(DateTime, default=datetime.utcnow)
    compounding_fee_inr = Column(Float, default=0.0)   # Rule 32 compounding fee
    status = Column(String(32), default="ISSUED")       # ISSUED, PAID, COURT_SUMMONS
    pdf_path = Column(String(255), nullable=False)

    scan = relationship("ScanRecord", back_populates="notices")
