import os
from database.db_setup import create_database, log_action, log_evidence
from evidence.acquisition import acquire_evidence
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
    evidence_file = "data/suspect_file.txt"
    
    # Ensure our dummy file exists for the test script
    if not os.path.exists('data'):
        os.makedirs('data')
    if not os.path.exists(evidence_file):
        with open(evidence_file, 'w') as f:
            f.write("This is a dummy suspect file used for testing the digital forensics pipeline.\nIt contains simulated sensitive data.\nCONFIDENTIAL: Do not distribute.\n")

    print("Initializing Database...")
    create_database()

    print(f"\nAcquiring Evidence: {evidence_file}")
    evidence = acquire_evidence(evidence_file)
    
    if evidence:
        log_action(evidence["file_name"], "Evidence Acquired", "Swastik Garg")
        log_evidence(evidence["file_name"], evidence["sha256_hash"], evidence["blake3_hash"])

        metadata = extract_metadata(evidence_file)
        memory_info = capture_memory_info()
        integrity_result = verify_integrity(evidence)

        # Output explicit report to the reports folder
        if not os.path.exists('reports'):
            os.makedirs('reports')
        
        report_path = os.path.join("reports", "forensic_report.pdf")
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
        print("\n")
    else:
        print("Could not acquire evidence. Ensure the file exists.")

if __name__ == "__main__":
    main()
