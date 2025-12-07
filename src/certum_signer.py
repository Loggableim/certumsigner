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
import glob
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
        list_frame = ttk.LabelFrame(main_frame, text="Files to Sign", padding="5")
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
        verified_count = 0
        
        self.log_message(f"Starting signing process for {len(self.files_to_sign)} files...")
        self.log_message("")
        
        for file_path in self.files_to_sign:
            try:
                # Build and log the signing command
                cmd = self._build_sign_command(file_path)
                self.log_message(f"=" * 80)
                self.log_message(f"Processing: {file_path}")
                self.log_message(f"Command: {' '.join(cmd)}")
                self.log_message("")
                
                # Execute signing
                self.log_message(f"Executing signtool...")
                result = subprocess.run(
                    cmd,
                    capture_output=True,
                    text=True,
                    timeout=120  # 2 minute timeout per file
                )
                
                # Log the complete output
                self.log_message(f"Return code: {result.returncode}")
                if result.stdout:
                    self.log_message(f"Standard output:")
                    for line in result.stdout.strip().split('\n'):
                        self.log_message(f"  {line}")
                if result.stderr:
                    self.log_message(f"Standard error:")
                    for line in result.stderr.strip().split('\n'):
                        self.log_message(f"  {line}")
                self.log_message("")
                
                # Check return code
                if result.returncode == 0:
                    self.log_message(f"Signtool reported success for: {os.path.basename(file_path)}")
                    
                    # Verify the signature
                    self.log_message(f"Verifying signature...")
                    is_verified, verify_msg = self._verify_signature(file_path)
                    
                    if is_verified:
                        success_count += 1
                        verified_count += 1
                        self.log_message(f"✓ VERIFIED: File is properly signed: {os.path.basename(file_path)}")
                    else:
                        failure_count += 1
                        self.log_message(f"✗ VERIFICATION FAILED: Signature not valid!", error=True)
                        self.log_message(f"  Verification output: {verify_msg}", error=True)
                        self.log_message(f"  WARNING: File may appear signed but signature is invalid!", error=True)
                else:
                    failure_count += 1
                    self.log_message(f"✗ Signtool failed for: {os.path.basename(file_path)}", error=True)
                    
                self.log_message("")
                    
            except subprocess.TimeoutExpired:
                failure_count += 1
                self.log_message(f"✗ Timeout signing: {os.path.basename(file_path)}", error=True)
                self.log_message("")
            except FileNotFoundError:
                failure_count += 1
                self.log_message(f"✗ Error signing {os.path.basename(file_path)}: signtool.exe not found", error=True)
                self.log_message(f"  Please install Windows SDK or configure the full path in Settings", error=True)
                self.log_message(f"  Current command: {self.settings.get('signing_command', 'signtool')}", error=True)
                self.log_message("")
            except Exception as e:
                failure_count += 1
                self.log_message(f"✗ Error signing {os.path.basename(file_path)}: {e}", error=True)
                self.log_message("")
        
        # Summary
        self.log_message("=" * 80)
        self.log_message(f"=== Signing Complete ===")
        self.log_message(f"Total files processed: {len(self.files_to_sign)}")
        self.log_message(f"Successfully signed and verified: {verified_count}")
        self.log_message(f"Failed or unverified: {failure_count}")
        self.log_message("=" * 80)
        
        # Re-enable button
        self.root.after(0, lambda: self.sign_button.config(state='normal'))
        self.root.after(0, lambda: self.status_label.config(text="Ready"))
        
        # Show completion message
        if failure_count == 0:
            self.root.after(0, lambda: messagebox.showinfo("Success", 
                f"All {verified_count} files signed and verified successfully!"))
        else:
            self.root.after(0, lambda: messagebox.showwarning("Completed with Errors", 
                f"Verified: {verified_count}\nFailed: {failure_count}\n\nCheck log for details."))
    
    def _verify_signature(self, file_path):
        """Verify that a file is properly signed
        
        Always uses signtool.exe for verification, regardless of the signing tool used.
        SimplySignDesktop.exe doesn't support verification commands.
        
        Returns:
            tuple: (is_valid: bool, message: str)
        """
        try:
            # Always use signtool for verification, even if user configured a different signing tool
            # SimplySignDesktop.exe doesn't support the verify command
            signing_tool = self.settings.get("signing_command", "signtool")
            
            # Check if user configured SimplySignDesktop or another non-signtool binary
            if "simplysign" in signing_tool.lower():
                # Try to find signtool.exe in common locations
                signtool_path = self._find_signtool()
                if not signtool_path:
                    self.log_message("Note: Verification requires signtool.exe, but using SimplySignDesktop.exe for signing")
                    self.log_message("Attempting to find signtool.exe in system...")
                    # Try just 'signtool' - maybe it's in PATH
                    signtool_path = "signtool"
                verify_tool = signtool_path
            else:
                verify_tool = signing_tool
            
            # Build verify command (using Certum's official verification parameters)
            verify_cmd = [
                verify_tool,
                "verify",
                "/pa",   # Verify using default authentication verification policy
                "/all",  # Verify all signatures (Certum official documentation)
                "/v",    # Verbose output
                file_path
            ]
            
            self.log_message(f"Verify command: {' '.join(verify_cmd)}")
            
            # Execute verification
            result = subprocess.run(
                verify_cmd,
                capture_output=True,
                text=True,
                timeout=30
            )
            
            # Log verification output
            if result.stdout:
                self.log_message(f"Verification output:")
                for line in result.stdout.strip().split('\n'):
                    self.log_message(f"  {line}")
            if result.stderr:
                self.log_message(f"Verification errors:")
                for line in result.stderr.strip().split('\n'):
                    self.log_message(f"  {line}")
            
            # Check if verification succeeded
            if result.returncode == 0:
                # Additional check: look for "Successfully verified" in output
                if "Successfully verified" in result.stdout:
                    return True, "Signature verified successfully"
                else:
                    return False, "Verification returned success but confirmation not found in output"
            else:
                return False, result.stdout + "\n" + result.stderr
                
        except subprocess.TimeoutExpired:
            return False, "Verification timeout"
        except FileNotFoundError:
            return False, "signtool.exe not found for verification - install Windows SDK"
        except Exception as e:
            return False, f"Verification error: {str(e)}"
    
    def _find_signtool(self):
        """Try to find signtool.exe in common Windows SDK locations
        
        Returns:
            str: Path to signtool.exe or None if not found
        """
        # Common Windows SDK locations
        sdk_paths = [
            r"C:\Program Files (x86)\Windows Kits\10\bin\*\x64\signtool.exe",
            r"C:\Program Files (x86)\Windows Kits\10\bin\*\x86\signtool.exe",
            r"C:\Program Files (x86)\Windows Kits\8.1\bin\x64\signtool.exe",
            r"C:\Program Files (x86)\Windows Kits\8.1\bin\x86\signtool.exe",
            r"C:\Program Files\Windows Kits\10\bin\*\x64\signtool.exe",
        ]
        
        for pattern in sdk_paths:
            matches = glob.glob(pattern)
            if matches:
                # Return the first match (usually the newest SDK version)
                return matches[0]
        
        return None
    
    def _build_sign_command(self, file_path):
        """Build the signing command
        
        Based on Certum's official documentation, there are two approaches:
        1. Use /a to auto-select certificate (current implementation - works with SimplySign Desktop)
        2. Use /sha1 <thumbprint> to specify exact certificate
        
        Current implementation uses /a which is simpler and works well with SimplySign Desktop.
        Reference: CS-Code_Signing_in_the_Cloud_Signtool_jarsigner_signing.pdf
        
        IMPORTANT: You should use signtool.exe, NOT SimplySignDesktop.exe for signing.
        signtool automatically integrates with SimplySign Desktop when you have it installed.
        """
        # This builds the command for Certum SimplySign
        # Default command uses signtool which integrates with SimplySign Desktop
        
        signing_tool = self.settings.get("signing_command", "signtool")
        timestamp_server = self.settings.get("timestamp_server", "http://time.certum.pl")
        
        # Warn if user configured SimplySignDesktop.exe directly
        if "simplysign" in signing_tool.lower() and "simplysigndesktop.exe" in signing_tool.lower():
            self.log_message("=" * 80, error=True)
            self.log_message("⚠ WARNING: You configured SimplySignDesktop.exe as the signing tool!", error=True)
            self.log_message("", error=True)
            self.log_message("SimplySignDesktop.exe does NOT accept signtool command-line parameters!", error=True)
            self.log_message("This will likely result in files NOT being signed.", error=True)
            self.log_message("", error=True)
            self.log_message("CORRECT CONFIGURATION:", error=True)
            self.log_message("  Use 'signtool' or the full path to signtool.exe", error=True)
            self.log_message("  signtool automatically integrates with SimplySign Desktop", error=True)
            self.log_message("", error=True)
            self.log_message("To fix:", error=True)
            self.log_message("  1. Go to File → Settings", error=True)
            self.log_message("  2. Change 'Signing Command' to: signtool", error=True)
            self.log_message("  3. Or use full path: C:\\Program Files (x86)\\Windows Kits\\10\\bin\\...\\signtool.exe", error=True)
            self.log_message("=" * 80, error=True)
            self.log_message("")
        
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
            "Signing Command: Use 'signtool' (NOT SimplySignDesktop.exe!)\n"
            "  • Leave as 'signtool' if it's in your PATH\n"
            "  • Or provide full path to signtool.exe from Windows SDK\n"
            "  • signtool integrates automatically with SimplySign Desktop\n\n"
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
            signing_cmd = signing_cmd_entry.get()
            
            # Warn if user is trying to use SimplySignDesktop.exe
            if "simplysigndesktop.exe" in signing_cmd.lower():
                warning_msg = (
                    "⚠ WARNING: You configured SimplySignDesktop.exe\n\n"
                    "SimplySignDesktop.exe does NOT work with signtool command-line parameters!\n"
                    "Your files will NOT be signed with this configuration.\n\n"
                    "CORRECT CONFIGURATION:\n"
                    "• Use 'signtool' (if in PATH)\n"
                    "• Or full path to signtool.exe from Windows SDK\n\n"
                    "signtool automatically integrates with SimplySign Desktop.\n\n"
                    "Do you want to continue anyway?"
                )
                if not messagebox.askyesno("Configuration Warning", warning_msg, icon='warning'):
                    return
            
            self.settings["signing_command"] = signing_cmd
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
• Batch signing
• Real-time logging
• File-based logs
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
