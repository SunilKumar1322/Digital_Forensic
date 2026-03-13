import os
import logging
from database.db_setup import create_database, log_action, store_hash
from evidence.acquisition import acquire_evidence, scan_evidence_folder
from evidence.metadata import extract_metadata
from evidence.integrity import verify_integrity
from system.memory_capture import capture_memory_info
from reports.report_generator import generate_report

# =========================================
# DIGITAL EVIDENCE INTEGRITY SYSTEM
# =========================================
# MAIN PROGRAM
# =========================================

# Ensure log directory exists before setting up basicConfig
if not os.path.exists('logs'):
    os.makedirs('logs')

logging.basicConfig(
    filename="logs/forensic.log",
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

def main():
    evidence_folder = "data"
    
    # Ensure our dummy file exists for the test script inside the folder
    if not os.path.exists(evidence_folder):
        os.makedirs(evidence_folder)
    
    dummy_file = os.path.join(evidence_folder, "suspect_file.txt")
    if not os.path.exists(dummy_file):
        with open(dummy_file, 'w') as f:
            f.write("This is a dummy suspect file used for testing the digital forensics pipeline.\nIt contains simulated sensitive data.\nCONFIDENTIAL: Do not distribute.\n")

    print("Initializing Database...")
    logging.info("Initializing SQLite forensics database...")
    create_database()

    print(f"\nScanning Evidence Folder: {evidence_folder}")
    logging.info(f"Scanning Evidence Folder: {evidence_folder}")
    files = scan_evidence_folder("data")
    
    if not files:
        print(f"No files found in {evidence_folder}.")
        logging.warning(f"No files found in {evidence_folder}.")
        return

    for file in files:
        print(f"\n[{file}] Acquiring Evidence...")
        logging.info(f"Acquiring Evidence for file: {file}")
        evidence = acquire_evidence(file, case_id="CASE-2026-001", location="Server Room A", officer_id="OFF-8942")
        
        if evidence:
            log_action(evidence["file_name"], "Evidence Acquired", evidence["officer_id"])
            store_hash(evidence)
            logging.info(f"Successfully logged hashes and custody for {evidence['file_name']}")

            metadata = extract_metadata(file)
            memory_info = capture_memory_info()
            integrity_result = verify_integrity(evidence)

            # Output explicit report to the reports folder
            if not os.path.exists('reports'):
                os.makedirs('reports')
            
            report_name = f"forensic_report_{evidence['file_name']}.pdf"
            report_path = os.path.join("reports", report_name)
            generate_report(evidence, metadata, memory_info, integrity_result, output_file=report_path)
            logging.info(f"Generated PDF Report: {report_path}")

            print("\n" + "="*40)
            print("EVIDENCE INFORMATION")
            print("="*40)
            for k, v in evidence.items():
                print(f"{k}: {v}")

            print("\n" + "="*40)
            print("FILE METADATA")
            print("="*40)
            for k, v in metadata.items():
                print(f"{k}: {v}")

            print("\n" + "="*40)
            print("SYSTEM MEMORY INFO")
            print("="*40)
            for k, v in memory_info.items():
                print(f"{k}: {v} bytes")

            print("\n" + "="*40)
            print("INTEGRITY CHECK RESULT")
            print("="*40)
            print(integrity_result)
        else:
            print(f"Could not acquire evidence for {file}.")
            logging.error(f"Could not acquire evidence for {file}.")
            
    print("\nCompleted scanning and acquisition.")
    logging.info("Completed scanning and acquisition process.")

if __name__ == "__main__":
    main()
