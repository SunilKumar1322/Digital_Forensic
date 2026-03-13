import tkinter as tk
from tkinter import filedialog, messagebox

from database.db_setup import create_database
from evidence.acquisition import acquire_evidence
from evidence.metadata import extract_metadata
from evidence.integrity import verify_integrity
from system.memory_capture import capture_memory_info
from reports.report_generator import generate_report


def analyze_file():

    file_path = filedialog.askopenfilename()

    if not file_path:
        return

    create_database()

    evidence = acquire_evidence(file_path)

    if not evidence:
        messagebox.showerror("Error", "Could not acquire evidence from the selected file.")
        return

    metadata = extract_metadata(file_path)

    memory_info = capture_memory_info()

    integrity = verify_integrity(evidence)

    generate_report(evidence, metadata, memory_info, integrity)

    result = f"""
File: {evidence['file_name']}

SHA256:
{evidence['sha256_hash']}

BLAKE3:
{evidence['blake3_hash']}

Integrity:
{integrity}
"""

    messagebox.showinfo("Analysis Result", result)


root = tk.Tk()
root.title("Digital Evidence Integrity Tool")
root.geometry("500x300")


title = tk.Label(root, text="Digital Forensic Evidence Tool", font=("Arial", 16))
title.pack(pady=20)


btn = tk.Button(root, text="Select Evidence File", command=analyze_file, height=2, width=25)
btn.pack(pady=20)


exit_btn = tk.Button(root, text="Exit", command=root.quit)
exit_btn.pack()


root.mainloop()
