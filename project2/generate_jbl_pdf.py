from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle

def create_jbl_comparison_pdf(output_path):
    doc = SimpleDocTemplate(output_path, pagesize=A4)
    elements = []
    
    styles = getSampleStyleSheet()
    title_style = ParagraphStyle(
        'MainTitle',
        parent=styles['Heading1'],
        fontSize=24,
        spaceAfter=30,
        alignment=1,
        textColor=colors.HexColor("#FF6600") # JBL Orange
    )
    
    # Title
    elements.append(Paragraph("JBL Amazon Japan Product Comparison", title_style))
    elements.append(Paragraph("Market Analysis & Specification Overview (2024-2025)", styles['Normal']))
    elements.append(Spacer(1, 20))
    
    # Product Data
    data = [
        ["Product Name", "Approx. Price (JPY)", "Rating", "Key Features"],
        ["JBL Charge 6", "¥21,480", "4.7 / 5", "AI Sound Boost, 28h Battery, IP67"],
        ["JBL Charge 5", "¥11,616", "4.1 / 5", "Best Value, Rugged Design, Powerbank function"],
        ["JBL Flip 6", "¥8,091", "4.5 / 5", "Compact, Dual Passive Radiators, IP67"],
        ["JBL Wave Buds 2", "¥2,999", "4.4 / 5", "Budget Choice, ANC Support, 40h Playtime"],
        ["JBL Authentics 300", "¥52,727", "4.8 / 5", "Premium Retro, Wi-Fi/Alexa/Google, Multi-room"],
        ["JBL Xtreme 4", "¥25,800", "4.6 / 5", "Powerful Bass, Shoulder Strap, Replaceable Battery"],
    ]
    
    # Create Table
    table = Table(data, colWidths=[120, 100, 70, 200])
    
    # Add Style to Table
    style = TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor("#FF6600")),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 12),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('FONTSIZE', (0, 1), (-1, -1), 10),
    ])
    table.setStyle(style)
    
    elements.append(table)
    elements.append(Spacer(1, 30))
    
    # Summary Paragraphs
    elements.append(Paragraph("Market Summary:", styles['Heading2']))
    summary_text = """
    Based on our analysis of Amazon.co.jp listings, JBL dominates the portable audio segment in Japan. 
    The <b>Charge</b> series remains the highest-selling line due to its balance of durability and sound quality. 
    Newer models like the <b>Authentics 300</b> satisfy the growing demand for premium, smart home integrated audio.
    """
    elements.append(Paragraph(summary_text, styles['Normal']))
    
    # Build PDF
    doc.build(elements)
    print(f"PDF successfully created at {output_path}")

if __name__ == "__main__":
    create_jbl_comparison_pdf("JBL_Amazon_Japan_Comparison.pdf")
