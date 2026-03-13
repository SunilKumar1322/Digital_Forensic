import tkinter as tk
from tkinter import filedialog, messagebox
import tkinter.ttk as ttk

from database.db_setup import create_database
from evidence.acquisition import acquire_evidence
from evidence.metadata import extract_metadata
from evidence.integrity import verify_integrity
from system.memory_capture import capture_memory_info
from reports.report_generator import generate_report


def analyze_file():
    file_path = filedialog.askopenfilename(title="Select File to Analyze")

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

    result = f"""=====================================
 DIGITAL EVIDENCE ACQUIRED
=====================================
📄 File Name: {evidence['file_name']}

🔒 SHA256 Hash:
{evidence['sha256_hash']}

⚡ BLAKE3 Hash:
{evidence['blake3_hash']}

🛡️ Integrity Check:
{integrity}
====================================="""

    messagebox.showinfo("Analysis Result", result)


# --- UI SETUP ---
root = tk.Tk()
root.title("Digital Evidence Integrity Tool")
root.geometry("600x400")
root.configure(bg="#f4f5f7")
root.resizable(False, False)

# Custom Style Configs
style = ttk.Style()
style.theme_use('clam')

# Define custom button styles
style.configure("Primary.TButton",
                font=("Segoe UI", 12, "bold"),
                foreground="white",
                background="#0052cc",
                padding=10)
style.map("Primary.TButton",
          background=[("active", "#004099")])

style.configure("Secondary.TButton",
                font=("Segoe UI", 11),
                foreground="#333",
                background="#e2e8f0",
                padding=8)
style.map("Secondary.TButton",
          background=[("active", "#cbd5e1")])

# Main Header Frame
header_frame = tk.Frame(root, bg="#1e293b", pady=25)
header_frame.pack(fill=tk.X)

title_lbl = tk.Label(header_frame, 
                     text="Digital Forensic Evidence Tool", 
                     font=("Segoe UI Semibold", 18), 
                     fg="white", 
                     bg="#1e293b")
title_lbl.pack()

subtitle_lbl = tk.Label(header_frame, 
                        text="Secure File Analysis & Reporting Pipeline", 
                        font=("Segoe UI", 10, "italic"), 
                        fg="#94a3b8", 
                        bg="#1e293b")
subtitle_lbl.pack(pady=(5, 0))

# Content Frame
content_frame = tk.Frame(root, bg="#f4f5f7", pady=40)
content_frame.pack(fill=tk.BOTH, expand=True)

instruction_lbl = tk.Label(content_frame, 
                           text="Please select a suspect file to generate cryptography hashes\nand PDF forensic reports.", 
                           font=("Segoe UI", 11), 
                           fg="#475569", 
                           bg="#f4f5f7",
                           justify="center")
instruction_lbl.pack(pady=(0, 30))

btn_select = ttk.Button(content_frame, 
                        text="🔍 Select Evidence File", 
                        style="Primary.TButton", 
                        command=analyze_file,
                        cursor="hand2")
btn_select.pack(ipadx=20)

# Footer Frame
footer_frame = tk.Frame(root, bg="#f4f5f7", pady=20)
footer_frame.pack(fill=tk.X, side=tk.BOTTOM)

exit_btn = ttk.Button(footer_frame, 
                      text="Exit App", 
                      style="Secondary.TButton", 
                      command=root.quit,
                      cursor="hand2")
exit_btn.pack(side=tk.RIGHT, padx=20)

version_lbl = tk.Label(footer_frame, 
                       text="v1.0.0 | System Ready", 
                       font=("Segoe UI", 9), 
                       fg="#94a3b8", 
                       bg="#f4f5f7")
version_lbl.pack(side=tk.LEFT, padx=20)

root.mainloop()
