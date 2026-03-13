import hashlib
import blake3
import os

# =========================================
# INTEGRITY VERIFICATION
# =========================================

def verify_integrity(evidence):
    file_path = evidence["file_path"]

    if not os.path.exists(file_path):
        return "WARNING: File no longer exists"

    with open(file_path, "rb") as f:
        file_data = f.read()

    new_sha = hashlib.sha256(file_data).hexdigest()
    new_blake = blake3.blake3(file_data).hexdigest()

    if new_sha == evidence["sha256_hash"] and new_blake == evidence["blake3_hash"]:
        return "Evidence Integrity Verified"
    else:
        return "WARNING: Evidence Tampered"
