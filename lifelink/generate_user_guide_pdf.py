import os
from datetime import datetime
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, HRFlowable
)
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.pdfgen import canvas

class NumberedCanvas(canvas.Canvas):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._saved_page_states = []

    def showPage(self):
        self._saved_page_states.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        num_pages = len(self._saved_page_states)
        for state in self._saved_page_states:
            self.__dict__.update(state)
            self.draw_page_decorations(num_pages)
            super().showPage()
        super().save()

    def draw_page_decorations(self, page_count):
        if self._pageNumber == 1:
            return
        
        self.saveState()
        self.setFont("Helvetica", 8)
        self.setFillColor(colors.HexColor("#64748b"))
        
        # Running Header
        self.drawString(54, 750, "LifeLink Platform — End-User Feature Guide & Website Walkthrough")
        self.setStrokeColor(colors.HexColor("#e2e8f0"))
        self.setLineWidth(0.5)
        self.line(54, 744, letter[0] - 54, 744)

        # Running Footer
        self.line(54, 45, letter[0] - 54, 45)
        self.drawString(54, 32, "User Guide & Feature Manual — What Can You Do On LifeLink?")
        page_str = f"Page {self._pageNumber} of {page_count}"
        self.drawRightString(letter[0] - 54, 32, page_str)
        self.restoreState()

def generate_user_guide(pdf_path):
    doc = SimpleDocTemplate(
        pdf_path,
        pagesize=letter,
        leftMargin=54,
        rightMargin=54,
        topMargin=54,
        bottomMargin=54
    )

    styles = getSampleStyleSheet()

    # Brand Colors
    primary = colors.HexColor("#0f172a") # Slate 900
    accent = colors.HexColor("#e11d48")  # Rose 600
    emerald = colors.HexColor("#059669") # Emerald 600
    amber = colors.HexColor("#d97706")   # Amber 600
    secondary = colors.HexColor("#475569") # Slate 600
    border_color = colors.HexColor("#cbd5e1")

    # Typography
    cover_title = ParagraphStyle(
        "CoverTitle",
        parent=styles["Normal"],
        fontName="Helvetica-Bold",
        fontSize=26,
        leading=32,
        textColor=primary,
        spaceAfter=6
    )

    cover_subtitle = ParagraphStyle(
        "CoverSubtitle",
        parent=styles["Normal"],
        fontName="Helvetica",
        fontSize=12,
        leading=16,
        textColor=accent,
        spaceAfter=15
    )

    h1_style = ParagraphStyle(
        "H1Style",
        parent=styles["Normal"],
        fontName="Helvetica-Bold",
        fontSize=16,
        leading=20,
        textColor=primary,
        spaceBefore=14,
        spaceAfter=6,
        keepWithNext=True
    )

    h2_style = ParagraphStyle(
        "H2Style",
        parent=styles["Normal"],
        fontName="Helvetica-Bold",
        fontSize=12,
        leading=16,
        textColor=accent,
        spaceBefore=8,
        spaceAfter=4,
        keepWithNext=True
    )

    body_style = ParagraphStyle(
        "BodyText",
        parent=styles["Normal"],
        fontName="Helvetica",
        fontSize=9.5,
        leading=14,
        textColor=colors.HexColor("#1e293b"),
        spaceAfter=6
    )

    bullet_style = ParagraphStyle(
        "BulletText",
        parent=styles["Normal"],
        fontName="Helvetica",
        fontSize=9,
        leading=13.5,
        textColor=colors.HexColor("#334155"),
        spaceAfter=4
    )

    box_text = ParagraphStyle(
        "BoxText",
        parent=styles["Normal"],
        fontName="Helvetica",
        fontSize=9.5,
        leading=14,
        textColor=primary
    )

    table_header = ParagraphStyle(
        "TableHeader",
        parent=styles["Normal"],
        fontName="Helvetica-Bold",
        fontSize=8.5,
        leading=11,
        textColor=primary
    )

    table_cell = ParagraphStyle(
        "TableCell",
        parent=styles["Normal"],
        fontName="Helvetica",
        fontSize=8.5,
        leading=11.5,
        textColor=primary
    )

    story = []

    # ==================== COVER PAGE ====================
    story.append(Spacer(1, 25))
    story.append(Paragraph("WEBSITE CAPABILITIES & USER GUIDE", ParagraphStyle("Badge", fontName="Helvetica-Bold", fontSize=10, textColor=accent, spaceAfter=8)))
    story.append(Paragraph("What Can a User Do on LifeLink?", cover_title))
    story.append(Paragraph("A Plain-English, Comprehensive Walkthrough of Every Screen, Feature, and User Flow", cover_subtitle))
    story.append(HRFlowable(width="100%", thickness=3, color=accent, spaceAfter=20))

    story.append(Paragraph("<b>Target Audience:</b> Patients, Family Attendants, Voluntary Donors, Hospital Staff, Lab Technicians, Evaluators", body_style))
    story.append(Paragraph("<b>Focus:</b> User Experience, Screen Actions, Visual Controls, and Interactive Workflows (No Code / No Backend Jargon)", body_style))
    story.append(Paragraph(f"<b>Document Date:</b> {datetime.now().strftime('%B %d, %Y')}", body_style))
    story.append(Spacer(1, 15))

    # Executive Overview Callout
    intro_html = (
        "<b>What is LifeLink at a glance?</b><br/>"
        "LifeLink is a centralized emergency website that replaces frantic phone calls and chaotic WhatsApp messages during medical crises. "
        "Whether you are a desperate family member seeking rare blood for a patient, a healthy citizen wanting to donate blood, "
        "an ER doctor monitoring local trauma cases, or a citizen needing an urgent ambulance—this single website connects everyone "
        "in real time on an interactive city map."
    )
    intro_table = Table([[Paragraph(intro_html, box_text)]], colWidths=[letter[0] - 108])
    intro_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor("#f0fdf4")),
        ('BOX', (0, 0), (-1, -1), 1, emerald),
        ('TOPPADDING', (0, 0), (-1, -1), 10),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 10),
        ('LEFTPADDING', (0, 0), (-1, -1), 12),
        ('RIGHTPADDING', (0, 0), (-1, -1), 12),
    ]))
    story.append(intro_table)

    story.append(Spacer(1, 20))
    story.append(Paragraph("<b>Summary of User Personas & What They Can Do:</b>", h2_style))

    persona_rows = [
        ["User Persona", "Immediate Need / Role", "What They Do On This Website"],
        ["Patient Attendant", "Needs blood or emergency resource fast", "Fills the 1-minute Emergency Request form; tracks progress live from 'Matching' to 'Confirmed'; gets direct phone & GPS directions."],
        ["Voluntary Donor", "Wants to help without spam calls", "Toggles availability 'ON/OFF'; sets travel radius (e.g. 10 km); accepts live emergency dispatches while keeping personal phone number hidden."],
        ["Hospital Doctor / ER", "Triage & emergency coordination", "Monitors active critical trauma cases across the city; requests emergency blood or life-support ambulances for arriving patients."],
        ["Blood Bank Technician", "Managing daily inventory", "Updates live units for Packed RBC, Platelets, Plasma, and Whole Blood across 8 blood groups with 1-click '+' and '-' buttons."],
        ["General Public", "Needs emergency logistics", "Searches 24x7 stocked pharmacies for rare coagulants/drugs; dispatches nearby Basic/Advanced Life Support ambulances; dials SOS 108."]
    ]
    persona_table = Table([[Paragraph(c, table_header if i == 0 else table_cell) for c in row] for i, row in enumerate(persona_rows)], colWidths=[110, 130, 260])
    persona_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor("#f1f5f9")),
        ('GRID', (0, 0), (-1, -1), 0.5, border_color),
        ('TOPPADDING', (0, 0), (-1, -1), 4),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
    ]))
    story.append(persona_table)

    story.append(PageBreak())

    # ==================== CHAPTER 1 ====================
    story.append(Paragraph("1. The Homepage — The Emergency Hub", h1_style))
    story.append(HRFlowable(width="100%", thickness=1, color=colors.HexColor("#e2e8f0"), spaceAfter=10))

    story.append(Paragraph(
        "When any visitor opens the website, they are greeted by a distraction-free, high-contrast emergency screen designed for quick decisions under stress.",
        body_style
    ))

    story.append(Paragraph("<b>Key Elements on the Homepage:</b>", h2_style))
    story.append(Paragraph("&bull; <b>Two Giant Call-to-Action Buttons:</b><br/>"
                           "  - <b>'I NEED HELP' (Red Button):</b> Clicked by family members or attendants in emergency. Takes you straight to the blood & resource request form.<br/>"
                           "  - <b>'I CAN HELP' (Green Button):</b> Clicked by registered or new voluntary donors ready to donate blood in their neighborhood.", bullet_style))
    story.append(Paragraph("&bull; <b>Live Emergency Ticker:</b> Displays real-time critical requests currently pending in the city (e.g., <i>'Patient Rahul Sharma: 2 units O+ Packed RBC needed at AIIMS'</i>). Visitors can click any card to see its live coordination status.", bullet_style))
    story.append(Paragraph("&bull; <b>One-Click Resource Directory:</b> Quick visual shortcut cards for <b>Blood Banks</b> (4 verified), <b>Hospitals</b> (Apex centers), <b>Ambulances</b> (on-duty fleet), <b>Pharmacies</b> (24x7 stocked), <b>Volunteers</b>, and the <b>Radar Map</b>.", bullet_style))
    story.append(Paragraph("&bull; <b>SOS 108 Hotline Button:</b> Always visible in the top header for immediate telephone connection to government emergency services.", bullet_style))

    story.append(Spacer(1, 8))

    # ==================== CHAPTER 2 ====================
    story.append(Paragraph("2. Creating an Emergency Request ('I Need Help')", h1_style))
    story.append(HRFlowable(width="100%", thickness=1, color=colors.HexColor("#e2e8f0"), spaceAfter=10))

    story.append(Paragraph(
        "When a user clicks <b>'I NEED HELP'</b>, they are taken to a streamlined form that collects only vital medical and location details:",
        body_style
    ))

    form_steps = [
        ("Step 1: Patient Information", "Enter patient's name, choose their exact Blood Group (O+, O-, A+, A-, B+, B-, AB+, AB-), pick the specific Component required (Packed RBC, Platelets, Plasma, Whole Blood), and state the number of units required (e.g., 2 units)."),
        ("Step 2: Hospital Selection", "Select the medical facility (e.g., AIIMS Hospital, Capital Hospital, Apollo, KIMS). The system automatically maps the GPS coordinates of that facility."),
        ("Step 3: Urgency Level & Deadline", "Select between <i>Normal</i> (within 24 hrs), <i>Urgent</i> (6-12 hrs), or <i>Critical</i> (immediate, under 2 hrs). Enter the deadline in hours and an attendant's phone number for receiving delivery."),
        ("Step 4: Click 'Create Emergency Request'", "The moment you click submit, the website generates a unique tracking code (like <b>#LL-2841</b>) and instantly notifies nearby blood banks and eligible volunteers.")
    ]
    for title, desc in form_steps:
        story.append(Paragraph(f"&bull; <b>{title}:</b> {desc}", bullet_style))

    story.append(Spacer(1, 8))

    # ==================== CHAPTER 3 ====================
    story.append(Paragraph("3. The Live Request Tracker — The Requester's Cockpit", h1_style))
    story.append(HRFlowable(width="100%", thickness=1, color=colors.HexColor("#e2e8f0"), spaceAfter=10))

    story.append(Paragraph(
        "Once the request is submitted, the user is redirected to a live interactive coordination dashboard. Here is what they see and can do:",
        body_style
    ))

    story.append(Paragraph("<b>A. The 5-Stage Live Progress Stepper:</b>", h2_style))
    story.append(Paragraph(
        "An animated progress bar visually moves through 5 stages as emergency actions take place:<br/>"
        "1. <b>Matching:</b> The system scans all blood banks and voluntary donors in the city.<br/>"
        "2. <b>Blood Bank Contacted:</b> Alerts sent to verified blood centres with stock.<br/>"
        "3. <b>Volunteer Response:</b> A nearby donor accepts the dispatch.<br/>"
        "4. <b>Resource Confirmed:</b> Units reserved and in transit to the hospital.<br/>"
        "5. <b>Completed:</b> Transfusion delivered and patient secured.",
        bullet_style
    ))

    story.append(Paragraph("<b>B. Ranked Resource Cards (The Best Matches First):</b>", h2_style))
    story.append(Paragraph(
        "The website displays a prioritized list of available options sorted by match quality:<br/>"
        "&bull; <b>Match Score %:</b> e.g., <i>AIIMS Blood Center — 99% Match</i> (closest, stock verified) vs <i>Capital Hospital — 94.7% Match</i>.<br/>"
        "&bull; <b>Distance:</b> Tells the user exactly how far away the resource is (e.g., <i>4.2 km away</i>).<br/>"
        "&bull; <b>Direct Action Buttons on Every Card:</b><br/>"
        "  - <b>[CALL] Button:</b> One tap dials the blood bank or opens a secure masked call to the volunteer.<br/>"
        "  - <b>[DIRECTIONS] Button:</b> Opens Google Maps with turn-by-turn driving directions straight to that blood bank.",
        bullet_style
    ))

    story.append(PageBreak())

    # ==================== CHAPTER 4 ====================
    story.append(Paragraph("4. The Emergency Radar Map — City-Wide Geo Navigation", h1_style))
    story.append(HRFlowable(width="100%", thickness=1, color=colors.HexColor("#e2e8f0"), spaceAfter=10))

    story.append(Paragraph(
        "LifeLink includes a full-screen interactive satellite and street map powered by OpenStreetMap and Leaflet:",
        body_style
    ))

    story.append(Paragraph("<b>What Can the User Do on the Map?</b>", h2_style))
    story.append(Paragraph("&bull; <b>See Color-Coded Pins:</b><br/>"
                           "  - 🩸 <b>Red Pins:</b> Verified Blood Banks with stock summary.<br/>"
                           "  - 🏥 <b>Indigo Pins:</b> Apex Hospitals with ICU bed counts.<br/>"
                           "  - 🚑 <b>Amber Pins:</b> Ambulances (shows if Available or on a trip).<br/>"
                           "  - ❤️ <b>Emerald Pins:</b> Registered Voluntary Donors ready to help.<br/>"
                           "  - 🆘 <b>Pulsing Red Marker:</b> The exact hospital where the patient is waiting.", bullet_style))
    story.append(Paragraph("&bull; <b>Click Any Marker for a Popup Card:</b> Shows institution name, exact street address, phone number, operating hours (e.g. 24x7), and a <b>'Get Directions'</b> shortcut.", bullet_style))
    story.append(Paragraph("&bull; <b>Filter by Resource:</b> Want to see only Ambulances? Or only Blood Banks? Simply click the filter buttons at the top of the map.", bullet_style))
    story.append(Paragraph("&bull; <b>Filter by Blood Group:</b> Select 'O-' from the map filter, and the map will highlight only centers and donors carrying O- blood.", bullet_style))

    story.append(Spacer(1, 8))

    # ==================== CHAPTER 5 ====================
    story.append(Paragraph("5. The Volunteer Portal ('I Can Help') — Privacy-First Giving", h1_style))
    story.append(HRFlowable(width="100%", thickness=1, color=colors.HexColor("#e2e8f0"), spaceAfter=10))

    story.append(Paragraph(
        "Many willing donors avoid registering on blood websites because they fear spam calls or privacy leaks. "
        "LifeLink solves this with a privacy-first volunteer interface:",
        body_style
    ))

    story.append(Paragraph("<b>Volunteer User Features:</b>", h2_style))
    story.append(Paragraph("&bull; <b>Anonymous Display Names:</b> Donors use handles like <i>Rohan_M</i> or <i>Ananya_K</i>. Their real phone numbers and email addresses are NEVER displayed publicly on the website.", bullet_style))
    story.append(Paragraph("&bull; <b>Emergency Availability Switch:</b> A simple toggle switch. If you are sick, working, or out of town, toggle it OFF. You will not receive emergency alerts until you turn it back ON.", bullet_style))
    story.append(Paragraph("&bull; <b>Dispatch Radius Slider:</b> Drag a slider from 2 km to 30 km. You only get alerts for patients within your chosen travel comfort zone.", bullet_style))
    story.append(Paragraph("&bull; <b>Incoming Emergency Alert Queue:</b> When a compatible patient nearby needs blood, a red emergency card appears on your screen showing patient name, hospital, and units needed.", bullet_style))
    story.append(Paragraph("&bull; <b>[ACCEPT DISPATCH] / [DECLINE] Buttons:</b><br/>"
                           "  - Clicking <b>Accept</b> notifies the requester instantly that a donor is on the way and generates a secure bridge token.<br/>"
                           "  - Clicking <b>Decline</b> dismisses the card gracefully without penalty.", bullet_style))

    story.append(Spacer(1, 8))

    # ==================== CHAPTER 6 ====================
    story.append(Paragraph("6. Hospital & Blood Bank Dashboards — Staff Views", h1_style))
    story.append(HRFlowable(width="100%", thickness=1, color=colors.HexColor("#e2e8f0"), spaceAfter=10))

    story.append(Paragraph("<b>A. Hospital Triage Portal:</b>", h2_style))
    story.append(Paragraph(
        "Designed for ER doctors and medical coordinators:<br/>"
        "&bull; <b>Live Triage Counters:</b> Shows Active Requests, Critical Trauma Cases, Blood Requests, and Available Ambulances at a glance.<br/>"
        "&bull; <b>Today's Throughput Stats:</b> Total requests received, successfully resolved, and currently pending.<br/>"
        "&bull; <b>Live Triage Feed:</b> ER staff can click any incoming patient to monitor the status of their blood unit in transit.",
        bullet_style
    ))

    story.append(Paragraph("<b>B. Blood Bank Inventory Hub:</b>", h2_style))
    story.append(Paragraph(
        "Designed for certified blood bank technicians (aligned with national e-RaktKosh standards):<br/>"
        "&bull; <b>Multi-Component Tabs:</b> Switch between <b>Packed RBC, Platelets, Plasma, and Whole Blood</b>.<br/>"
        "&bull; <b>8 Blood Group Tiles:</b> Displays current units for O+, O-, A+, A-, B+, B-, AB+, AB-.<br/>"
        "&bull; <b>1-Click Stock Updates:</b> Technicians click <b>[+]</b> when blood is collected and <b>[-]</b> when blood is issued. The updated stock updates across the entire city instantly without reloading.",
        bullet_style
    ))

    story.append(PageBreak())

    # ==================== CHAPTER 7 ====================
    story.append(Paragraph("7. Ambulance Fleet & 24x7 Pharmacy Modules", h1_style))
    story.append(HRFlowable(width="100%", thickness=1, color=colors.HexColor("#e2e8f0"), spaceAfter=10))

    story.append(Paragraph("<b>A. Ambulance Dispatch Directory:</b>", h2_style))
    story.append(Paragraph(
        "Allows users facing trauma or transit emergencies to locate nearby emergency vehicles:<br/>"
        "&bull; <b>Vehicle Details:</b> Shows vehicle number (e.g. <i>OD-02-AX-1081</i>), verified driver name, and base location.<br/>"
        "&bull; <b>Type Distinction:</b> Differentiates between <i>Advanced Life Support (ALS)</i> (for ventilators/cardiac emergencies) and <i>Basic Life Support (BLS)</i>.<br/>"
        "&bull; <b>[REQUEST DISPATCH] Button:</b> Sends a dispatch signal and triggers GPS tracking.<br/>"
        "&bull; <b>[Secure Driver Call] Button:</b> One-click telephone dial to the on-duty driver.",
        bullet_style
    ))

    story.append(Paragraph("<b>B. Emergency Pharmacy & Medication Network:</b>", h2_style))
    story.append(Paragraph(
        "In critical surgeries, specific coagulants and medications (like Heparin, Tranexamic Acid, Albumin, IV Saline) are as urgent as blood:<br/>"
        "&bull; <b>Search Bar:</b> Type any drug name to filter pharmacies that recently reported it in stock.<br/>"
        "&bull; <b>24x7 Operating Badge:</b> Clearly tags round-the-clock facilities vs day-shift pharmacies.<br/>"
        "&bull; <b>Telemetry Freshness Timestamp:</b> Shows <i>'Reported 8 mins ago'</i> so users know how fresh the data is, avoiding wasted travel.<br/>"
        "&bull; <b>Direct Call Shortcut:</b> Lets users confirm with the pharmacist with one tap before driving.",
        bullet_style
    ))

    story.append(Spacer(1, 10))

    # ==================== CHAPTER 8 ====================
    story.append(Paragraph("8. Complete Step-by-Step User Journey", h1_style))
    story.append(HRFlowable(width="100%", thickness=1, color=colors.HexColor("#e2e8f0"), spaceAfter=10))

    journey_steps = [
        ["Phase", "User Action", "What Happens on Screen"],
        ["1. Distress", "Family arrives at AIIMS ER; doctor requests 2 units O+ Packed RBC.", "Attendant opens LifeLink on mobile phone and taps red 'I NEED HELP' button."],
        ["2. Submission", "Selects 'O+', 'Packed RBC', '2 Units', 'AIIMS', urgency 'Critical'.", "Taps 'Create Emergency Request'. Request #LL-2841 is created instantly."],
        ["3. Matching", "User looks at Request Tracker screen.", "Matching Engine displays AIIMS Blood Bank (99% match, 0 km) and Capital Hospital (94.7% match, 5.9 km) with [CALL] & [DIRECTIONS]."],
        ["4. Alert", "Eligible volunteer Rohan_M opens the Volunteer Portal.", "A red emergency dispatch card pops up on his screen. He reviews it and clicks 'ACCEPT DISPATCH'."],
        ["5. Live Update", "Attendant looks at their phone screen.", "Progress stepper automatically transitions from 'Matching' to 'Volunteer Response' live without refreshing."],
        ["6. Resolution", "Blood is delivered to ICU-2 and verified by doctors.", "Status marks 'Completed'. The entire emergency was coordinated in minutes."]
    ]
    journey_table = Table([[Paragraph(c, table_header if i == 0 else table_cell) for c in row] for i, row in enumerate(journey_steps)], colWidths=[65, 175, 260])
    journey_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor("#f1f5f9")),
        ('GRID', (0, 0), (-1, -1), 0.5, border_color),
        ('TOPPADDING', (0, 0), (-1, -1), 4),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
    ]))
    story.append(journey_table)

    story.append(Spacer(1, 15))
    story.append(Paragraph("<b>Summary:</b> LifeLink empowers everyday citizens, emergency coordinators, and healthcare professionals with clarity, speed, and privacy when seconds matter most.", ParagraphStyle("Ending", fontName="Helvetica-Bold", fontSize=9.5, textColor=primary)))

    # Build PDF
    doc.build(story, canvasmaker=NumberedCanvas)
    print(f"[SUCCESS] User Guide PDF generated successfully at: {pdf_path}")

if __name__ == "__main__":
    out_dir = r"C:\Users\kamal\.gemini\antigravity\scratch\lifelink"
    pdf_file = os.path.join(out_dir, "LifeLink_Website_User_Guide_and_Features.pdf")
    generate_user_guide(pdf_file)
