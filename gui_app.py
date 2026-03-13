import tkinter as tk
from tkinter import filedialog, messagebox
import tkinter.scrolledtext as scrolledtext
import os
import threading
import logging

from database.db_setup import create_database, log_action, store_hash
from evidence.acquisition import acquire_evidence, scan_evidence_folder
from evidence.metadata import extract_metadata
from evidence.integrity import verify_integrity
from system.memory_capture import capture_memory_info
from reports.report_generator import generate_report

class ForensicsApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Digital Forensics Dashboard")
        self.root.geometry("700x550")
        
        # State
        self.selected_folder = ""
        self.analysis_data = []
        
        # Create Database
        create_database()

        self.setup_ui()

    def setup_ui(self):
        # --- Top Frame: Folder Selection ---
        frame_top = tk.Frame(self.root, pady=10)
        frame_top.pack(fill=tk.X, padx=20)
        
        self.lbl_folder = tk.Label(frame_top, text="No Evidence Selected", fg="gray", font=("Arial", 10, "italic"))
        self.lbl_folder.pack(side=tk.LEFT, fill=tk.X, expand=True)

        btn_select = tk.Button(frame_top, text="Select Evidence Folder", bg="#0052cc", fg="white", font=("Arial", 10, "bold"), command=self.select_evidence)
        btn_select.pack(side=tk.RIGHT, padx=10)

        # --- Middle Frame: Case Details ---
        frame_mid = tk.LabelFrame(self.root, text="Case Information", pady=10, padx=10)
        frame_mid.pack(fill=tk.X, padx=20, pady=10)

        tk.Label(frame_mid, text="Case ID:").grid(row=0, column=0, sticky=tk.W, pady=5)
        self.ent_case_id = tk.Entry(frame_mid, width=20)
        self.ent_case_id.insert(0, "CASE-2026-001")
        self.ent_case_id.grid(row=0, column=1, sticky=tk.W)

        tk.Label(frame_mid, text="Location:").grid(row=0, column=2, sticky=tk.W, padx=(20, 0), pady=5)
        self.ent_location = tk.Entry(frame_mid, width=20)
        self.ent_location.insert(0, "Server Room A")
        self.ent_location.grid(row=0, column=3, sticky=tk.W)

        tk.Label(frame_mid, text="Officer ID:").grid(row=1, column=0, sticky=tk.W, pady=5)
        self.ent_officer = tk.Entry(frame_mid, width=20)
        self.ent_officer.insert(0, "OFF-8942")
        self.ent_officer.grid(row=1, column=1, sticky=tk.W)

        # --- Action Buttons ---
        frame_actions = tk.Frame(self.root, pady=10)
        frame_actions.pack(fill=tk.X, padx=20)

        self.btn_analyze = tk.Button(frame_actions, text="Analyze", bg="#e68a00", fg="white", font=("Arial", 11, "bold"), width=15, command=self.run_analysis)
        self.btn_analyze.pack(side=tk.LEFT, padx=10)

        self.btn_report = tk.Button(frame_actions, text="Generate Reports", bg="#2eb82e", fg="white", font=("Arial", 11, "bold"), width=15, state=tk.DISABLED, command=self.generate_reports)
        self.btn_report.pack(side=tk.LEFT, padx=10)

        # --- Log Console ---
        frame_log = tk.LabelFrame(self.root, text="System Logs & Output")
        frame_log.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)

        self.log_box = scrolledtext.ScrolledText(frame_log, state=tk.DISABLED, bg="black", fg="#00ff00", font=("Consolas", 9))
        self.log_box.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

    def log(self, message):
        self.log_box.config(state=tk.NORMAL)
        self.log_box.insert(tk.END, message + "\n")
        self.log_box.see(tk.END)
        self.log_box.config(state=tk.DISABLED)
        # Also log to actual python logger
        logging.info(message)
        self.root.update_idletasks()

    def select_evidence(self):
        folder = filedialog.askdirectory(title="Select Evidence Folder")
        if folder:
            self.selected_folder = folder
            self.lbl_folder.config(text=f"Selected: {self.selected_folder}", fg="black", font=("Arial", 10))
            self.log(f"[*] Evidence folder selected: {self.selected_folder}")
            self.btn_report.config(state=tk.DISABLED) # reset report button
            self.analysis_data.clear()

    def run_analysis(self):
        if not self.selected_folder:
            messagebox.showwarning("Warning", "Please select an evidence folder first.")
            return

        self.btn_analyze.config(state=tk.DISABLED)
        self.log("[*] Starting Analysis...")
        
        # Run in thread to prevent UI freezing
        threading.Thread(target=self._analysis_thread, daemon=True).start()

    def _analysis_thread(self):
        case_id = self.ent_case_id.get()
        location = self.ent_location.get()
        officer = self.ent_officer.get()

        files = scan_evidence_folder(self.selected_folder)
        if not files:
            self.log(f"[!] No valid files found in {self.selected_folder}")
            self.btn_analyze.config(state=tk.NORMAL)
            return

        self.analysis_data = []

        for file in files:
            self.log(f"\n[+] Analyzing: {os.path.basename(file)}")
            evidence = acquire_evidence(file, case_id=case_id, location=location, officer_id=officer)
            
            if evidence:
                try:
                    log_action(evidence["file_name"], "Evidence Acquired via GUI", evidence["officer_id"])
                    store_hash(evidence)
                    self.log(f"    - Hashes calculated and stored in Database")
                    
                    metadata = extract_metadata(file)
                    memory_info = capture_memory_info()
                    integrity = verify_integrity(evidence)

                    self.log(f"    - Integrity: {integrity}")

                    # Store full context for reporting phase
                    self.analysis_data.append({
                        "evidence": evidence,
                        "metadata": metadata,
                        "memory": memory_info,
                        "integrity": integrity
                    })
                except Exception as e:
                    self.log(f"[!] Error processing {file}: {str(e)}")
            else:
                self.log(f"[!] Failed to acquire: {file}")

        self.log("\n[*] Analysis Complete! You can now generate reports.")
        
        # Re-enable buttons
        self.root.after(0, lambda: self.btn_analyze.config(state=tk.NORMAL))
        self.root.after(0, lambda: self.btn_report.config(state=tk.NORMAL))


    def generate_reports(self):
        if not self.analysis_data:
            messagebox.showwarning("Warning", "No analysis data available. Please run Analyze first.")
            return

        if not os.path.exists('reports'):
            os.makedirs('reports')

        self.log("\n[*] Generating PDF Reports...")
        
        for item in self.analysis_data:
            ev = item["evidence"]
            report_name = f"forensic_report_{ev['file_name']}.pdf"
            report_path = os.path.join("reports", report_name)
            
            try:
                generate_report(ev, item["metadata"], item["memory"], item["integrity"], output_file=report_path)
                self.log(f"    - Created: {report_path}")
            except Exception as e:
                self.log(f"[!] Error generating report for {ev['file_name']}: {str(e)}")
                
        self.log("[*] Report Generation Complete!")
        messagebox.showinfo("Success", "All forensic reports have been generated locally in the 'reports' folder.")

if __name__ == "__main__":
    # Ensure logs folder exists
    if not os.path.exists('logs'):
        os.makedirs('logs')

    logging.basicConfig(
        filename="logs/forensic.log",
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s'
    )

    root = tk.Tk()
    app = ForensicsApp(root)
    root.mainloop()
