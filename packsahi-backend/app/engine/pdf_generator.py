import os
import hashlib
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors

class PDFGenerator:
    @staticmethod
    def generate_form_a_notice(notice_data: dict, output_filepath: str) -> str:
        """Generates a court-ready Form A Legal Seizure Notice PDF with SHA-256 evidence signature."""
        doc = SimpleDocTemplate(output_filepath, pagesize=letter)
        styles = getSampleStyleSheet()
        story = []

        # Title Header
        title_style = ParagraphStyle(
            'GovHeader',
            parent=styles['Heading1'],
            fontName='Helvetica-Bold',
            fontSize=14,
            alignment=1, # Center
            textColor=colors.HexColor('#0F172A')
        )
        story.append(Paragraph("DEPARTMENT OF CONSUMER AFFAIRS (DoCA)", title_style))
        story.append(Paragraph("GOVERNMENT OF INDIA - LEGAL METROLOGY DIVISION", title_style))
        story.append(Spacer(1, 10))
        story.append(Paragraph("<b>FORM A: LEGAL SEIZURE NOTICE</b><br/>[Issued Under Section 15 & Rule 32]", title_style))
        story.append(Spacer(1, 15))

        # Metadata Table
        meta_data = [
            ["Inspection ID:", notice_data["scan_id"], "Date/Time:", notice_data["timestamp"]],
            ["Location:", notice_data.get("location_name", "Durg, CG"), "GPS Geotag:", f"{notice_data.get('lat', 21.19)}° N, {notice_data.get('lng', 81.28)}° E"]
        ]
        meta_table = Table(meta_data, colWidths=[100, 150, 100, 150])
        meta_table.setStyle(TableStyle([
            ('BACKGROUND', (0,0), (-1,-1), colors.HexColor('#F8FAFC')),
            ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor('#CBD5E1')),
            ('FONTNAME', (0,0), (-1,-1), 'Helvetica'),
            ('FONTSIZE', (0,0), (-1,-1), 9),
        ]))
        story.append(meta_table)
        story.append(Spacer(1, 15))

        # Violation Details Header
        story.append(Paragraph("<b>STATUTORY VIOLATIONS DETECTED:</b>", styles['Heading2']))
        
        violation_table_data = [["Rule Clause", "Field Name", "Detected Text / Finding"]]
        for v in notice_data["violations"]:
            violation_table_data.append([v["rule_clause"], v["field_name"], v["failure_reason"]])

        v_table = Table(violation_table_data, colWidths=[100, 130, 270])
        v_table.setStyle(TableStyle([
            ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#EF4444')),
            ('TEXTCOLOR', (0,0), (-1,0), colors.white),
            ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
            ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor('#E2E8F0')),
            ('FONTSIZE', (0,0), (-1,-1), 8),
        ]))
        story.append(v_table)
        story.append(Spacer(1, 20))

        # Cryptographic Hash Evidence Stamp
        raw_hash_str = f"{notice_data['scan_id']}-{notice_data['timestamp']}-{notice_data.get('lat')}"
        sha256_hash = hashlib.sha256(raw_hash_str.encode()).hexdigest()
        
        hash_style = ParagraphStyle('HashStyle', fontName='Courier', fontSize=7, textColor=colors.HexColor('#475569'))
        story.append(Paragraph(f"<b>Cryptographic SHA-256 Proof Signature:</b> {sha256_hash}", hash_style))

        # Build Document
        doc.build(story)
        return sha256_hash
