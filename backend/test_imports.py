try:
    from fpdf import FPDF
    print("FPDF Import Successful")
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    pdf.cell(200, 10, txt="Test PDF", ln=True, align='C')
    print("PDF initialization Successful")
except Exception as e:
    print(f"FPDF Error: {e}")

try:
    from ml_model import predictor
    print("ML Model Import Successful")
except Exception as e:
    print(f"ML Model Error: {e}")

try:
    from report_engine import report_engine
    print("Report Engine Import Successful")
except Exception as e:
    print(f"Report Engine Error: {e}")
