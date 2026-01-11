from flask import Flask, request, jsonify, render_template_string, send_file
from flask_cors import CORS
import hashlib
import datetime
import json
import os
from pathlib import Path
from io import BytesIO
from reportlab.lib.pagesizes import letter, A4
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, PageBreak
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT

app = Flask(__name__)
CORS(app)

# Database simulation (in production, use PostgreSQL/MongoDB)
EVIDENCE_DB = {}
CHAIN_OF_CUSTODY = {}
MULTI_EVIDENCE_CASES = {}
AI_DETECTION_RESULTS = {}

# ============ UTILITY FUNCTIONS ============

def generate_hash(file_bytes):
    """Generate SHA-256 hash of file"""
    sha256 = hashlib.sha256()
    sha256.update(file_bytes)
    return sha256.hexdigest()

def calculate_pre_entry_risk(source_type, metadata=None):
    """Enhanced risk calculation with metadata analysis"""
    source_type = source_type.lower()
    
    base_risk = {
        "cctv": 10,
        "official cctv": 5,
        "dashcam": 25,
        "mobile": 50,
        "phone": 50,
        "forwarded": 80,
        "unknown": 90
    }.get(source_type, 70)
    
    # Adjust risk based on metadata
    if metadata:
        if not metadata.get("gps_location"):
            base_risk += 10
        if not metadata.get("device_serial"):
            base_risk += 5
        if metadata.get("edited"):
            base_risk += 30
    
    # Convert to risk level
    if base_risk < 20:
        return "LOW"
    elif base_risk < 40:
        return "MEDIUM"
    elif base_risk < 60:
        return "HIGH"
    else:
        return "VERY HIGH"

def detect_ai_manipulation(file_bytes, filename):
    """Simulate AI manipulation detection"""
    # In production, integrate real AI models (e.g., CNN-based deepfake detection)
    file_hash = generate_hash(file_bytes)
    
    # Simulate detection based on file characteristics
    risk_score = (sum(file_hash.encode()) % 100) / 100
    
    return {
        "is_manipulated": risk_score > 0.7,
        "confidence": round(risk_score * 100, 2),
        "manipulation_type": "deepfake" if risk_score > 0.85 else "potential_edit" if risk_score > 0.7 else "none",
        "analysis_timestamp": datetime.datetime.now().isoformat()
    }

def add_to_chain_of_custody(evidence_id, action, user, details=""):
    """Add entry to chain of custody"""
    if evidence_id not in CHAIN_OF_CUSTODY:
        CHAIN_OF_CUSTODY[evidence_id] = []
    
    entry = {
        "timestamp": datetime.datetime.now().isoformat(),
        "action": action,
        "user": user,
        "details": details,
        "ip_address": request.remote_addr
    }
    
    CHAIN_OF_CUSTODY[evidence_id].append(entry)
    return entry

# ============ API ENDPOINTS ============

@app.route("/")
def home():
    """Serve the frontend HTML"""
    html_path = Path(__file__).parent / "templates" / "frontend.html"
    with open(html_path, 'r', encoding='utf-8') as f:
        return f.read()

@app.route("/register", methods=["POST"])
def register_evidence():
    """Register new evidence with full metadata"""
    file = request.files.get("file")
    evidence_id = request.form.get("evidence_id")
    source_type = request.form.get("source_type", "UNKNOWN")
    uploader_name = request.form.get("uploader_name", "Anonymous")
    case_number = request.form.get("case_number", "")
    
    if not file or not evidence_id:
        return jsonify({"error": "Missing file or evidence ID"}), 400
    
    # Check if evidence already exists
    if evidence_id in EVIDENCE_DB:
        return jsonify({"error": "Evidence ID already exists"}), 409
    
    # Read file and generate hash
    file_bytes = file.read()
    file_hash = generate_hash(file_bytes)
    
    # Extract metadata (simulate - in production, use EXIF/metadata libraries)
    metadata = {
        "filename": file.filename,
        "size_bytes": len(file_bytes),
        "upload_timestamp": datetime.datetime.now().isoformat(),
        "gps_location": request.form.get("gps_location"),
        "device_serial": request.form.get("device_serial"),
        "edited": request.form.get("edited", "false") == "true"
    }
    
    # Calculate risk
    risk = calculate_pre_entry_risk(source_type, metadata)
    
    # AI manipulation detection
    ai_result = detect_ai_manipulation(file_bytes, file.filename)
    AI_DETECTION_RESULTS[evidence_id] = ai_result
    
    # Store evidence
    EVIDENCE_DB[evidence_id] = {
        "hash": file_hash,
        "source_type": source_type,
        "uploader_name": uploader_name,
        "case_number": case_number,
        "metadata": metadata,
        "risk": risk,
        "registration_timestamp": datetime.datetime.now().isoformat(),
        "ai_detection": ai_result
    }
    
    # Add to chain of custody
    add_to_chain_of_custody(
        evidence_id, 
        "REGISTERED", 
        uploader_name,
        f"Initial registration via {source_type}"
    )
    
    return jsonify({
        "message": "Evidence registered successfully",
        "evidence_id": evidence_id,
        "hash": file_hash,
        "pre_entry_risk": risk,
        "ai_detection": ai_result,
        "timestamp": datetime.datetime.now().isoformat()
    })

@app.route("/verify", methods=["POST"])
def verify_evidence():
    """Verify evidence integrity"""
    file = request.files.get("file")
    evidence_id = request.form.get("evidence_id")
    verifier_name = request.form.get("verifier_name", "Anonymous")
    
    if not file:
        return jsonify({"error": "File missing"}), 400
    
    if evidence_id not in EVIDENCE_DB:
        return jsonify({"error": "Evidence ID not found"}), 404
    
    # Generate hash of uploaded file
    file_bytes = file.read()
    current_hash = generate_hash(file_bytes)
    
    # Get stored evidence
    stored_evidence = EVIDENCE_DB[evidence_id]
    original_hash = stored_evidence["hash"]
    
    # Determine integrity status
    status = "INTACT" if current_hash == original_hash else "TAMPERED"
    
    # Add to chain of custody
    add_to_chain_of_custody(
        evidence_id,
        "VERIFIED",
        verifier_name,
        f"Verification result: {status}"
    )
    
    return jsonify({
        "evidence_id": evidence_id,
        "integrity_status": status,
        "stored_hash": original_hash,
        "current_hash": current_hash,
        "match": current_hash == original_hash,
        "risk_level": stored_evidence["risk"],
        "verification_timestamp": datetime.datetime.now().isoformat()
    })

@app.route("/chain-of-custody/<evidence_id>", methods=["GET"])
def get_chain_of_custody(evidence_id):
    """Get complete chain of custody for evidence"""
    if evidence_id not in EVIDENCE_DB:
        return jsonify({"error": "Evidence ID not found"}), 404
    
    return jsonify({
        "evidence_id": evidence_id,
        "chain": CHAIN_OF_CUSTODY.get(evidence_id, []),
        "total_entries": len(CHAIN_OF_CUSTODY.get(evidence_id, []))
    })

@app.route("/multi-evidence/create-case", methods=["POST"])
def create_multi_evidence_case():
    """Create a case linking multiple pieces of evidence"""
    data = request.get_json()
    case_id = data.get("case_id")
    evidence_ids = data.get("evidence_ids", [])
    case_name = data.get("case_name", "")
    investigator = data.get("investigator", "Anonymous")
    
    if not case_id or not evidence_ids:
        return jsonify({"error": "Missing case_id or evidence_ids"}), 400
    
    # Verify all evidence exists
    missing_evidence = [eid for eid in evidence_ids if eid not in EVIDENCE_DB]
    if missing_evidence:
        return jsonify({"error": f"Evidence not found: {missing_evidence}"}), 404
    
    # Create case
    MULTI_EVIDENCE_CASES[case_id] = {
        "case_name": case_name,
        "evidence_ids": evidence_ids,
        "investigator": investigator,
        "created_timestamp": datetime.datetime.now().isoformat(),
        "status": "ACTIVE"
    }
    
    return jsonify({
        "message": "Case created successfully",
        "case_id": case_id,
        "evidence_count": len(evidence_ids)
    })

@app.route("/multi-evidence/corroborate/<case_id>", methods=["GET"])
def corroborate_evidence(case_id):
    """Analyze multiple evidence pieces for corroboration"""
    if case_id not in MULTI_EVIDENCE_CASES:
        return jsonify({"error": "Case not found"}), 404
    
    case = MULTI_EVIDENCE_CASES[case_id]
    evidence_ids = case["evidence_ids"]
    
    # Analyze evidence
    analysis = {
        "case_id": case_id,
        "total_evidence": len(evidence_ids),
        "evidence_details": [],
        "corroboration_score": 0,
        "conflicts": []
    }
    
    for eid in evidence_ids:
        if eid in EVIDENCE_DB:
            ev = EVIDENCE_DB[eid]
            analysis["evidence_details"].append({
                "evidence_id": eid,
                "risk": ev["risk"],
                "source_type": ev["source_type"],
                "ai_detection": ev.get("ai_detection", {})
            })
    
    # Calculate corroboration score (simplified)
    low_risk_count = sum(1 for ev in analysis["evidence_details"] if EVIDENCE_DB[ev["evidence_id"]]["risk"] in ["LOW", "MEDIUM"])
    analysis["corroboration_score"] = round((low_risk_count / len(evidence_ids)) * 100, 2)
    
    return jsonify(analysis)

@app.route("/ai-detection/<evidence_id>", methods=["GET"])
def get_ai_detection(evidence_id):
    """Get AI manipulation detection results"""
    if evidence_id not in AI_DETECTION_RESULTS:
        return jsonify({"error": "No AI detection results found"}), 404
    
    return jsonify(AI_DETECTION_RESULTS[evidence_id])

@app.route("/dashboard/stats", methods=["GET"])
def get_dashboard_stats():
    """Get statistics for dashboards"""
    total_evidence = len(EVIDENCE_DB)
    total_cases = len(MULTI_EVIDENCE_CASES)
    
    risk_distribution = {"LOW": 0, "MEDIUM": 0, "HIGH": 0, "VERY HIGH": 0}
    ai_flagged = 0
    
    for ev in EVIDENCE_DB.values():
        risk_distribution[ev["risk"]] += 1
        if ev.get("ai_detection", {}).get("is_manipulated"):
            ai_flagged += 1
    
    return jsonify({
        "total_evidence": total_evidence,
        "total_cases": total_cases,
        "risk_distribution": risk_distribution,
        "ai_flagged_count": ai_flagged,
        "last_updated": datetime.datetime.now().isoformat()
    })

@app.route("/evidence/list", methods=["GET"])
def list_evidence():
    """List all registered evidence"""
    evidence_list = []
    for eid, data in EVIDENCE_DB.items():
        evidence_list.append({
            "evidence_id": eid,
            "source_type": data["source_type"],
            "risk": data["risk"],
            "timestamp": data["registration_timestamp"],
            "uploader": data["uploader_name"]
        })
    
    return jsonify({
        "total": len(evidence_list),
        "evidence": evidence_list
    })

# ============ PDF DOWNLOAD ENDPOINTS ============

@app.route('/download-pdf/evidence', methods=['POST'])
def download_evidence_pdf():
    """Generate PDF for evidence registration"""
    try:
        data = request.json
        evidence_id = data.get('evidence_id')
        
        if not evidence_id:
            return jsonify({'error': 'Evidence ID required'}), 400
        
        if evidence_id not in EVIDENCE_DB:
            return jsonify({'error': 'Evidence not found'}), 404
        
        evidence = EVIDENCE_DB[evidence_id]
        
        # Create PDF
        buffer = BytesIO()
        doc = SimpleDocTemplate(buffer, pagesize=letter, topMargin=0.5*inch, bottomMargin=0.5*inch)
        elements = []
        styles = getSampleStyleSheet()
        
        # Custom styles
        title_style = ParagraphStyle(
            'CustomTitle',
            parent=styles['Heading1'],
            fontSize=28,
            textColor=colors.HexColor('#3b82f6'),
            spaceAfter=20,
            alignment=TA_CENTER,
            fontName='Helvetica-Bold'
        )
        
        subtitle_style = ParagraphStyle(
            'Subtitle',
            parent=styles['Normal'],
            fontSize=12,
            textColor=colors.HexColor('#64748b'),
            alignment=TA_CENTER,
            spaceAfter=30
        )
        
        # Title
        elements.append(Paragraph("🔒 VeriCourt Evidence Report", title_style))
        elements.append(Paragraph("Digital Evidence Integrity Platform", subtitle_style))
        elements.append(Spacer(1, 0.3*inch))
        
        # Evidence Information Section
        elements.append(Paragraph("Evidence Information", styles['Heading2']))
        elements.append(Spacer(1, 0.1*inch))
        
        info_data = [
            ['Evidence ID:', evidence_id],
            ['Case Number:', evidence.get('case_number', 'N/A')],
            ['Registration Date:', evidence.get('registration_timestamp', 'N/A')],
            ['Officer/Uploader:', evidence.get('uploader_name', 'N/A')],
            ['Source Type:', evidence.get('source_type', 'N/A')],
            ['Risk Level:', evidence.get('risk', 'N/A')],
            ['File Name:', evidence.get('metadata', {}).get('filename', 'N/A')],
            ['File Size:', f"{evidence.get('metadata', {}).get('size_bytes', 0) / (1024*1024):.2f} MB"],
        ]
        
        info_table = Table(info_data, colWidths=[2.5*inch, 4*inch])
        info_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (0, -1), colors.HexColor('#e0e7ff')),
            ('TEXTCOLOR', (0, 0), (-1, -1), colors.HexColor('#1e293b')),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, -1), 11),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 12),
            ('TOPPADDING', (0, 0), (-1, -1), 12),
            ('GRID', (0, 0), (-1, -1), 1, colors.HexColor('#cbd5e1')),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE')
        ]))
        elements.append(info_table)
        elements.append(Spacer(1, 0.4*inch))
        
        # Cryptographic Hash Section
        elements.append(Paragraph("Cryptographic Hash (SHA-256)", styles['Heading2']))
        elements.append(Spacer(1, 0.1*inch))
        
        hash_data = [[evidence.get('hash', 'N/A')]]
        hash_table = Table(hash_data, colWidths=[6.5*inch])
        hash_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor('#f0fdf4')),
            ('TEXTCOLOR', (0, 0), (-1, -1), colors.HexColor('#15803d')),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, -1), 'Courier'),
            ('FONTSIZE', (0, 0), (-1, -1), 9),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 15),
            ('TOPPADDING', (0, 0), (-1, -1), 15),
            ('BOX', (0, 0), (-1, -1), 2, colors.HexColor('#10b981')),
        ]))
        elements.append(hash_table)
        elements.append(Spacer(1, 0.4*inch))
        
        # AI Detection Results Section
        ai_detection = evidence.get('ai_detection', {})
        elements.append(Paragraph("AI Authenticity Assessment", styles['Heading2']))
        elements.append(Spacer(1, 0.1*inch))
        
        is_manipulated = ai_detection.get('is_manipulated', False)
        status_text = "⚠️ FLAGGED FOR REVIEW" if is_manipulated else "✅ VERIFIED AUTHENTIC"
        status_color = colors.HexColor('#fef2f2') if is_manipulated else colors.HexColor('#f0fdf4')
        status_text_color = colors.HexColor('#991b1b') if is_manipulated else colors.HexColor('#15803d')
        
        detection_data = [
            ['Status:', status_text],
            ['Confidence:', f"{ai_detection.get('confidence', 0):.2f}%"],
            ['Detection Type:', ai_detection.get('manipulation_type', 'None').upper()],
            ['Analysis Date:', ai_detection.get('analysis_timestamp', 'N/A')],
        ]
        
        detection_table = Table(detection_data, colWidths=[2.5*inch, 4*inch])
        detection_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, -1), status_color),
            ('TEXTCOLOR', (0, 0), (0, -1), colors.HexColor('#1e293b')),
            ('TEXTCOLOR', (1, 0), (1, 0), status_text_color),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
            ('FONTNAME', (1, 0), (1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, -1), 11),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 12),
            ('TOPPADDING', (0, 0), (-1, -1), 12),
            ('GRID', (0, 0), (-1, -1), 1, colors.HexColor('#cbd5e1')),
        ]))
        elements.append(detection_table)
        elements.append(Spacer(1, 0.5*inch))
        
        # Footer
        footer_style = ParagraphStyle(
            'Footer',
            parent=styles['Normal'],
            fontSize=9,
            textColor=colors.HexColor('#64748b'),
            alignment=TA_CENTER
        )
        elements.append(Spacer(1, 0.3*inch))
        elements.append(Paragraph("─" * 80, footer_style))
        elements.append(Spacer(1, 0.1*inch))
        elements.append(Paragraph(
            f"Generated on {datetime.datetime.now().strftime('%B %d, %Y at %I:%M %p')} | VeriCourt © 2025<br/>Forensic-Grade Digital Evidence Platform", 
            footer_style
        ))
        
        # Build PDF
        doc.build(elements)
        buffer.seek(0)
        
        return send_file(
            buffer,
            mimetype='application/pdf',
            as_attachment=True,
            download_name=f'Evidence_{evidence_id}_{datetime.datetime.now().strftime("%Y%m%d")}.pdf'
        )
        
    except Exception as e:
        print(f"PDF generation error: {str(e)}")
        return jsonify({'error': str(e)}), 500


@app.route('/download-pdf/verification', methods=['POST'])
def download_verification_pdf():
    """Generate PDF for verification results"""
    try:
        data = request.json
        evidence_id = data.get('evidence_id')
        
        if not evidence_id:
            return jsonify({'error': 'Evidence ID required'}), 400
        
        if evidence_id not in EVIDENCE_DB:
            return jsonify({'error': 'Evidence not found'}), 404
        
        evidence = EVIDENCE_DB[evidence_id]
        chain = CHAIN_OF_CUSTODY.get(evidence_id, [])
        
        # Find latest verification
        verification_entries = [entry for entry in chain if entry['action'] == 'VERIFIED']
        latest_verification = verification_entries[-1] if verification_entries else None
        
        # Create PDF
        buffer = BytesIO()
        doc = SimpleDocTemplate(buffer, pagesize=letter, topMargin=0.5*inch, bottomMargin=0.5*inch)
        elements = []
        styles = getSampleStyleSheet()
        
        # Title
        title_style = ParagraphStyle(
            'CustomTitle',
            parent=styles['Heading1'],
            fontSize=28,
            textColor=colors.HexColor('#3b82f6'),
            spaceAfter=20,
            alignment=TA_CENTER,
            fontName='Helvetica-Bold'
        )
        
        elements.append(Paragraph("🔍 Evidence Verification Report", title_style))
        elements.append(Spacer(1, 0.3*inch))
        
        if latest_verification:
            # Verification details
            is_intact = 'INTACT' in latest_verification.get('details', '')
            status_text = "✅ INTEGRITY VERIFIED" if is_intact else "🚨 TAMPERING DETECTED"
            status_color = colors.HexColor('#f0fdf4') if is_intact else colors.HexColor('#fef2f2')
            
            verification_data = [
                ['Evidence ID:', evidence_id],
                ['Verification Status:', status_text],
                ['Verified By:', latest_verification.get('user', 'N/A')],
                ['Verification Time:', latest_verification.get('timestamp', 'N/A')],
                ['Result:', latest_verification.get('details', 'N/A')],
            ]
            
            verification_table = Table(verification_data, colWidths=[2.5*inch, 4*inch])
            verification_table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, -1), status_color),
                ('TEXTCOLOR', (0, 0), (-1, -1), colors.HexColor('#1e293b')),
                ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
                ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, -1), 11),
                ('BOTTOMPADDING', (0, 0), (-1, -1), 12),
                ('TOPPADDING', (0, 0), (-1, -1), 12),
                ('GRID', (0, 0), (-1, -1), 1, colors.HexColor('#cbd5e1')),
            ]))
            elements.append(verification_table)
        else:
            elements.append(Paragraph("No verification records found.", styles['Normal']))
        
        # Build PDF
        doc.build(elements)
        buffer.seek(0)
        
        return send_file(
            buffer,
            mimetype='application/pdf',
            as_attachment=True,
            download_name=f'Verification_{evidence_id}_{datetime.datetime.now().strftime("%Y%m%d")}.pdf'
        )
        
    except Exception as e:
        print(f"PDF generation error: {str(e)}")
        return jsonify({'error': str(e)}), 500


@app.route('/download-pdf/case', methods=['POST'])
def download_case_pdf():
    """Generate PDF for case analysis"""
    try:
        data = request.json
        case_id = data.get('case_id')
        
        if not case_id:
            return jsonify({'error': 'Case ID required'}), 400
        
        if case_id not in MULTI_EVIDENCE_CASES:
            return jsonify({'error': 'Case not found'}), 404
        
        case = MULTI_EVIDENCE_CASES[case_id]
        
        # Create PDF
        buffer = BytesIO()
        doc = SimpleDocTemplate(buffer, pagesize=letter, topMargin=0.5*inch, bottomMargin=0.5*inch)
        elements = []
        styles = getSampleStyleSheet()
        
        # Title
        title_style = ParagraphStyle(
            'CustomTitle',
            parent=styles['Heading1'],
            fontSize=28,
            textColor=colors.HexColor('#3b82f6'),
            spaceAfter=20,
            alignment=TA_CENTER,
            fontName='Helvetica-Bold'
        )
        
        elements.append(Paragraph("📊 Case Analysis Report", title_style))
        elements.append(Spacer(1, 0.3*inch))
        
        # Case Information
        case_data = [
            ['Case ID:', case_id],
            ['Case Name:', case.get('case_name', 'N/A')],
            ['Lead Investigator:', case.get('investigator', 'N/A')],
            ['Created:', case.get('created_timestamp', 'N/A')],
            ['Status:', case.get('status', 'N/A')],
            ['Total Evidence:', str(len(case.get('evidence_ids', [])))],
        ]
        
        case_table = Table(case_data, colWidths=[2.5*inch, 4*inch])
        case_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (0, -1), colors.HexColor('#e0e7ff')),
            ('TEXTCOLOR', (0, 0), (-1, -1), colors.HexColor('#1e293b')),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, -1), 11),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 12),
            ('TOPPADDING', (0, 0), (-1, -1), 12),
            ('GRID', (0, 0), (-1, -1), 1, colors.HexColor('#cbd5e1')),
        ]))
        elements.append(case_table)
        elements.append(Spacer(1, 0.4*inch))
        
        # Evidence List
        elements.append(Paragraph("Linked Evidence Items", styles['Heading2']))
        elements.append(Spacer(1, 0.1*inch))
        
        evidence_list = [['#', 'Evidence ID', 'Source Type', 'Risk Level']]
        
        for i, eid in enumerate(case.get('evidence_ids', []), 1):
            if eid in EVIDENCE_DB:
                ev = EVIDENCE_DB[eid]
                evidence_list.append([
                    str(i),
                    eid,
                    ev.get('source_type', 'N/A'),
                    ev.get('risk', 'N/A')
                ])
        
        evidence_table = Table(evidence_list, colWidths=[0.5*inch, 2.5*inch, 2*inch, 1.5*inch])
        evidence_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#3b82f6')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, -1), 10),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 10),
            ('TOPPADDING', (0, 0), (-1, -1), 10),
            ('GRID', (0, 0), (-1, -1), 1, colors.HexColor('#cbd5e1')),
            ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#f8fafc')])
        ]))
        elements.append(evidence_table)
        
        # Build PDF
        doc.build(elements)
        buffer.seek(0)
        
        return send_file(
            buffer,
            mimetype='application/pdf',
            as_attachment=True,
            download_name=f'Case_{case_id}_{datetime.datetime.now().strftime("%Y%m%d")}.pdf'
        )
        
    except Exception as e:
        print(f"PDF generation error: {str(e)}")
        return jsonify({'error': str(e)}), 500


@app.route('/download-pdf/chain', methods=['POST'])
def download_chain_pdf():
    """Generate PDF for chain of custody"""
    try:
        data = request.json
        evidence_id = data.get('evidence_id')
        
        if not evidence_id:
            return jsonify({'error': 'Evidence ID required'}), 400
        
        if evidence_id not in EVIDENCE_DB:
            return jsonify({'error': 'Evidence not found'}), 404
        
        chain = CHAIN_OF_CUSTODY.get(evidence_id, [])
        
        # Create PDF
        buffer = BytesIO()
        doc = SimpleDocTemplate(buffer, pagesize=letter, topMargin=0.5*inch, bottomMargin=0.5*inch)
        elements = []
        styles = getSampleStyleSheet()
        
        # Title
        title_style = ParagraphStyle(
            'CustomTitle',
            parent=styles['Heading1'],
            fontSize=28,
            textColor=colors.HexColor('#3b82f6'),
            spaceAfter=20,
            alignment=TA_CENTER,
            fontName='Helvetica-Bold'
        )
        
        elements.append(Paragraph("⏱️ Chain of Custody Report", title_style))
        elements.append(Spacer(1, 0.2*inch))
        
        elements.append(Paragraph(f"Evidence ID: {data.get('evidence_id')}", styles['Heading2']))
        elements.append(Spacer(1, 0.3*inch))
        
        if not CHAIN_OF_CUSTODY.get(data.get('evidence_id')):
            elements.append(Paragraph("No chain of custody records found.", styles['Normal']))
        else:
            # Chain records
            chain_data = [['#', 'Action', 'Officer/User', 'Timestamp', 'Details']]
            
            for i, record in enumerate(CHAIN_OF_CUSTODY.get(evidence_id, []), 1):
                chain_data.append([
                    str(i),
                    record.get('action', 'N/A'),
                    record.get('user', 'N/A'),
                    record.get('timestamp', 'N/A')[:19]  # Trim timestamp
                ])
            
            chain_table = Table(chain_data, colWidths=[0.5*inch, 2*inch, 2*inch, 2*inch])
            chain_table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#3b82f6')),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
                ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, -1), 10),
                ('BOTTOMPADDING', (0, 0), (-1, -1), 10),
                ('TOPPADDING', (0, 0), (-1, -1), 10),
                ('GRID', (0, 0), (-1, -1), 1, colors.HexColor('#cbd5e1')),
                ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#f8fafc')])
            ]))
            elements.append(chain_table)
        
        # Build PDF
        doc.build(elements)
        buffer.seek(0)
        
        return send_file(
            buffer,
            mimetype='application/pdf',
            as_attachment=True,
            download_name=f'Chain_of_Custody_{evidence_id}_{datetime.datetime.now().strftime("%Y%m%d")}.pdf'
        )
        
    except Exception as e:
        print(f"PDF generation error: {str(e)}")
        return jsonify({'error': str(e)}), 500


if __name__ == "__main__":
    # Create templates directory if it doesn't exist
    os.makedirs("templates", exist_ok=True)
    print("🔒 VeriCourt Backend Starting...")
    print("📊 Dashboard: http://localhost:5000")
    print("✅ PDF Download: Enabled")
    app.run(debug=True, port=5000)