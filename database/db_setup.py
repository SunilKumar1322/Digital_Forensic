import sqlite3

# =========================================
# DATABASE CREATION AND LOGGING
# =========================================

DB_NAME = "forensics.db"

def create_database():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS chain_of_custody(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        evidence_name TEXT,
        action TEXT,
        investigator TEXT,
        timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
    )
    """)
    
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS evidence_hash(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        file_name TEXT,
        sha256_hash TEXT,
        blake3_hash TEXT,
        case_id TEXT,
        location TEXT,
        officer_id TEXT,
        timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
    )
    """)

    conn.commit()
    conn.close()

def log_action(evidence_name, action, investigator):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("""
    INSERT INTO chain_of_custody(evidence_name, action, investigator)
    VALUES (?, ?, ?)
    """, (evidence_name, action, investigator))

    conn.commit()
    conn.close()

def store_hash(evidence):

    conn = sqlite3.connect("forensics.db")
    cursor = conn.cursor()

    cursor.execute("""
    INSERT INTO evidence_hash(file_name, sha256_hash, blake3_hash, case_id, location, officer_id)
    VALUES (?, ?, ?, ?, ?, ?)
    """, (evidence["file_name"], evidence["sha256_hash"], evidence["blake3_hash"], evidence.get("case_id"), evidence.get("location"), evidence.get("officer_id")))

    conn.commit()
    conn.close()

if __name__ == '__main__':
    create_database()
