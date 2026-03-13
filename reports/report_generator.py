from fpdf import FPDF

def generate_report(evidence, metadata, memory_info, integrity_result, output_file="forensic_report.pdf"):
    pdf = FPDF()
    pdf.add_page()
    
    # Title
    pdf.set_font("Arial", 'B', size=16)
    pdf.cell(200, 10, "Digital Forensic Evidence Report", ln=True, align="C")
    pdf.ln(5)
    
    # Case Information Section
    pdf.set_font("Arial", 'B', size=14)
    pdf.cell(200, 10, "Case Information", ln=True)
    pdf.set_font("Arial", size=12)
    pdf.cell(200, 8, f"Case ID: {evidence.get('case_id', 'N/A')}", ln=True)
    pdf.cell(200, 8, f"Location: {evidence.get('location', 'N/A')}", ln=True)
    pdf.cell(200, 8, f"Officer ID: {evidence.get('officer_id', 'N/A')}", ln=True)
    pdf.ln(3)

    # Evidence Information Section
    pdf.set_font("Arial", 'B', size=14)
    pdf.cell(200, 10, "Evidence Information", ln=True)
    pdf.set_font("Arial", size=12)
    pdf.cell(200, 8, f"File Name: {evidence['file_name']}", ln=True)
    pdf.cell(200, 8, f"File Path: {evidence['file_path']}", ln=True)
    pdf.cell(200, 8, f"File Size: {evidence['file_size']} bytes", ln=True)
    pdf.ln(3)

    # Hash Values Section
    pdf.set_font("Arial", 'B', size=14)
    pdf.cell(200, 10, "Hash Values", ln=True)
    pdf.set_font("Arial", size=12)
    pdf.cell(200, 8, f"SHA256 Hash: {evidence['sha256_hash']}", ln=True)
    pdf.cell(200, 8, f"BLAKE3 Hash: {evidence['blake3_hash']}", ln=True)
    pdf.ln(3)
    
    # Metadata Section
    pdf.set_font("Arial", 'B', size=14)
    pdf.cell(200, 10, "Metadata", ln=True)
    pdf.set_font("Arial", size=12)
    pdf.cell(200, 8, f"Created Time: {metadata.get('created_time', 'N/A')}", ln=True)
    pdf.cell(200, 8, f"Modified Time: {metadata.get('modified_time', 'N/A')}", ln=True)
    pdf.cell(200, 8, f"Access Time: {metadata.get('access_time', 'N/A')}", ln=True)
    pdf.ln(3)
    
    # System Information Section
    pdf.set_font("Arial", 'B', size=14)
    pdf.cell(200, 10, "System Information", ln=True)
    pdf.set_font("Arial", size=12)
    pdf.cell(200, 8, f"Total Memory: {memory_info.get('total_memory', 'N/A')} bytes", ln=True)
    pdf.cell(200, 8, f"Used Memory: {memory_info.get('used_memory', 'N/A')} bytes", ln=True)
    pdf.cell(200, 8, f"Available Memory: {memory_info.get('available_memory', 'N/A')} bytes", ln=True)
    pdf.ln(3)
    
    # Integrity Result Section
    pdf.set_font("Arial", 'B', size=14)
    pdf.cell(200, 10, "Integrity Result", ln=True)
    pdf.set_font("Arial", size=12)
    pdf.cell(200, 8, str(integrity_result), ln=True)
    pdf.ln(3)

    pdf.output(output_file)
    print(f"Report generated: {output_file}")
