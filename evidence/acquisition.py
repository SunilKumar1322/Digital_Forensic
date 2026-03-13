import hashlib
import blake3
import os

# =========================================
# EVIDENCE ACQUISITION
# =========================================

def scan_evidence_folder(folder):

    files = []

    for file in os.listdir(folder):
        path = os.path.join(folder, file)

        if os.path.isfile(path):
            files.append(path)

    return files

def acquire_evidence(file_path):
    if not os.path.exists(file_path):
        print(f"Error: {file_path} does not exist.")
        return None

    with open(file_path, "rb") as f:
        file_data = f.read()

    sha256_hash = hashlib.sha256(file_data).hexdigest()
    blake3_hash = blake3.blake3(file_data).hexdigest()

    evidence = {
        "file_name": os.path.basename(file_path),
        "file_path": os.path.abspath(file_path),
        "sha256_hash": sha256_hash,
        "blake3_hash": blake3_hash
    }

    return evidence
