from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Image, Table, TableStyle, Spacer, PageBreak
)
from django.conf import settings
from django.contrib.staticfiles.finders import find
from mysite.models import Orders
import os

def create_bill(order_id, output_path):
    # --- 1. Fetch your order ------------------------------------------------
    order = Orders.objects.get(pk=order_id)

    # --- 2. Document setup --------------------------------------------------
    doc = SimpleDocTemplate(
        output_path,
        pagesize=A4,
        leftMargin=20*mm, rightMargin=20*mm,
        topMargin=20*mm, bottomMargin=20*mm,
    )
    styles = getSampleStyleSheet()

    # Define custom styles BEFORE they are used
    styles.add( ParagraphStyle(name="CenterHeading",
                               fontSize=14, leading=16, alignment=1) )  # Adjusted font size to 14
    styles.add( ParagraphStyle(name="Small", fontSize=8, leading=10) )
    styles.add( ParagraphStyle(name="Bold", parent=styles["Normal"], fontName="Helvetica-Bold") )
    styles.add( ParagraphStyle(name="NormalCenter", parent=styles["Normal"], alignment=1) )
    styles.add( ParagraphStyle(name="RightBold", parent=styles["Normal"], alignment=2) )
    styles.add( ParagraphStyle(name="NormalRight", parent=styles["Normal"], alignment=2) )
    # Style for table headers
    styles.add( ParagraphStyle(name="TableHeader", parent=styles["Normal"], fontName="Helvetica-Bold", alignment=1) )
    # Style for right-aligned table cell content (e.g., Amount)
    styles.add( ParagraphStyle(name="TableCellRight", parent=styles["Normal"], alignment=2) )
    styles.add(ParagraphStyle(name="CenterSmall", parent=styles["Small"], alignment=1))


    story = []

    # --- 3. Header: logo + company name + address/contact/GSTIN ------------
    # Logo (centered)
    logo_path = find('SVDS/media/logo.png')

    if logo_path and os.path.exists(logo_path):
        logo = Image(logo_path, width=15*mm, height=15*mm)
        logo.hAlign = 'CENTER'
        story.append(logo)
    else:
        # Optional: Add placeholder text if logo not found
        placeholder = Paragraph("<i>[Company Logo]</i>", styles["NormalCenter"])
        placeholder.hAlign = 'CENTER'
        story.append(placeholder)

    # Company name
    story.append( Paragraph("SVDS Goods & Transport", styles["CenterHeading"]) )
    # Address / contact
    addr = """123 Logistics Park, Industrial Area,<br/>
              Bhopal 462001, Madhya Pradesh<br/>
              Phone: +91 7551234567, +91 9999912345<br/>
              Email: svds@gmail.com<br/>
              GSTIN: 23ABCDE1234F1Z5"""
    story.append( Paragraph(addr, styles["NormalCenter"]) )
    story.append( Spacer(1, 12) )

    # --- 4. Title + Bill No -----------------------------------------------
    story.append( Paragraph("BILL", styles["CenterHeading"]) )
    story.append( Paragraph(f"Bill No.: SVDS {order.svds_bill_no}", styles["Bold"]) )
    story.append( Spacer(1, 12) )

    # --- 5. Consignor / Consignee Table ------------------------------------
    consignor_para = Paragraph(
        f"<b>Consignor:</b><br/>{order.consignor}<br/>{order.transit_from}", styles["Normal"]
    )
    consignee_para = Paragraph(
        f"<b>Consignee:</b><br/>{order.consignee}<br/>{order.transit_to}", styles["NormalRight"]
    )
    # Using a Table for consignor/consignee to push them to left/right
    party_table = Table(
        [[consignor_para, consignee_para]],
        # Adjust colWidths to provide enough space and control their horizontal spread
        # Total available width for this row is doc.width
        colWidths=[doc.width / 2, doc.width / 2],
    )
    party_table.setStyle(TableStyle([
        ("VALIGN", (0,0), (-1,-1), "TOP"),
        ("ALIGN",   (0,0), (0,0), "LEFT"),    # Consignor Left
        ("ALIGN",   (1,0), (1,0), "RIGHT"),   # Consignee Right
        ("LEFTPADDING",  (0,0), (0,0), 0),    # No left padding for consignor cell
        ("RIGHTPADDING", (0,0), (0,0), 0),   # No right padding for consignor cell
        ("LEFTPADDING",  (1,0), (1,0), 0),    # No left padding for consignee cell
        ("RIGHTPADDING", (1,0), (1,0), 0),   # No right padding for consignee cell
    ]))
    story.append(party_table)
    story.append(Spacer(1, 18)) # Add more space after consignor/consignee details

    # --- 6. Horizontal Consignment Details Table ---------------------------
    # Headers
    cons_header = [
        Paragraph("Packages", styles["TableHeader"]),
        Paragraph("Description", styles["TableHeader"]),
        Paragraph("Actual Weight (kg)", styles["TableHeader"]),
        Paragraph("Charged Weight (kg)", styles["TableHeader"]),
        Paragraph("Freight Charges (Rs)", styles["TableHeader"]),
        Paragraph("Amount (Rs)", styles["TableHeader"]), # New Amount column header
    ]

    # Data Row
    cons_data_row = [
        Paragraph(str(order.packages), styles["NormalCenter"]), # Center align packages
        Paragraph(order.description or "-", styles["Normal"]),
        Paragraph(str(order.actual_weight), styles["TableCellRight"]), # Right align weights
        Paragraph(str(order.charged_weight), styles["TableCellRight"]), # Right align weights
        Paragraph(f"{order.freight_charges:.2f}", styles["TableCellRight"]), # Right align charges
        Paragraph(f"{order.total_charge:.2f}", styles["TableCellRight"]), # Right align total amount
    ]

    cons_table_data = [cons_header, cons_data_row]

    # Calculate column widths dynamically based on available space
    # Divide doc.width by the number of columns (6) for equal distribution initially
    # You can adjust these widths based on expected content length
    col_widths = [doc.width / 6] * 6 # 6 columns, each taking 1/6th of doc.width
    # Adjust specific column widths if needed, e.g., description might need more space
    col_widths[1] = doc.width / 6 * 1.5 # Description gets 1.5 times the base width
    col_widths[0] = doc.width / 6 * 0.75 # Packages gets less
    col_widths[2] = doc.width / 6 * 0.9 # Actual weight
    col_widths[3] = doc.width / 6 * 0.9 # Charged weight
    col_widths[4] = doc.width / 6 * 1.0 # Freight charges
    col_widths[5] = doc.width / 6 * 1.0 # Amount

    cons_table = Table(cons_table_data, colWidths=col_widths)
    cons_table.setStyle(TableStyle([
        ("BACKGROUND", (0,0), (-1,0), colors.lightgrey), # Header background
        ("GRID",       (0,0), (-1,-1), 0.5, colors.grey),
        ("VALIGN",     (0,0), (-1,-1), "MIDDLE"),
        ("TOPPADDING", (0,0), (-1,-1), 6),
        ("BOTTOMPADDING", (0,0), (-1,-1), 6),
        # Alignments for data cells (headers are handled by ParagraphStyle)
        ("ALIGN",      (0,1), (0,-1), "CENTER"), # Packages data
        ("ALIGN",      (1,1), (1,-1), "LEFT"),   # Description data
        ("ALIGN",      (2,1), (-1,-1), "RIGHT"), # Weights, Charges, Amount data
    ]))
    story.append(cons_table)
    story.append(Spacer(1, 12)) # Space after the consignment table

    # --- 7. Liability Note and Total Charges -------------------------------
    # Place liability note and total charges side-by-side if space allows, or stack
    # For now, stack them to ensure they fit, as the cons_table now takes full width.

    liability = Paragraph(
        "<i>*Not Responsible for transport leakage, theft, natural "
        "disasters, accidents and damages for any claim.</i>",
        styles["Small"]
    )
    total_para = Paragraph(
        f"<b>Total: Rs. {order.total_charge:.2f}</b>",
        styles["RightBold"]
    )

    # We can use a table to put liability left and total right
    liability_total_table = Table(
        [[liability, total_para]],
        colWidths=[doc.width / 2, doc.width / 2]
    )
    liability_total_table.setStyle(TableStyle([
        ("VALIGN", (0,0), (-1,-1), "TOP"),
        ("ALIGN", (0,0), (0,0), "LEFT"),
        ("ALIGN", (1,0), (1,0), "RIGHT"),
    ]))
    story.append(liability_total_table)
    story.append( Spacer(1, 24) )


    # --- 8. Signatures -----------------------------------------------------
    sig_table = Table(
        [[Paragraph("Consignor Signature", styles["Normal"]),
          Paragraph("Receiver Signature", styles["Normal"])]],
        colWidths=[doc.width/4, doc.width/4]
    )
    sig_table.setStyle(TableStyle([
        ("ALIGN", (0,0), (0,0), "LEFT"),    # Consignor sig left
        ("ALIGN", (1,0), (1,0), "RIGHT"),   # Receiver sig right
        ("TOPPADDING",    (0,0), (-1,-1), 80),
    ]))
    story.append(sig_table)
    story.append( Spacer(1, 24) )

    # --- 9. Motto + footer note -------------------------------------------
    story.append( Paragraph(
        "<b>“Customer satisfaction is our motto.”</b>",
        ParagraphStyle("CenterItalic", parent=styles["Normal"], alignment=1, fontName="Helvetica-Oblique")
    ) )
    story.append( Spacer(1, 6) )
    story.append( Paragraph(
        "<small>Note: I agree to terms and conditions mentioned. "
        "*Subject to Bhopal Jurisdiction*</small>",
        styles["CenterSmall"]
    ) )

    # --- 10. Build ----------------------------------------------------------
    doc.build(story)