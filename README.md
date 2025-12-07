# Certum Signer

A simple Windows desktop tool for code signing using **Certum SimplySign** and **SimplySign Desktop**.

## Features

✅ **Select Files** - Choose individual files to sign  
✅ **Select Folder** - Add all signable files from a folder  
✅ **Batch Signing** - Sign multiple files at once  
✅ **Automatic Verification** - Verifies each signature after signing  
✅ **Detailed Logging** - Complete command output and verification results  
✅ **Progress Logging** - Real-time log output with success/failure status  
✅ **File Logging** - All operations logged to a text file  
✅ **Configurable Settings** - Customize signing command, timestamp server, and log location  
✅ **Simple GUI** - Clean, Windows-style interface

## Requirements

### For Using the Pre-built Executable

1. **Windows 10/11**
2. **Certum SimplySign Desktop** installed and configured
3. **Windows SDK** (for signtool.exe) - Usually comes with Visual Studio or can be downloaded separately
   - Alternative: Add signtool.exe to your system PATH

### For Building from Source

1. **Python 3.8 or higher** (with tkinter - included in standard Windows Python)
2. **PyInstaller** (for creating the .exe)

## Quick Start (Using Pre-built .exe)

1. Make sure **Certum SimplySign Desktop** is installed and configured on your system
2. Ensure **signtool.exe** is available in your system PATH or configure the full path in Settings
3. Run **CertumSigner.exe**
4. Add files using "Select Files" or "Select Folder" buttons
5. Click "Sign All Files"
6. SimplySign Desktop will prompt for OTP when signing begins

## Building the Executable

### Windows

1. Install Python 3.8 or higher from [python.org](https://www.python.org/downloads/)
2. Open Command Prompt in the project directory
3. Install requirements:
   ```
   pip install -r requirements.txt
   ```
4. Run the build script:
   ```
   build.bat
   ```
5. The executable will be created in the `dist` folder as **CertumSigner.exe**

### Manual Build

```bash
pip install pyinstaller
python -m PyInstaller --onefile --windowed --name CertumSigner certum_signer.py
```

The standalone .exe will be in the `dist` folder.

## Usage

### Adding Files

**Method 1: Select Files Button**
- Click "Select Files"
- Choose one or more files to sign
- Supported formats: .exe, .dll, .msi, .cab, .ocx, .sys

**Method 2: Select Folder Button**
- Click "Select Folder"
- Choose a folder
- All signable files in the folder (and subfolders) will be added

### Signing Files

1. Add files using any of the methods above
2. Click "Sign All Files"
3. SimplySign Desktop will open and prompt for OTP
4. Enter your OTP code
5. Files will be signed sequentially
6. Check the log output for results

### Settings

Access settings via **File → Settings**

**Available Settings:**

- **Signing Command**: Path to signing tool (default: `signtool`)
  - **✅ RECOMMENDED**: Use `signtool` (or full path to signtool.exe)
    - If signtool is in your PATH, leave as `signtool`
    - Otherwise, provide full path: `C:\Program Files (x86)\Windows Kits\10\bin\10.0.22000.0\x64\signtool.exe`
    - signtool automatically integrates with SimplySign Desktop
  - **❌ NOT RECOMMENDED**: SimplySignDesktop.exe
    - Does NOT accept signtool command-line parameters
    - Will fail to sign files
    - Only use signtool.exe!

- **Timestamp Server**: URL for timestamping (default: `http://time.certum.pl`)
  - Certum's timestamp server: `http://time.certum.pl`
  - Alternative: `http://timestamp.digicert.com`

- **Log File Location**: Where signing logs are saved (default: `%USERPROFILE%\certum_signer.log`)

**⚠️ IMPORTANT**: 
- Always use **signtool.exe** for signing (NOT SimplySignDesktop.exe)
- signtool automatically integrates with SimplySign Desktop when you have it installed
- SimplySignDesktop.exe does not accept signtool command-line parameters
- The tool will warn you if you try to configure SimplySignDesktop.exe

## How It Works

The tool integrates with **Certum SimplySign Desktop** using the standard Windows code signing workflow:

1. The tool invokes `signtool.exe sign` with appropriate parameters
2. signtool detects the SimplySign virtual smart card
3. SimplySign Desktop prompts for OTP verification
4. Upon successful OTP entry, the file is signed
5. The signature is timestamped using the configured timestamp server
6. **The tool automatically verifies the signature** using `signtool.exe verify`
7. Verification results are logged with detailed output

### Detailed Logging

The tool logs:
- Complete command being executed
- All stdout and stderr from signtool
- Return codes
- Verification command and results
- Warning if signing reports success but verification fails

This helps identify issues like:
- Files appearing signed but having invalid signatures
- Timestamp server problems
- Certificate issues
- Authentication failures

**The tool does NOT:**
- Handle certificates directly
- Store or manage OTP codes
- Use PFX files or passwords
- Implement custom signing logic

All actual signing is performed by **Certum SimplySign Desktop** and **signtool.exe**.

## File Locations

### Settings File
`%USERPROFILE%\certum_signer_settings.json`

Contains:
```json
{
  "signing_command": "signtool",
  "timestamp_server": "http://time.certum.pl",
  "log_file": "C:\\Users\\YourName\\certum_signer.log"
}
```

### Log File
Default: `%USERPROFILE%\certum_signer.log`

All signing operations are logged here with timestamps.

## Troubleshooting

### Signing succeeds but verification shows "No signature found"

**This is the most common issue!**

**Cause**: You configured `SimplySignDesktop.exe` instead of `signtool.exe` in Settings.

**Why this fails**:
- `SimplySignDesktop.exe` does NOT accept signtool command-line parameters
- The signing command runs without error (return code 0) but doesn't actually sign anything
- Verification correctly detects that the file is NOT signed

**Solution**:
1. Go to **File → Settings**
2. Change **Signing Command** from:
   ```
   C:\Program Files\Certum\SimplySign Desktop\SimplySignDesktop.exe
   ```
   To:
   ```
   signtool
   ```
   Or the full path to signtool.exe:
   ```
   C:\Program Files (x86)\Windows Kits\10\bin\10.0.22000.0\x64\signtool.exe
   ```
3. Click **Save**
4. Try signing again

**Important**: signtool.exe automatically integrates with SimplySign Desktop. You don't need to call SimplySignDesktop.exe directly!

### "signtool not found" or command fails

**Solution**: Install Windows SDK or provide full path to signtool.exe in Settings
- Download Windows SDK from Microsoft
- Or locate signtool.exe on your system and add its directory to PATH
- Or set full path in Settings: `C:\Program Files (x86)\Windows Kits\10\bin\...\signtool.exe`

### SimplySign Desktop doesn't prompt for OTP

**Solution**: 
- Ensure SimplySign Desktop is running
- Check that your Certum certificate is installed correctly
- Verify SimplySign Desktop is configured properly
- Try signing manually with signtool first to test the setup

### "No files" or files not being added

**Solution**:
- Check file extensions (.exe, .dll, .msi, etc.)
- Ensure files are not in use by other programs
- Check file permissions

### Signing fails for all files

**Solution**:
- Test signtool manually: `signtool sign /tr http://time.certum.pl /td sha256 /fd sha256 /a test.exe`
- Check your Certum subscription is active
- Ensure you have signing permissions for the certificate
- Check internet connection (needed for timestamp server)

### Signing reports success but verification fails

**NEW**: The tool now automatically verifies signatures after signing.

**Possible causes**:
- Using SimplySignDesktop.exe for signing (verification requires signtool.exe)
- Timestamp server failed (file signed but not timestamped)
- Certificate chain issue
- System time incorrect
- Intermediate certificates missing

**Solution**:

**If using SimplySignDesktop.exe for signing**:
1. This is normal - SimplySignDesktop.exe doesn't support verification
2. The tool automatically searches for signtool.exe in Windows SDK locations
3. Install Windows SDK if you don't have it: https://developer.microsoft.com/windows/downloads/windows-sdk/
4. Alternative: Change signing command to use signtool.exe instead

**For other verification failures**:
1. Check the detailed log output for verification errors
2. Look for timestamp-related errors in the log
3. Try a different timestamp server in Settings
4. Ensure system date/time is correct
5. Check that certificate chain is complete in certificate store
6. Re-run the signing for failed files

**What to check in the log**:
- Look for "VERIFICATION FAILED" messages
- Check the "Verification output" section for specific errors
- If it says "Successfully verified" - the file is properly signed
- If verification timeout occurs, file may still be signed but check manually
- If using SimplySignDesktop.exe, you'll see a note about needing signtool for verification

## Technical Details

### Signing Command

The tool uses this signtool command:
```
signtool sign /tr <timestamp_server> /td sha256 /fd sha256 /a <file>
```

Parameters:
- `/tr` - Timestamp server URL (RFC 3161)
- `/td` - Timestamp digest algorithm (SHA256)
- `/fd` - File digest algorithm (SHA256)
- `/a` - Automatically select best certificate
- `<file>` - File to sign

### Supported File Types

The tool automatically detects and includes these file types when adding folders:
- `.exe` - Executables
- `.dll` - Dynamic libraries
- `.msi` - Windows installers
- `.cab` - Cabinet files
- `.ocx` - ActiveX controls
- `.sys` - System drivers

## License

GNU General Public License v3.0

See LICENSE file for details.

## Credits

Developed for use with:
- **Certum SimplySign** - Code signing service
- **Certum SimplySign Desktop** - Virtual smart card client
- **Microsoft SignTool** - Code signing utility

## Support

For issues with:
- **This tool**: Open an issue on GitHub
- **Certum SimplySign**: Contact Certum support
- **Certificate issues**: Contact Certum support
- **SignTool issues**: Check Microsoft documentation

---

**Version**: 1.0  
**Platform**: Windows 10/11  
**Requirements**: Certum SimplySign Desktop, Python 3.8+ (for building)
