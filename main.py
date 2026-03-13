import os
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
    create_database()

    print(f"\nScanning Evidence Folder: {evidence_folder}")
    files = scan_evidence_folder("data")
    
    if not files:
        print(f"No files found in {evidence_folder}.")
        return

    for file in files:
        print(f"\n[{file}] Acquiring Evidence...")
        evidence = acquire_evidence(file)
        
        if evidence:
            log_action(evidence["file_name"], "Evidence Acquired", "Swastik Garg")
            store_hash(evidence)

            metadata = extract_metadata(evidence_file)
            memory_info = capture_memory_info()
            integrity_result = verify_integrity(evidence)

            # Output explicit report to the reports folder
            if not os.path.exists('reports'):
                os.makedirs('reports')
            
            report_name = f"forensic_report_{evidence['file_name']}.pdf"
            report_path = os.path.join("reports", report_name)
            generate_report(evidence, output_file=report_path)

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
            print(f"Could not acquire evidence for {evidence_file}.")
            
    print("\nCompleted scanning and acquisition.")

if __name__ == "__main__":
    main()
