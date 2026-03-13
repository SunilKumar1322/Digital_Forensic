# Digital Forensics Tool

A modular, python-based digital forensics project that demonstrates evidence acquisition, integrity checking (hashing), metadata extraction, system memory process capture, and evidence report generation.

## Features
- **Database Setup**: SQLite database to log and keep track of acquired evidence.
- **Evidence Acquisition**: Securely copying files, calculating MD5 and SHA-256 hashes, and storing metadata.
- **System Memory Capture**: Fetching running system processes, PIDs, and users.
- **Reporting**: Generating tabular console / file reports from the evidence database.

## Prerequisites
Optional but recommended:
```bash
pip install -r requirements.txt
```

## Usage

### 1. Initialize the Database
Before acquiring any evidence, initialize the SQLite database:
```bash
python main.py --setup
```

### 2. Acquire Evidence
To copy a file into the evidence directory and log its metadata/hashes:
```bash
python main.py --acquire data/suspect_file.txt
```

### 3. Capture Running Processes
Capture the current system processes to a log file:
```bash
python main.py --capture-mem
```

### 4. Generate Evidence Report
Generate a summary report of all evidence acquired so far:
```bash
python main.py --report
```

You can optionally specify a destination folder for acquired files using the `--dest` argument.
