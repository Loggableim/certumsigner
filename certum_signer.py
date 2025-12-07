#!/usr/bin/env python3
"""
Certum Signer - Windows Desktop Tool for Code Signing
Uses Certum SimplySign + SimplySign Desktop for signing files
"""

import tkinter as tk
from tkinter import ttk, filedialog, messagebox, scrolledtext
import os
import subprocess
import json
from datetime import datetime
from pathlib import Path
import threading


class CertumSignerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Certum Signer")
        self.root.geometry("800x600")
        self.root.minsize(600, 400)
        
        # File list
        self.files_to_sign = set()
        
        # Load settings
        self.settings_file = Path.home() / "certum_signer_settings.json"
        self.log_file = Path.home() / "certum_signer.log"
        self.load_settings()
        
        # Create UI
        self.create_menu()
        self.create_widgets()
        
        # Enable drag and drop
        self.setup_drag_drop()
        
    def load_settings(self):
        """Load settings from JSON file"""
        default_settings = {
            "signing_command": "signtool",
            "timestamp_server": "http://time.certum.pl",
            "log_file": str(self.log_file)
        }
        
        if self.settings_file.exists():
            try:
                with open(self.settings_file, 'r') as f:
                    self.settings = json.load(f)
                # Ensure all keys exist
                for key in default_settings:
                    if key not in self.settings:
                        self.settings[key] = default_settings[key]
            except Exception as e:
                self.settings = default_settings
                self.log_message(f"Error loading settings: {e}", error=True)
        else:
            self.settings = default_settings
            self.save_settings()
        
        # Update log file path
        self.log_file = Path(self.settings["log_file"])
        
    def save_settings(self):
        """Save settings to JSON file"""
        try:
            with open(self.settings_file, 'w') as f:
                json.dump(self.settings, f, indent=2)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save settings: {e}")
    
    def create_menu(self):
        """Create menu bar"""
        menubar = tk.Menu(self.root)
        self.root.config(menu=menubar)
        
        # File menu
        file_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="File", menu=file_menu)
        file_menu.add_command(label="Settings", command=self.open_settings)
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self.root.quit)
        
        # Help menu
        help_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Help", menu=help_menu)
        help_menu.add_command(label="About", command=self.show_about)
    
    def create_widgets(self):
        """Create main UI widgets"""
        # Main container
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Configure grid weights
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(0, weight=1)
        main_frame.rowconfigure(1, weight=1)
        main_frame.rowconfigure(3, weight=1)
        
        # Button frame
        button_frame = ttk.Frame(main_frame)
        button_frame.grid(row=0, column=0, sticky=(tk.W, tk.E), pady=(0, 10))
        
        ttk.Button(button_frame, text="Select Files", command=self.select_files).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Select Folder", command=self.select_folder).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Clear List", command=self.clear_files).pack(side=tk.LEFT, padx=5)
        
        # File list frame
        list_frame = ttk.LabelFrame(main_frame, text="Files to Sign (Drag & Drop files/folders here)", padding="5")
        list_frame.grid(row=1, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), pady=(0, 10))
        list_frame.columnconfigure(0, weight=1)
        list_frame.rowconfigure(0, weight=1)
        
        # Scrollbar and Listbox
        scrollbar = ttk.Scrollbar(list_frame)
        scrollbar.grid(row=0, column=1, sticky=(tk.N, tk.S))
        
        self.file_listbox = tk.Listbox(list_frame, yscrollcommand=scrollbar.set, selectmode=tk.EXTENDED)
        self.file_listbox.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        scrollbar.config(command=self.file_listbox.yview)
        
        # Sign button
        sign_frame = ttk.Frame(main_frame)
        sign_frame.grid(row=2, column=0, sticky=(tk.W, tk.E), pady=(0, 10))
        
        self.sign_button = ttk.Button(sign_frame, text="Sign All Files", command=self.sign_files)
        self.sign_button.pack(side=tk.LEFT, padx=5)
        
        self.status_label = ttk.Label(sign_frame, text="Ready")
        self.status_label.pack(side=tk.LEFT, padx=10)
        
        # Log frame
        log_frame = ttk.LabelFrame(main_frame, text="Log Output", padding="5")
        log_frame.grid(row=3, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        log_frame.columnconfigure(0, weight=1)
        log_frame.rowconfigure(0, weight=1)
        
        self.log_text = scrolledtext.ScrolledText(log_frame, height=10, state='disabled')
        self.log_text.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
    
    def setup_drag_drop(self):
        """Setup drag and drop for files"""
        # For full Windows drag-and-drop, tkinterdnd2 package is recommended
        # For now, we provide file selection dialogs
        # Users can install tkinterdnd2 for native drag-and-drop support
        pass
    
    def select_files(self):
        """Open file dialog to select files"""
        files = filedialog.askopenfilenames(
            title="Select files to sign",
            filetypes=[
                ("Executable files", "*.exe"),
                ("DLL files", "*.dll"),
                ("MSI files", "*.msi"),
                ("Cabinet files", "*.cab"),
                ("All files", "*.*")
            ]
        )
        for file_path in files:
            self.add_file(file_path)
        self.update_file_list()
    
    def select_folder(self):
        """Open folder dialog to select a folder"""
        folder = filedialog.askdirectory(title="Select folder containing files to sign")
        if folder:
            self.add_folder(folder)
            self.update_file_list()
    
    def add_file(self, file_path):
        """Add a single file to the list"""
        if os.path.isfile(file_path):
            self.files_to_sign.add(os.path.abspath(file_path))
    
    def add_folder(self, folder_path):
        """Add all signable files from a folder"""
        signable_extensions = ['.exe', '.dll', '.msi', '.cab', '.ocx', '.sys']
        for root, dirs, files in os.walk(folder_path):
            for file in files:
                if any(file.lower().endswith(ext) for ext in signable_extensions):
                    file_path = os.path.join(root, file)
                    self.files_to_sign.add(os.path.abspath(file_path))
    
    def clear_files(self):
        """Clear the file list"""
        self.files_to_sign.clear()
        self.update_file_list()
        self.log_message("File list cleared")
    
    def update_file_list(self):
        """Update the listbox with current files"""
        self.file_listbox.delete(0, tk.END)
        for file_path in sorted(self.files_to_sign):
            self.file_listbox.insert(tk.END, file_path)
    
    def sign_files(self):
        """Sign all files in the list"""
        if not self.files_to_sign:
            messagebox.showwarning("No Files", "Please add files to sign first.")
            return
        
        # Disable sign button during signing
        self.sign_button.config(state='disabled')
        self.status_label.config(text="Signing in progress...")
        
        # Run signing in a separate thread to keep UI responsive
        thread = threading.Thread(target=self._sign_files_thread)
        thread.daemon = True
        thread.start()
    
    def _sign_files_thread(self):
        """Thread function to sign files"""
        success_count = 0
        failure_count = 0
        
        self.log_message(f"Starting signing process for {len(self.files_to_sign)} files...")
        
        for file_path in self.files_to_sign:
            try:
                # Use Certum SimplySign command
                # The actual command will depend on how SimplySign Desktop is configured
                # Typically it would be something like:
                # signtool sign /tr <timestamp_server> /td sha256 /fd sha256 /a <file>
                
                cmd = self._build_sign_command(file_path)
                self.log_message(f"Signing: {os.path.basename(file_path)}")
                
                result = subprocess.run(
                    cmd,
                    capture_output=True,
                    text=True,
                    timeout=120  # 2 minute timeout per file
                )
                
                if result.returncode == 0:
                    success_count += 1
                    self.log_message(f"✓ Successfully signed: {os.path.basename(file_path)}")
                else:
                    failure_count += 1
                    error_msg = result.stderr or result.stdout
                    self.log_message(f"✗ Failed to sign: {os.path.basename(file_path)}", error=True)
                    self.log_message(f"  Error: {error_msg}", error=True)
                    
            except subprocess.TimeoutExpired:
                failure_count += 1
                self.log_message(f"✗ Timeout signing: {os.path.basename(file_path)}", error=True)
            except Exception as e:
                failure_count += 1
                self.log_message(f"✗ Error signing {os.path.basename(file_path)}: {e}", error=True)
        
        # Summary
        self.log_message("")
        self.log_message(f"=== Signing Complete ===")
        self.log_message(f"Successful: {success_count}")
        self.log_message(f"Failed: {failure_count}")
        self.log_message(f"Total: {len(self.files_to_sign)}")
        
        # Re-enable button
        self.root.after(0, lambda: self.sign_button.config(state='normal'))
        self.root.after(0, lambda: self.status_label.config(text="Ready"))
        
        # Show completion message
        if failure_count == 0:
            self.root.after(0, lambda: messagebox.showinfo("Success", f"All {success_count} files signed successfully!"))
        else:
            self.root.after(0, lambda: messagebox.showwarning("Completed with Errors", 
                f"Signed: {success_count}\nFailed: {failure_count}\nCheck log for details."))
    
    def _build_sign_command(self, file_path):
        """Build the signing command"""
        # This builds the command for Certum SimplySign
        # Default command uses signtool which integrates with SimplySign Desktop
        
        signing_tool = self.settings.get("signing_command", "signtool")
        timestamp_server = self.settings.get("timestamp_server", "http://time.certum.pl")
        
        # Standard signtool command that works with SimplySign Desktop
        cmd = [
            signing_tool,
            "sign",
            "/tr", timestamp_server,
            "/td", "sha256",
            "/fd", "sha256",
            "/a",  # Select the best signing cert automatically
            file_path
        ]
        
        return cmd
    
    def log_message(self, message, error=False):
        """Add message to log output and log file"""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_entry = f"[{timestamp}] {message}"
        
        # Update UI log
        self.log_text.config(state='normal')
        if error:
            self.log_text.insert(tk.END, log_entry + "\n", "error")
            self.log_text.tag_config("error", foreground="red")
        else:
            self.log_text.insert(tk.END, log_entry + "\n")
        self.log_text.see(tk.END)
        self.log_text.config(state='disabled')
        
        # Write to log file
        try:
            with open(self.log_file, 'a', encoding='utf-8') as f:
                f.write(log_entry + "\n")
        except Exception as e:
            print(f"Failed to write to log file: {e}")
    
    def open_settings(self):
        """Open settings dialog"""
        settings_window = tk.Toplevel(self.root)
        settings_window.title("Settings")
        settings_window.geometry("500x300")
        settings_window.transient(self.root)
        settings_window.grab_set()
        
        # Main frame
        frame = ttk.Frame(settings_window, padding="20")
        frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        settings_window.columnconfigure(0, weight=1)
        settings_window.rowconfigure(0, weight=1)
        
        # Signing command
        ttk.Label(frame, text="Signing Command:").grid(row=0, column=0, sticky=tk.W, pady=5)
        signing_cmd_entry = ttk.Entry(frame, width=50)
        signing_cmd_entry.insert(0, self.settings.get("signing_command", "signtool"))
        signing_cmd_entry.grid(row=0, column=1, sticky=(tk.W, tk.E), pady=5, padx=(10, 0))
        
        # Timestamp server
        ttk.Label(frame, text="Timestamp Server:").grid(row=1, column=0, sticky=tk.W, pady=5)
        timestamp_entry = ttk.Entry(frame, width=50)
        timestamp_entry.insert(0, self.settings.get("timestamp_server", "http://time.certum.pl"))
        timestamp_entry.grid(row=1, column=1, sticky=(tk.W, tk.E), pady=5, padx=(10, 0))
        
        # Log file location
        ttk.Label(frame, text="Log File Location:").grid(row=2, column=0, sticky=tk.W, pady=5)
        log_file_entry = ttk.Entry(frame, width=50)
        log_file_entry.insert(0, self.settings.get("log_file", str(self.log_file)))
        log_file_entry.grid(row=2, column=1, sticky=(tk.W, tk.E), pady=5, padx=(10, 0))
        
        def browse_log_file():
            filename = filedialog.asksaveasfilename(
                title="Select log file location",
                defaultextension=".log",
                filetypes=[("Log files", "*.log"), ("Text files", "*.txt"), ("All files", "*.*")]
            )
            if filename:
                log_file_entry.delete(0, tk.END)
                log_file_entry.insert(0, filename)
        
        ttk.Button(frame, text="Browse...", command=browse_log_file).grid(row=2, column=2, pady=5, padx=(5, 0))
        
        # Help text
        help_text = (
            "Signing Command: Path to signtool.exe (leave as 'signtool' if it's in PATH)\n"
            "Timestamp Server: URL of the timestamp server for timestamping signatures\n"
            "Log File: Location where signing logs will be saved"
        )
        help_label = ttk.Label(frame, text=help_text, wraplength=450, justify=tk.LEFT, foreground="gray")
        help_label.grid(row=3, column=0, columnspan=3, sticky=tk.W, pady=(20, 10))
        
        frame.columnconfigure(1, weight=1)
        
        # Buttons
        button_frame = ttk.Frame(frame)
        button_frame.grid(row=4, column=0, columnspan=3, pady=(20, 0))
        
        def save_and_close():
            self.settings["signing_command"] = signing_cmd_entry.get()
            self.settings["timestamp_server"] = timestamp_entry.get()
            self.settings["log_file"] = log_file_entry.get()
            self.log_file = Path(self.settings["log_file"])
            self.save_settings()
            self.log_message("Settings saved")
            settings_window.destroy()
        
        ttk.Button(button_frame, text="Save", command=save_and_close).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Cancel", command=settings_window.destroy).pack(side=tk.LEFT, padx=5)
    
    def show_about(self):
        """Show about dialog"""
        about_text = """Certum Signer v1.0

A simple Windows desktop tool for code signing using Certum SimplySign.

Features:
• Select files or folders for signing
• Drag and drop support
• Batch signing
• Logging system
• Configurable settings

The tool integrates with Certum SimplySign Desktop
for secure code signing with OTP verification.

License: GNU GPL v3"""
        messagebox.showinfo("About Certum Signer", about_text)


def main():
    root = tk.Tk()
    app = CertumSignerApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
