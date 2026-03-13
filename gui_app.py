import customtkinter as ctk
from tkinter import filedialog, messagebox
import os
import sqlite3
import threading

from database.db_setup import create_database, log_action, store_hash
from evidence.acquisition import acquire_evidence, scan_evidence_folder
from evidence.metadata import extract_metadata
from evidence.integrity import verify_integrity
from system.memory_capture import capture_memory_info
from reports.report_generator import generate_report

# Configure CustomTkinter Appearance
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

class AdvancedForensicsApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Digital Evidence Integrity Tool")
        self.geometry("900x650")
        self.resizable(False, False)

        # Database initialization
        create_database()
        
        # State tracking for generating reports
        self.analysis_data = []

        self.setup_ui()

    def setup_ui(self):
        # --- Top Header ---
        self.header_frame = ctk.CTkFrame(self, corner_radius=0, fg_color="transparent")
        self.header_frame.pack(fill="x", pady=(15, 5))

        self.title_label = ctk.CTkLabel(self.header_frame, text="Digital Evidence Integrity Tool", font=("Segoe UI", 24, "bold"))
        self.title_label.pack()

        self.divider = ctk.CTkFrame(self, height=2, fg_color="gray50")
        self.divider.pack(fill="x", padx=20, pady=5)

        # --- Main Layout Grid ---
        self.main_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.main_frame.pack(fill="both", expand=True, padx=20, pady=10)

        # Sidebar (Buttons)
        self.sidebar_frame = ctk.CTkFrame(self.main_frame, width=250, corner_radius=10)
        self.sidebar_frame.pack(side="left", fill="y", padx=(0, 15))

        # Dashboard / Result Box (Right Side)
        self.dashboard_frame = ctk.CTkFrame(self.main_frame, corner_radius=10)
        self.dashboard_frame.pack(side="right", fill="both", expand=True)

        self.lbl_dashboard = ctk.CTkLabel(self.dashboard_frame, text="Results Dashboard", font=("Segoe UI", 16, "bold"))
        self.lbl_dashboard.pack(pady=10)

        self.result_box = ctk.CTkTextbox(self.dashboard_frame, font=("Consolas", 12), wrap="word", state="normal")
        self.result_box.pack(fill="both", expand=True, padx=10, pady=(0, 10))
        self.result_box.configure(state="disabled")

        # --- Sidebar Buttons ---
        btn_font = ("Segoe UI", 13, "bold")

        self.btn_single = ctk.CTkButton(self.sidebar_frame, text="[ Select Evidence File ]", font=btn_font, command=self.analyze_single)
        self.btn_single.pack(pady=15, padx=20, fill="x")

        self.btn_folder = ctk.CTkButton(self.sidebar_frame, text="[ Analyze Folder ]", font=btn_font, command=self.analyze_folder)
        self.btn_folder.pack(pady=15, padx=20, fill="x")

        self.btn_compare = ctk.CTkButton(self.sidebar_frame, text="[ Compare Files ]", font=btn_font, fg_color="#E67E22", hover_color="#D35400", command=self.compare_files)
        self.btn_compare.pack(pady=15, padx=20, fill="x")

        self.btn_chain = ctk.CTkButton(self.sidebar_frame, text="[ View Chain of Custody ]", font=btn_font, fg_color="#8E44AD", hover_color="#732D91", command=self.view_chain_of_custody)
        self.btn_chain.pack(pady=15, padx=20, fill="x")

        self.btn_sys = ctk.CTkButton(self.sidebar_frame, text="[ System Memory Info ]", font=btn_font, fg_color="#2980B9", hover_color="#1F618D", command=self.show_memory)
        self.btn_sys.pack(pady=15, padx=20, fill="x")

        self.btn_report = ctk.CTkButton(self.sidebar_frame, text="[ Generate Report ]", font=btn_font, fg_color="#27AE60", hover_color="#1E8449", command=self.generate_advanced_report)
        self.btn_report.pack(pady=15, padx=20, fill="x")

        # Instructions Initial Text
        self.show_result("System Initialized.\nSelect an option from the menu to begin forensic analysis.\n" + "-"*50)

    def show_result(self, text):
        self.result_box.configure(state="normal")
        self.result_box.insert("end", text + "\n")
        self.result_box.see("end")
        self.result_box.configure(state="disabled")
        self.update()

    # --- 1. Single Analyze ---
    def analyze_single(self):
        file_path = filedialog.askopenfilename(title="Select Evidence File")
        if not file_path: return
        self.show_result(f"\n[*] Scanning Single File: {os.path.basename(file_path)}")
        self._process_file(file_path)
        self.show_result("[*] Single File Analysis Completed.\n" + "-"*50)

    # --- 2. Multiple Folder Analyzer ---
    def analyze_folder(self):
        folder = filedialog.askdirectory(title="Select Evidence Folder")
        if not folder: return
        self.show_result(f"\n[*] Scanning Folder: {folder}")
        
        files = scan_evidence_folder(folder)
        if not files:
            self.show_result("[!] No valid files found in folder.")
            return

        for path in files:
            self._process_file(path)

        self.show_result(f"[*] Folder Analysis Completed. ({len(files)} files scanned)\n" + "-"*50)

    # Core Logic Abstraction
    def _process_file(self, file_path):
        evidence = acquire_evidence(file_path)
        if not evidence:
            self.show_result(f"[!] Errored acquiring: {file_path}")
            return

        log_action(evidence["file_name"], "GUI Evidence Acquisition", "System_GUI")
        store_hash(evidence)

        metadata = extract_metadata(file_path)
        memory_info = capture_memory_info()
        integrity = verify_integrity(evidence)

        # Store for reports
        self.analysis_data.append({
            "evidence": evidence,
            "metadata": metadata,
            "memory": memory_info,
            "integrity": integrity
        })

        self.show_result(f"File Name: {evidence['file_name']}")
        self.show_result(f"SHA256: {evidence['sha256_hash']}")
        self.show_result(f"Integrity: {integrity}\n")

    # --- 3. Chain of Custody Viewer ---
    def view_chain_of_custody(self):
        self.show_result("\n[*] Retrieving Chain of Custody Database Logs...")
        try:
            conn = sqlite3.connect("forensics.db")
            cursor = conn.cursor()
            cursor.execute("SELECT id, evidence_name, action, timestamp FROM chain_of_custody")
            rows = cursor.fetchall()
            
            if not rows:
                self.show_result("No records found in database.")
            else:
                self.show_result(f"{'ID':<5}| {'Evidence':<25}| {'Action':<30}| {'Timestamp'}")
                self.show_result("-" * 80)
                for row in rows[-20:]:  # Limit to last 20 for readability
                    self.show_result(f"{row[0]:<5}| {row[1]:<25}| {row[2]:<30}| {row[3]}")
                self.show_result("\n[*] Chain of custody retrieval complete (showing max 20 latest).\n" + "-"*50)
            conn.close()
        except Exception as e:
            self.show_result(f"[!] Database Error: {str(e)}")

    # --- 4. Evidence Hash Comparison Tool ---
    def compare_files(self):
        self.show_result("\n[*] Hash Comparison System")
        self.show_result("Please select the FIRST file...")
        file1 = filedialog.askopenfilename(title="Select File A")
        if not file1: return

        self.show_result("Please select the SECOND file...")
        file2 = filedialog.askopenfilename(title="Select File B")
        if not file2: return

        ev1 = acquire_evidence(file1)
        ev2 = acquire_evidence(file2)

        self.show_result(f"File A: {os.path.basename(file1)} (SHA256: {ev1['sha256_hash'][:15]}...)")
        self.show_result(f"File B: {os.path.basename(file2)} (SHA256: {ev2['sha256_hash'][:15]}...)")

        if ev1["sha256_hash"] == ev2["sha256_hash"]:
            self.show_result(">>> MATCH: Files are cryptographically identical! <<<\n" + "-"*50)
            messagebox.showinfo("Result", "Files are identical.")
        else:
            self.show_result(">>> NOT MATCH: Files are different! <<<\n" + "-"*50)
            messagebox.showwarning("Result", "Files are different.")

    # --- 5. System Information Panel ---
    def show_memory(self):
        self.show_result("\n[*] Extracting System Memory Statistics...")
        mem = capture_memory_info()
        self.show_result(f"Total Memory: {mem['total_memory']} bytes")
        self.show_result(f"Used Memory: {mem['used_memory']} bytes")
        self.show_result(f"Available Memory: {mem['available_memory']} bytes")
        self.show_result("[*] System check complete.\n" + "-"*50)

    # --- 6. Generate Advanced Report ---
    def generate_advanced_report(self):
        if not self.analysis_data:
            messagebox.showerror("Error", "No evidence analyzed yet! Run 'Analyze Folder' or 'Select Evidence File' first.")
            return

        self.show_result("\n[*] Generating Advanced PDF Forensic Reports...")
        if not os.path.exists('reports'):
            os.makedirs('reports')

        count = 0
        for item in self.analysis_data:
            ev = item["evidence"]
            report_path = os.path.join("reports", f"forensic_report_{ev['file_name']}.pdf")
            generate_report(ev, item["metadata"], item["memory"], item["integrity"], output_file=report_path)
            self.show_result(f"-> Generated: {report_path}")
            count += 1
            
        self.show_result(f"[*] Complete. {count} reports generated.\n" + "-"*50)
        messagebox.showinfo("Success", f"{count} PDF Reports compiled inside the 'reports' folder.")

if __name__ == "__main__":
    app = AdvancedForensicsApp()
    app.mainloop()
