from fpdf import FPDF
from database import get_stats

def generate_pdf():
    stats = get_stats()
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=14)
    pdf.cell(200, 10, txt="Reporte de Auditoría de Phishing", ln=True, align='C')
    pdf.ln(10)
    for k, v in stats.items():
        pdf.cell(200, 10, txt=f"{k.capitalize()}: {v}", ln=True)
    pdf.output("reporte_phishing.pdf")