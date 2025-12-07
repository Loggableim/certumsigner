# Certum Signer

A simple Windows desktop tool for code signing using **Certum SimplySign** and **SimplySign Desktop**.

## Features

✅ **Select Files** - Choose individual files to sign  
✅ **Select Folder** - Add all signable files from a folder  
✅ **Batch Signing** - Sign multiple files at once  
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
pyinstaller --onefile --windowed --name CertumSigner certum_signer.py
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

**Method 3: Drag and Drop** (requires tkinterdnd2)
- Drag files or folders directly onto the file list
- Note: Basic version uses file selection dialogs

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

- **Signing Command**: Path to signtool.exe (default: `signtool`)
  - If signtool is in your PATH, leave as `signtool`
  - Otherwise, provide full path: `C:\Program Files (x86)\Windows Kits\10\bin\10.0.22000.0\x64\signtool.exe`

- **Timestamp Server**: URL for timestamping (default: `http://time.certum.pl`)
  - Certum's timestamp server: `http://time.certum.pl`
  - Alternative: `http://timestamp.digicert.com`

- **Log File Location**: Where signing logs are saved (default: `%USERPROFILE%\certum_signer.log`)

## How It Works

The tool integrates with **Certum SimplySign Desktop** using the standard Windows code signing workflow:

1. The tool invokes `signtool.exe` with appropriate parameters
2. signtool detects the SimplySign virtual smart card
3. SimplySign Desktop prompts for OTP verification
4. Upon successful OTP entry, the file is signed
5. The signature is timestamped using the configured timestamp server

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
