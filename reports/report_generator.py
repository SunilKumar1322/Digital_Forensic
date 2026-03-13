from fpdf import FPDF

def generate_report(evidence, output_file="forensic_report.pdf"):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)

    pdf.cell(200, 10, "Digital Forensic Evidence Report", ln=True)
    pdf.cell(200, 10, f"File Name: {evidence['file_name']}", ln=True)
    pdf.cell(200, 10, f"File Path: {evidence['file_path']}", ln=True)
    pdf.cell(200, 10, f"SHA256 Hash: {evidence['sha256_hash']}", ln=True)
    pdf.cell(200, 10, f"BLAKE3 Hash: {evidence['blake3_hash']}", ln=True)

    pdf.output(output_file)
    print(f"Report generated: {output_file}")
