import datetime
import os

# =========================================
# METADATA EXTRACTION
# =========================================

def extract_metadata(file_path):
    if not os.path.exists(file_path):
        return None
        
    stats = os.stat(file_path)

    metadata = {
        "created_time": datetime.datetime.fromtimestamp(stats.st_ctime),
        "modified_time": datetime.datetime.fromtimestamp(stats.st_mtime),
        "access_time": datetime.datetime.fromtimestamp(stats.st_atime)
    }

    return metadata
