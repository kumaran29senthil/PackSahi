from fastapi import APIRouter, Depends, UploadFile, File, Form, HTTPException
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.engine.cv_engine import CVEngine
from app.engine.nlp_rules import DeterministicRuleEngine
import uuid
import datetime

router = APIRouter()

@router.post("/")
async def process_scan(
    image: UploadFile = File(...),
    package_width_mm: float = Form(150.0),
    db: Session = Depends(get_db)
):
    try:
        # Read image bytes
        image_bytes = await image.read()
        
        # 1. Preprocess & Dewarp (Commented out full OpenCV logic for immediate API testing)
        # enhanced_img = CVEngine.preprocess_image(image_bytes)
        # dewarped_img = CVEngine.dewarp_cylindrical_surface(enhanced_img)
        
        # 2. Extract Text & Spatial Bboxes (Mocking PaddleOCR output for now)
        extracted_text_blocks = [
            {"raw_text": "MRP: Rs. 150.00 (inclusive of all taxes)", "bbox": [10, 10, 100, 20]},
            {"raw_text": "Net Qty: 500 ml", "bbox": [10, 30, 80, 20]},
            {"raw_text": "Customer Care: care@innovx.com", "bbox": [10, 50, 150, 20]},
            {"raw_text": "Pin Code: 400001", "bbox": [10, 70, 100, 20]}
        ]
        
        # 3. Validate Rules
        rule_6_results = DeterministicRuleEngine.evaluate_rule_6(extracted_text_blocks)
        
        # Mocking PDP calculation
        pdp_area_cm2 = 250.0 
        detected_height_mm = 2.5
        rule_7_results = DeterministicRuleEngine.evaluate_rule_7(pdp_area_cm2, detected_height_mm)
        
        all_violations = rule_6_results + [rule_7_results]
        
        # Calculate Verdict based on violations
        failed_rules = [v for v in all_violations if v["status"] == "FAIL"]
        verdict = "FAIL" if failed_rules else "PASS"
        
        # 4. Return Final Decision
        return {
            "scan_id": str(uuid.uuid4()),
            "timestamp": datetime.datetime.utcnow().isoformat(),
            "verdict": verdict,
            "violations": all_violations,
            "message": "Scan processed successfully"
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
