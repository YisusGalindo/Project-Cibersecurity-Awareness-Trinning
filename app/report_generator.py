from fpdf import FPDF
from database import get_stats
from datetime import datetime
import os

class PhishingReportPDF(FPDF):
    def header(self):
        self.set_font('Arial', 'B', 16)
        self.cell(0, 10, 'REPORTE DE AUDITORÍA DE PHISHING', 0, 1, 'C')
        self.set_font('Arial', '', 10)
        self.cell(0, 10, f'Generado el: {datetime.now().strftime("%d/%m/%Y %H:%M:%S")}', 0, 1, 'C')
        self.ln(10)

    def footer(self):
        self.set_y(-15)
        self.set_font('Arial', 'I', 8)
        self.cell(0, 10, f'Página {self.page_no()}', 0, 0, 'C')

def generate_pdf():
    stats = get_stats()
    
    pdf = PhishingReportPDF()
    pdf.add_page()
    
    # Resumen ejecutivo
    pdf.set_font("Arial", 'B', 14)
    pdf.cell(0, 10, "RESUMEN EJECUTIVO", 0, 1, 'L')
    pdf.ln(5)
    
    pdf.set_font("Arial", '', 11)
    total_events = sum(stats[action] for action in ['clicked', 'ignored', 'reported'])
    
    if total_events > 0:
        click_rate = (stats['clicked'] / total_events) * 100
        report_rate = (stats['reported'] / total_events) * 100
        ignore_rate = (stats['ignored'] / total_events) * 100
        
        pdf.cell(0, 8, f"• Total de eventos registrados: {total_events}", 0, 1)
        pdf.cell(0, 8, f"• Usuarios que cayeron en el phishing: {stats['clicked']} ({click_rate:.1f}%)", 0, 1)
        pdf.cell(0, 8, f"• Usuarios que reportaron el correo: {stats['reported']} ({report_rate:.1f}%)", 0, 1)
        pdf.cell(0, 8, f"• Usuarios que ignoraron el correo: {stats['ignored']} ({ignore_rate:.1f}%)", 0, 1)
    else:
        pdf.cell(0, 8, "No se han registrado eventos aún.", 0, 1)
    
    pdf.ln(10)
    
    # Resultados por departamento
    pdf.set_font("Arial", 'B', 14)
    pdf.cell(0, 10, "RESULTADOS POR DEPARTAMENTO", 0, 1, 'L')
    pdf.ln(5)
    
    pdf.set_font("Arial", 'B', 10)
    pdf.cell(60, 8, "DEPARTAMENTO", 1, 0, 'C')
    pdf.cell(30, 8, "CAYERON", 1, 0, 'C')
    pdf.cell(30, 8, "IGNORARON", 1, 0, 'C')
    pdf.cell(30, 8, "REPORTARON", 1, 0, 'C')
    pdf.cell(30, 8, "TOTAL", 1, 1, 'C')
    
    pdf.set_font("Arial", '', 9)
    
    for dept in stats['departments']:
        dept_data = stats['by_department'][dept]
        dept_total = sum(dept_data.values())
        
        pdf.cell(60, 7, dept, 1, 0, 'L')
        pdf.cell(30, 7, str(dept_data['clicked']), 1, 0, 'C')
        pdf.cell(30, 7, str(dept_data['ignored']), 1, 0, 'C')
        pdf.cell(30, 7, str(dept_data['reported']), 1, 0, 'C')
        pdf.cell(30, 7, str(dept_total), 1, 1, 'C')
    
    pdf.ln(10)
    
    # Recomendaciones
    pdf.set_font("Arial", 'B', 14)
    pdf.cell(0, 10, "RECOMENDACIONES", 0, 1, 'L')
    pdf.ln(5)
    
    pdf.set_font("Arial", '', 11)
    recommendations = [
        "1. Implementar capacitación adicional en departamentos con alta tasa de clics",
        "2. Reconocer a los departamentos con alta tasa de reporte de correos sospechosos",
        "3. Establecer políticas claras de verificación antes de hacer clic en enlaces",
        "4. Realizar campañas de concientización regulares",
        "5. Implementar filtros de correo más estrictos"
    ]
    
    for rec in recommendations:
        pdf.cell(0, 8, rec, 0, 1)
    
    # Guardar el archivo
    filename = f"reporte_phishing_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
    pdf.output(filename)
    
    return filename