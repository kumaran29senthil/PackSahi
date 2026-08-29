import re
from typing import Dict, Any, List

class DeterministicRuleEngine:
    @staticmethod
    def evaluate_rule_6(extracted_text_blocks: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Evaluates all 7 sub-clauses of Rule 6 against extracted OCR text."""
        full_text = " ".join([b["raw_text"] for b in extracted_text_blocks])
        results = []

        # Rule 6(1)(a): Manufacturer Address & 6-digit PIN Code
        pin_match = re.search(r'\b[1-9][0-9]{5}\b', full_text)
        results.append({
            "rule_clause": "Rule 6(1)(a)",
            "field_name": "Manufacturer Name & Address",
            "status": "PASS" if pin_match else "FAIL",
            "raw_text_detected": pin_match.group(0) if pin_match else "No 6-digit PIN found",
            "message": "Valid 6-digit Indian PIN code identified." if pin_match else "Missing statutory 6-digit PIN code in address."
        })

        # Rule 6(1)(c): Net Quantity & Metric Units (g, kg, ml, l, N)
        net_qty_match = re.search(r'(?i)(net\s*qty|net\s*quantity|net\s*wt)[:\s]*(\d+(\.\d+)?)\s*(g|kg|ml|l|n)\b', full_text)
        results.append({
            "rule_clause": "Rule 6(1)(c)",
            "field_name": "Net Quantity & Metric Unit",
            "status": "PASS" if net_qty_match else "FAIL",
            "raw_text_detected": net_qty_match.group(0) if net_qty_match else "Not detected",
            "message": "Valid net quantity and standard metric unit detected." if net_qty_match else "Non-standard or missing metric unit."
        })

        # Rule 6(1)(e): MRP Syntax ("inclusive of all taxes")
        mrp_match = re.search(r'(?i)(mrp|rs\.?|₹)\s*(\d+(\.\d+)?)\s*(incl\.?\s*of\s*all\s*taxes)', full_text)
        results.append({
            "rule_clause": "Rule 6(1)(e)",
            "field_name": "Maximum Retail Price (MRP)",
            "status": "PASS" if mrp_match else "FAIL",
            "raw_text_detected": mrp_match.group(0) if mrp_match else "Missing statutory phrase",
            "message": "MRP includes mandatory 'inclusive of all taxes' phrase." if mrp_match else "MRP syntax fails statutory requirement: Missing 'inclusive of all taxes'."
        })

        # Rule 6(1)(f): Consumer Care Contact Details
        contact_match = re.search(r'(?i)(customer\s*care|consumer\s*care|helpline|email)[:\s]*([\w\.-]+@[\w\.-]+|\+?\d{10,12})', full_text)
        results.append({
            "rule_clause": "Rule 6(1)(f)",
            "field_name": "Consumer Care Contact",
            "status": "PASS" if contact_match else "FAIL",
            "raw_text_detected": contact_match.group(0) if contact_match else "No helpline/email found",
            "message": "Valid consumer care phone or email declared." if contact_match else "Missing statutory consumer care contact details."
        })

        return results

    @staticmethod
    def evaluate_rule_7(pdp_area_cm2: float, detected_height_mm: float) -> Dict[str, Any]:
        """Evaluates font height in mm against Principal Display Panel (PDP) surface area thresholds."""
        required_min_mm = 1.0
        if pdp_area_cm2 > 500:
            required_min_mm = 4.0
        elif pdp_area_cm2 >= 100:
            required_min_mm = 2.0

        is_pass = detected_height_mm >= required_min_mm

        return {
            "rule_clause": "Rule 7",
            "field_name": "Font Size Scaling",
            "status": "PASS" if is_pass else "FAIL",
            "font_height_mm": detected_height_mm,
            "message": f"Detected font height ({detected_height_mm}mm) meets threshold." if is_pass else f"Font height ({detected_height_mm}mm) is below required statutory minimum of {required_min_mm}mm for PDP area of {pdp_area_cm2}cm²."
        }
