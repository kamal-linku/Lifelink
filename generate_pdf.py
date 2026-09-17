import sys
import os
from datetime import datetime
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, KeepTogether, HRFlowable
)
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.pdfgen import canvas

class NumberedCanvas(canvas.Canvas):
    """Two-pass canvas to dynamically compute and print total page count."""
    def __init__(self, *args, **kwargs):
        canvas.Canvas.__init__(self, *args, **kwargs)
        self._saved_page_states = []

    def showPage(self):
        self._saved_page_states.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        num_pages = len(self._saved_page_states)
        for state in self._saved_page_states:
            self.__dict__.update(state)
            self.draw_page_decorations(num_pages)
            canvas.Canvas.showPage(self)
        canvas.Canvas.save(self)

    def draw_page_decorations(self, page_count):
        if self._pageNumber == 1:
            # Suppress running header/footer on cover page
            return
        
        self.saveState()
        self.setFont("Helvetica", 8)
        self.setFillColor(colors.HexColor("#64748b"))
        
        # Header
        self.drawString(54, 750, "LifeLink — Emergency Resource Coordination Platform | Technical Documentation")
        self.setStrokeColor(colors.HexColor("#e2e8f0"))
        self.setLineWidth(0.5)
        self.line(54, 744, letter[0] - 54, 744)

        # Footer
        self.line(54, 45, letter[0] - 54, 45)
        self.drawString(54, 32, "Confidential — Academic & Technical Evaluation Reference")
        page_str = f"Page {self._pageNumber} of {page_count}"
        self.drawRightString(letter[0] - 54, 32, page_str)
        self.restoreState()

def build_pdf(pdf_path):
    doc = SimpleDocTemplate(
        pdf_path,
        pagesize=letter,
        leftMargin=54,
        rightMargin=54,
        topMargin=54,
        bottomMargin=54
    )

    styles = getSampleStyleSheet()
    
    # Custom Brand Palette
    primary = colors.HexColor("#0f172a") # Slate 900
    accent = colors.HexColor("#e11d48")  # Rose 600
    secondary = colors.HexColor("#334155") # Slate 700
    bg_light = colors.HexColor("#f8fafc") # Slate 50
    border_color = colors.HexColor("#cbd5e1")

    # Typography Styles
    title_style = ParagraphStyle(
        "CoverTitle",
        parent=styles["Normal"],
        fontName="Helvetica-Bold",
        fontSize=28,
        leading=34,
        textColor=primary,
        alignment=0
    )

    subtitle_style = ParagraphStyle(
        "CoverSubtitle",
        parent=styles["Normal"],
        fontName="Helvetica",
        fontSize=13,
        leading=18,
        textColor=accent,
        alignment=0
    )

    meta_style = ParagraphStyle(
        "CoverMeta",
        parent=styles["Normal"],
        fontName="Helvetica",
        fontSize=9,
        leading=14,
        textColor=secondary
    )

    h1_style = ParagraphStyle(
        "SectionH1",
        parent=styles["Normal"],
        fontName="Helvetica-Bold",
        fontSize=18,
        leading=22,
        textColor=primary,
        spaceBefore=14,
        spaceAfter=8,
        keepWithNext=True
    )

    h2_style = ParagraphStyle(
        "SectionH2",
        parent=styles["Normal"],
        fontName="Helvetica-Bold",
        fontSize=13,
        leading=17,
        textColor=accent,
        spaceBefore=10,
        spaceAfter=4,
        keepWithNext=True
    )

    body_style = ParagraphStyle(
        "BodyDark",
        parent=styles["Normal"],
        fontName="Helvetica",
        fontSize=9.5,
        leading=14,
        textColor=colors.HexColor("#1e293b"),
        spaceAfter=6
    )

    callout_style = ParagraphStyle(
        "CalloutText",
        parent=styles["Normal"],
        fontName="Helvetica-Oblique",
        fontSize=9.5,
        leading=14,
        textColor=primary
    )

    code_style = ParagraphStyle(
        "CodeBlock",
        parent=styles["Normal"],
        fontName="Courier",
        fontSize=8,
        leading=11,
        textColor=colors.HexColor("#0f172a")
    )

    table_cell = ParagraphStyle(
        "TableCell",
        parent=styles["Normal"],
        fontName="Helvetica",
        fontSize=8.5,
        leading=11,
        textColor=primary
    )

    table_cell_bold = ParagraphStyle(
        "TableCellBold",
        parent=styles["Normal"],
        fontName="Helvetica-Bold",
        fontSize=8.5,
        leading=11,
        textColor=primary
    )

    story = []

    # ==================== COVER PAGE ====================
    story.append(Spacer(1, 30))
    story.append(Paragraph("PROJECT DOCUMENTATION", ParagraphStyle("Tag", fontName="Helvetica-Bold", fontSize=10, textColor=accent, spaceAfter=8)))
    story.append(Paragraph("LifeLink — Emergency Resource Coordination Platform", title_style))
    story.append(Spacer(1, 6))
    story.append(Paragraph("Real-Time Multi-Resource Triage, Geospatial Matching Engine & Volunteer Privacy Architecture", subtitle_style))
    story.append(Spacer(1, 20))
    story.append(HRFlowable(width="100%", thickness=3, color=accent, spaceAfter=25))

    story.append(Paragraph("<b>Project Domain:</b> Critical Healthcare Dispatch & Emergency Informatics", meta_style))
    story.append(Paragraph("<b>Architecture:</b> FastAPI (Python 3.10) + React 19 / Vite + WebSockets + Leaflet GIS", meta_style))
    story.append(Paragraph("<b>Geographic Deployment:</b> Bhubaneswar Emergency Medical Region (AIIMS, Capital Hospital, Red Cross)", meta_style))
    story.append(Paragraph(f"<b>Generated:</b> {datetime.now().strftime('%B %d, %Y')}", meta_style))
    story.append(Paragraph("<b>Author / Lead Developer:</b> Kamal (Pair-programmed with Antigravity)", meta_style))
    story.append(Spacer(1, 35))

    # Viva Pitch Highlight Callout Box
    viva_text = (
        "<b>Core Viva Proposition:</b><br/>"
        "<i>\"Our problem is not simply finding a blood donor. The problem is coordinating the entire emergency response quickly.\"</i><br/><br/>"
        "During critical trauma, fragmented communication across WhatsApp, phone calls, and manual searches causes lethal delays. "
        "LifeLink solves this through automated multi-factor resource ranking, verified inventory synchronization, and sub-second WebSocket dispatch."
    )
    viva_table = Table([[Paragraph(viva_text, callout_style)]], colWidths=[letter[0] - 108])
    viva_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor("#fff1f2")),
        ('BOX', (0, 0), (-1, -1), 1, colors.HexColor("#f43f5e")),
        ('TOPPADDING', (0, 0), (-1, -1), 12),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 12),
        ('LEFTPADDING', (0, 0), (-1, -1), 14),
        ('RIGHTPADDING', (0, 0), (-1, -1), 14),
    ]))
    story.append(viva_table)

    story.append(Spacer(1, 40))
    story.append(Paragraph("<b>Table of Contents:</b>", h2_style))
    toc_data = [
        ["1. Executive Summary & Problem Formulation", "5. Database Schema & Relational Design"],
        ["2. Technical Architecture & Tech Stack", "6. Platform Modules & Frontend Portals"],
        ["3. Mathematical Matching & Ranking Algorithm", "7. Automated Testing & Verification Results"],
        ["4. Real-time Workflow State Machine", "8. VS Code Run & Viva Demo Script"]
    ]
    toc_table = Table([[Paragraph(c, body_style) for c in row] for row in toc_data], colWidths=[240, 240])
    toc_table.setStyle(TableStyle([
        ('TOPPADDING', (0, 0), (-1, -1), 3),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 3),
        ('LEFTPADDING', (0, 0), (-1, -1), 0),
    ]))
    story.append(toc_table)

    story.append(PageBreak())

    # ==================== CHAPTER 1 ====================
    story.append(Paragraph("1. Executive Summary & Problem Formulation", h1_style))
    story.append(HRFlowable(width="100%", thickness=1, color=colors.HexColor("#e2e8f0"), spaceAfter=12))
    
    story.append(Paragraph(
        "In emergency medical emergencies—such as road traffic accidents, acute surgeries, or post-partum hemorrhages—access to "
        "time-sensitive compatible blood components (Packed Red Blood Cells, Platelets, Plasma, Whole Blood) and immediate support services "
        "(Ambulances, ICU beds) is fragmented across disconnected hospital telephone switchboards, social media posts, and unverified contacts.",
        body_style
    ))
    story.append(Paragraph(
        "<b>The Concrete Dilemma:</b> Rahul Sharma (Age 28) suffers severe trauma in Bhubaneswar and requires <b>2 Units of O+ Packed RBC</b> "
        "at AIIMS Hospital within <b>2 hours</b>. Traditionally, the family calls relatives, sends broadcast messages into WhatsApp groups, "
        "calls random blood banks, and searches Google Maps while vital minutes expire.",
        body_style
    ))
    story.append(Paragraph(
        "<b>The LifeLink Solution:</b> LifeLink acts as a unified command-and-control emergency exchange. A single request triggers an "
        "instant spatial query that checks nearby verified blood banks (e.g. AIIMS Blood Bank, Capital Hospital, Red Cross) and nearby registered "
        "voluntary donors, computes a normalized <b>Match Score</b>, and initiates a prioritized real-time dispatch cascade via WebSockets.",
        body_style
    ))

    story.append(Spacer(1, 8))

    # ==================== CHAPTER 2 ====================
    story.append(Paragraph("2. Technical Architecture & System Design", h1_style))
    story.append(HRFlowable(width="100%", thickness=1, color=colors.HexColor("#e2e8f0"), spaceAfter=12))

    story.append(Paragraph(
        "The system follows an asynchronous, decoupled client-server architecture tailored for sub-second emergency response times:",
        body_style
    ))

    arch_rows = [
        ["Layer", "Technology", "Role & Key Responsibilities"],
        ["Client (Frontend)", "React 19, Vite 8, Tailwind v4", "Interactive responsive UI, dual triage actions, role portals, toast alert listener"],
        ["Map Radar", "Leaflet & React-Leaflet GIS", "Real-time OpenStreetMap canvas plotting color-coded hospital, blood bank, ambulance, donor markers"],
        ["Backend REST API", "FastAPI (Python 3.10)", "High-performance async request routing, Pydantic validation, JWT token creation"],
        ["Real-Time Dispatch", "Native WebSockets Hub", "Bi-directional event bus pushing instant emergency notifications and status shifts"],
        ["Matching Engine", "Python Mathematical Core", "Multi-factor scoring: Haversine distance, stock availability, urgency weighting"],
        ["Data Persistence", "SQLAlchemy 2.0 / SQLite / Postgres", "ACID transactional store for multi-user requests, donor profiles, inventories, audit logs"]
    ]
    arch_table = Table([[Paragraph(c, table_cell_bold if i == 0 else table_cell) for c in row] for i, row in enumerate(arch_rows)], colWidths=[90, 140, 270])
    arch_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor("#f1f5f9")),
        ('GRID', (0, 0), (-1, -1), 0.5, border_color),
        ('TOPPADDING', (0, 0), (-1, -1), 5),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 5),
    ]))
    story.append(arch_table)

    story.append(Spacer(1, 10))

    # ==================== CHAPTER 3 ====================
    story.append(Paragraph("3. Mathematical Matching & Ranking Engine", h1_style))
    story.append(HRFlowable(width="100%", thickness=1, color=colors.HexColor("#e2e8f0"), spaceAfter=12))

    story.append(Paragraph(
        "LifeLink distinguishes itself from generic CRUD systems through its quantitative ranking algorithm. "
        "When an emergency request is lodged, candidate resources receive a normalized score <b>S &in; [0, 99]%</b>:",
        body_style
    ))

    formula_text = (
        "<b>Normalized Score Formula:</b><br/>"
        "S = S_avail (35 pts) + S_dist (30 pts) + S_type (15 pts) + S_urgency (10 pts) + S_compat (10 pts)<br/><br/>"
        "1. <b>Distance Decay Score:</b> S_dist = 30 * (1 - (d / 25.0) * 0.75) for d &le; 25 km<br/>"
        "   where distance <i>d</i> is computed using the Great-Circle Haversine formula:<br/>"
        "   d = 2R * arcsin( sqrt( sin&sup2;(&Delta;&phi;/2) + cos(&phi;&sub1;)cos(&phi;&sub2;)sin&sup2;(&Delta;&lambda;/2) ) )<br/>"
        "2. <b>Stock Availability:</b> Full 35 pts if verified stock &ge; needed units; proportional points if partial stock.<br/>"
        "3. <b>Institutional Reliability:</b> Blood Bank = 15 pts, Hospital = 14 pts, Verified Voluntary Donor = 12 pts.<br/>"
        "4. <b>Urgency Weight:</b> Critical emergency requests (&lt;2 hrs) grant maximum priority to proximate units.<br/>"
        "5. <b>ABO/Rh Blood Compatibility:</b> Exact blood group match receives 10 pts; universally compatible units receive 7 pts."
    )
    formula_table = Table([[Paragraph(formula_text, code_style)]], colWidths=[letter[0] - 108])
    formula_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor("#f8fafc")),
        ('BOX', (0, 0), (-1, -1), 1, border_color),
        ('TOPPADDING', (0, 0), (-1, -1), 8),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
        ('LEFTPADDING', (0, 0), (-1, -1), 10),
        ('RIGHTPADDING', (0, 0), (-1, -1), 10),
    ]))
    story.append(formula_table)

    story.append(Spacer(1, 8))
    story.append(Paragraph(
        "<b>Medical Governance Protocol:</b> LifeLink strictly operates as a coordination and discovery platform. "
        "As highlighted in national transfusion guidelines, clinical blood compatibility verification, cross-matching, "
        "and final component release are exclusively performed by licensed medical officers at the receiving blood centre.",
        body_style
    ))

    story.append(PageBreak())

    # ==================== CHAPTER 4 ====================
    story.append(Paragraph("4. Real-time Workflow Pipeline & State Machine", h1_style))
    story.append(HRFlowable(width="100%", thickness=1, color=colors.HexColor("#e2e8f0"), spaceAfter=12))

    story.append(Paragraph(
        "An emergency lifecycle progresses through five deterministic workflow states tracked concurrently on both requester and coordinator screens:",
        body_style
    ))

    steps_rows = [
        ["State Code", "Stage Name", "Trigger Action", "WebSocket Broadcast Event"],
        ["MATCHING", "1. Matching", "Emergency request submitted by attendant", "EMERGENCY_CREATED (payload with request code, units, hospital)"],
        ["CONTACTED", "2. Blood Bank Contacted", "Matching engine contacts apex centers", "STATUS_CHANGED (alerts staff of pending reservation)"],
        ["RESPONDED", "3. Volunteer Response", "Donor reviews alert & clicks [ACCEPT]", "VOLUNTEER_ACCEPTED (issues ephemeral bridge token)"],
        ["CONFIRMED", "4. Resource Confirmed", "Unit reserved / donor en-route to center", "STATUS_CHANGED (locks assigned coordinator)"],
        ["COMPLETED", "5. Completed", "Blood delivered & transfusion initiated", "STATUS_CHANGED (archives request into hospital analytics)"]
    ]
    steps_table = Table([[Paragraph(c, table_cell_bold if i == 0 else table_cell) for c in row] for i, row in enumerate(steps_rows)], colWidths=[80, 110, 150, 160])
    steps_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor("#f1f5f9")),
        ('GRID', (0, 0), (-1, -1), 0.5, border_color),
        ('TOPPADDING', (0, 0), (-1, -1), 5),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 5),
    ]))
    story.append(steps_table)

    story.append(Spacer(1, 12))

    # ==================== CHAPTER 5 ====================
    story.append(Paragraph("5. Database Relational Architecture", h1_style))
    story.append(HRFlowable(width="100%", thickness=1, color=colors.HexColor("#e2e8f0"), spaceAfter=12))

    db_rows = [
        ["Entity Table", "Primary Key", "Key Attributes & Foreign Keys", "Cardinality"],
        ["users", "id (Int)", "name, email, phone (hashed), role, is_verified", "1 : 1 donor_profile, 1 : N requests"],
        ["donor_profiles", "id (Int)", "user_id (FK), blood_group, lat, lng, preferred_radius_km, is_available", "1 : 1 with users"],
        ["blood_banks", "id (Int)", "name, license_no, category, lat, lng, contact_phone, is_verified", "1 : N blood_inventory"],
        ["blood_inventory", "id (Int)", "blood_bank_id (FK), blood_group, component, units_available, last_updated", "N : 1 with blood_banks"],
        ["hospitals", "id (Int)", "name, registration_no, address, lat, lng, emergency_contact, total_beds, icu_beds", "Apex reference node"],
        ["emergency_requests", "id (Int)", "request_code (LL-xxxx), patient_name, blood_group, units_needed, status", "1 : N resource_matches"],
        ["resource_matches", "id (Int)", "request_id (FK), resource_type, resource_id, score, distance_km, status", "N : 1 with emergency_requests"],
        ["ambulances", "id (Int)", "vehicle_number, provider_name, ambulance_type (BLS/ALS), driver_name, is_available", "Independent fleet node"],
        ["pharmacies", "id (Int)", "name, address, lat, lng, is_24x7, inventory_notes, last_verified_minutes_ago", "Independent supplier node"]
    ]
    db_table = Table([[Paragraph(c, table_cell_bold if i == 0 else table_cell) for c in row] for i, row in enumerate(db_rows)], colWidths=[95, 65, 230, 110])
    db_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor("#f1f5f9")),
        ('GRID', (0, 0), (-1, -1), 0.5, border_color),
        ('TOPPADDING', (0, 0), (-1, -1), 4),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
    ]))
    story.append(db_table)

    story.append(PageBreak())

    # ==================== CHAPTER 6 ====================
    story.append(Paragraph("6. Platform Modules & Frontend Portals", h1_style))
    story.append(HRFlowable(width="100%", thickness=1, color=colors.HexColor("#e2e8f0"), spaceAfter=12))

    story.append(Paragraph(
        "LifeLink provides specialized, high-fidelity views tailored to the distinct participants in an emergency:",
        body_style
    ))

    modules = [
        ("Homepage & Dual Triage Dispatch:", "Features high-contrast action buttons: <b>'I NEED HELP'</b> (triggers sub-2-minute emergency request submission) and <b>'I CAN HELP'</b> (donor onboarding). Displays real-time metrics and emergency feed."),
        ("Emergency Radar Map (Leaflet):", "Interactive spatial canvas with custom HTML markers: Blood Banks (Red), Hospitals (Indigo), Ambulances (Amber), Donors (Emerald), and Active Patients (Pulsing Red SOS Beacon) with 1-click Google Maps turn-by-turn navigation."),
        ("Volunteer Privacy & Masked Bridge:", "Donors toggle emergency availability, calibrate response radiuses (2–30 km), and accept alerts. Under zero phone leakage rules, an ephemeral bridge token (e.g. <code>SECURE-BRIDGE-1-2</code>) connects the parties."),
        ("Hospital Triage & Analytics:", "Apex dashboard monitoring active requests, critical trauma counts, and resolved cases (31 received, 26 resolved, 5 pending)."),
        ("e-RaktKosh Aligned Blood Bank Hub:", "Allows certified lab technicians to manage stock by component (Packed RBC, Platelets, Plasma, Whole Blood) with real-time increment/decrement controls that synchronize across the entire city instantly."),
        ("Ambulance Fleet & 24x7 Pharmacy Telemetry:", "Provides vehicle dispatch triggers and rare medication searches (Heparin, Albumin, Tranexamic Acid) featuring explicit 'Reported 14m ago' freshness notices.")
    ]
    for title, desc in modules:
        story.append(Paragraph(f"&bull; <b>{title}</b> {desc}", body_style))
        story.append(Spacer(1, 3))

    story.append(Spacer(1, 8))

    # ==================== CHAPTER 7 ====================
    story.append(Paragraph("7. Automated Testing & Verification Results", h1_style))
    story.append(HRFlowable(width="100%", thickness=1, color=colors.HexColor("#e2e8f0"), spaceAfter=12))

    story.append(Paragraph(
        "A rigorous end-to-end automated test suite (<code>backend/test_pipeline.py</code>) was constructed to validate the entire coordination lifecycle:",
        body_style
    ))

    test_rows = [
        ["Test #", "Target Component / Verification Objective", "Observed Outcome", "Status"],
        ["T1", "Backend Health Check (/api/health)", "HTTP 200 OK — service online", "PASSED"],
        ["T2", "Geospatial Markers (/api/resources/map)", "17 verified medical markers returned", "PASSED"],
        ["T3", "Emergency Creation & Engine Execution", "Request generated; AIIMS scored 99.0%", "PASSED"],
        ["T4", "Workflow Pipeline Advancement", "Transitioned to CONTACTED state", "PASSED"],
        ["T5", "Volunteer Response & Privacy Bridge", "Accepted; SECURE-BRIDGE token issued", "PASSED"],
        ["T6", "Autonomous State Shift Validation", "Status auto-promoted to RESPONDED", "PASSED"],
        ["T7", "Hospital Triage Metrics Counter", "Active queue accurately updated", "PASSED"]
    ]
    test_table = Table([[Paragraph(c, table_cell_bold if i == 0 else table_cell) for c in row] for i, row in enumerate(test_rows)], colWidths=[40, 240, 160, 60])
    test_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor("#f1f5f9")),
        ('GRID', (0, 0), (-1, -1), 0.5, border_color),
        ('TOPPADDING', (0, 0), (-1, -1), 4),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
    ]))
    story.append(test_table)

    story.append(Spacer(1, 12))

    # ==================== CHAPTER 8 ====================
    story.append(Paragraph("8. VS Code Execution Guide & 5-Minute Viva Demo", h1_style))
    story.append(HRFlowable(width="100%", thickness=1, color=colors.HexColor("#e2e8f0"), spaceAfter=12))

    run_instructions = (
        "<b>Step-by-Step Launch Instructions:</b><br/>"
        "1. Open folder in VS Code: <code>File -&gt; Open Folder -&gt; lifelink</code><br/>"
        "2. Press <b>Ctrl + Shift + B</b> to execute the pre-configured compound task <i>'Start LifeLink (Full Stack)'</i>.<br/>"
        "3. Alternatively, use split terminals:<br/>"
        "   - Terminal 1 (Backend): <code>cd backend &amp;&amp; python run.py</code> (API: http://127.0.0.1:8000)<br/>"
        "   - Terminal 2 (Frontend): <code>cd frontend &amp;&amp; npm run dev</code> (UI: http://localhost:3000)<br/><br/>"
        "<b>Examiner 5-Minute Demonstration Script:</b><br/>"
        "&bull; <i>Minute 1:</i> Present the homepage and discuss the fragmentation of emergency care.<br/>"
        "&bull; <i>Minute 2:</i> Submit a Critical Request for 2 units of O+ Packed RBC at AIIMS Hospital.<br/>"
        "&bull; <i>Minute 3:</i> Demonstrate the Matching Engine results ranking AIIMS (99.0%) and Capital Hospital (94.7%).<br/>"
        "&bull; <i>Minute 4:</i> Open the Volunteer Portal, display the incoming emergency alert, and click [ACCEPT DISPATCH].<br/>"
        "&bull; <i>Minute 5:</i> Show how the requester's workflow stepper automatically moves to 'Volunteer Response' live via WebSockets."
    )
    run_table = Table([[Paragraph(run_instructions, body_style)]], colWidths=[letter[0] - 108])
    run_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor("#f8fafc")),
        ('BOX', (0, 0), (-1, -1), 1, border_color),
        ('TOPPADDING', (0, 0), (-1, -1), 8),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
        ('LEFTPADDING', (0, 0), (-1, -1), 10),
        ('RIGHTPADDING', (0, 0), (-1, -1), 10),
    ]))
    story.append(run_table)

    # Build the document
    doc.build(story, canvasmaker=NumberedCanvas)
    print(f"[SUCCESS] PDF generated successfully at: {pdf_path}")

if __name__ == "__main__":
    out_dir = r"C:\Users\kamal\.gemini\antigravity\scratch\lifelink"
    pdf_file = os.path.join(out_dir, "LifeLink_Project_Documentation.pdf")
    build_pdf(pdf_file)
