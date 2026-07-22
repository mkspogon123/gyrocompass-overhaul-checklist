"""
PDF Report Generator for Gyrocompass Overhaul Checklist
"""

from datetime import datetime
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib import colors

class ReportGenerator:
    def __init__(self, page_size=letter):
        self.page_size = page_size
        self.margin = 0.5 * inch
        
    def generate(self, file_path, technician, equipment_id, start_date, checklist_data):
        doc = SimpleDocTemplate(
            file_path,
            pagesize=self.page_size,
            rightMargin=self.margin,
            leftMargin=self.margin,
            topMargin=self.margin,
            bottomMargin=self.margin,
            title="Gyrocompass Overhaul Report"
        )
        
        elements = []
        styles = getSampleStyleSheet()
        
        title_style = ParagraphStyle(
            'CustomTitle',
            parent=styles['Heading1'],
            fontSize=24,
            textColor=colors.HexColor('#003366'),
            spaceAfter=30,
            alignment=TA_CENTER,
            fontName='Helvetica-Bold'
        )
        
        heading_style = ParagraphStyle(
            'CustomHeading',
            parent=styles['Heading2'],
            fontSize=14,
            textColor=colors.HexColor('#003366'),
            spaceAfter=12,
            spaceBefore=12,
            fontName='Helvetica-Bold'
        )
        
        elements.append(Paragraph("GYROCOMPASS OVERHAUL REPORT", title_style))
        elements.append(Spacer(1, 0.2 * inch))
        
        completion_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        header_data = [
            ["Technician Name:", technician],
            ["Equipment ID:", equipment_id],
            ["Start Date:", start_date],
            ["Completion Date:", completion_date],
        ]
        
        header_table = Table(header_data, colWidths=[2 * inch, 4 * inch])
        header_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (0, -1), colors.HexColor('#E8F0F5')),
            ('TEXTCOLOR', (0, 0), (-1, -1), colors.black),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, -1), 10),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
            ('TOPPADDING', (0, 0), (-1, -1), 6),
            ('GRID', (0, 0), (-1, -1), 1, colors.grey),
        ]))
        
        elements.append(header_table)
        elements.append(Spacer(1, 0.3 * inch))
        
        elements.append(Paragraph("CHECKLIST DETAILS", heading_style))
        
        for category_name, items in checklist_data.items():
            elements.append(Paragraph(f"• {category_name}", styles['Heading3']))
            
            item_data = [["Item", "Status", "Notes"]]
            
            for item in items:
                status = "✓ Completed" if item['completed'] else "○ Incomplete"
                notes = item['notes'] if item['notes'] else "-"
                item_data.append([
                    item['name'],
                    status,
                    notes
                ])
            
            col_widths = [3.5 * inch, 1.2 * inch, 1.8 * inch]
            item_table = Table(item_data, colWidths=col_widths)
            
            item_table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#003366')),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
                ('ALIGN', (1, 0), (1, -1), 'CENTER'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, -1), 9),
                ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
                ('TOPPADDING', (0, 0), (-1, -1), 6),
                ('GRID', (0, 0), (-1, -1), 1, colors.grey),
                ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#F0F5FA')]),
            ]))
            
            elements.append(item_table)
            elements.append(Spacer(1, 0.2 * inch))
        
        elements.append(Spacer(1, 0.2 * inch))
        elements.append(Paragraph("SUMMARY", heading_style))
        
        total_items = sum(len(items) for items in checklist_data.values())
        completed_items = sum(1 for items in checklist_data.values() for item in items if item['completed'])
        completion_percentage = (completed_items / total_items * 100) if total_items > 0 else 0
        
        summary_data = [
            ["Total Items:", str(total_items)],
            ["Completed Items:", str(completed_items)],
            ["Incomplete Items:", str(total_items - completed_items)],
            ["Completion Percentage:", f"{completion_percentage:.1f}%"],
        ]
        
        summary_table = Table(summary_data, colWidths=[2.5 * inch, 2 * inch])
        summary_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (0, -1), colors.HexColor('#E8F0F5')),
            ('TEXTCOLOR', (0, 0), (-1, -1), colors.black),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, -1), 10),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
            ('TOPPADDING', (0, 0), (-1, -1), 8),
            ('GRID', (0, 0), (-1, -1), 1, colors.grey),
        ]))
        
        elements.append(summary_table)
        elements.append(Spacer(1, 0.4 * inch))
        
        elements.append(Paragraph("SIGN-OFF", heading_style))
        
        signature_data = [
            ["Technician Signature:", "___________________________", "Date: _______________"],
            ["Supervisor Review:", "___________________________", "Date: _______________"],
        ]
        
        signature_table = Table(signature_data, colWidths=[2 * inch, 2.5 * inch, 2 * inch])
        signature_table.setStyle(TableStyle([
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTSIZE', (0, 0), (-1, -1), 10),
            ('TOPPADDING', (0, 0), (-1, -1), 20),
        ]))
        
        elements.append(signature_table)
        
        elements.append(Spacer(1, 0.3 * inch))
        footer_text = f"Report generated on {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} by Gyrocompass Overhaul System"
        elements.append(Paragraph(footer_text, ParagraphStyle(
            'Footer',
            parent=styles['Normal'],
            fontSize=8,
            textColor=colors.grey,
            alignment=TA_CENTER
        )))
        
        doc.build(elements)