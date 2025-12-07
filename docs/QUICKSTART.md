# Quick Start Guide - Getting Your .exe File

This guide will help you create the standalone **CertumSigner.exe** file in under 5 minutes.

## Prerequisites

✅ Windows 10 or 11  
✅ Internet connection (for downloading Python/PyInstaller)

## Option 1: Automated Setup (Recommended - Easiest!)

1. **Install Python** (if not already installed):
   - Download from: https://www.python.org/downloads/
   - ⚠️ **IMPORTANT**: During installation, check ☑️ "Add Python to PATH"
   - Click "Install Now"

2. **Run the setup script**:
   - Double-click `SETUP.bat`
   - Wait 1-2 minutes for the build to complete
   - Done! Your executable is in the `dist` folder

3. **Use the executable**:
   - Copy `dist\CertumSigner.exe` to any location
   - Double-click to run (no installation needed!)

## Option 2: Manual Steps

If you prefer to see what's happening:

```batch
REM 1. Install Python (see above)

REM 2. Open Command Prompt in this folder

REM 3. Install PyInstaller
python -m pip install pyinstaller

REM 4. Build the executable
python -m PyInstaller --onefile --windowed --name CertumSigner certum_signer.py

REM 5. Your .exe is now in the dist\ folder
```

## Option 3: Just Run the Python Script (No .exe)

If you have Python installed, you can run the tool directly without building an .exe:

```batch
python certum_signer.py
```

This works exactly the same as the .exe version!

## What Gets Created

After building, you'll have:

- ✅ `dist\CertumSigner.exe` - **This is what you want!**
- ⚠️ `build\` folder - Can be deleted (temporary build files)
- ⚠️ `CertumSigner.spec` - Can be deleted (build configuration)

## Distributing the .exe

The `CertumSigner.exe` file is:
- ✅ **Standalone** - No installation needed
- ✅ **Portable** - Copy anywhere and run
- ✅ **Self-contained** - All dependencies included
- ⚠️ **~10-15 MB** - Includes Python runtime

You can:
- Copy it to any Windows 10/11 computer
- Run it directly
- No Python installation needed on target computers

## First Run Notes

When you first run `CertumSigner.exe`:

1. Windows may show "Windows protected your PC" (SmartScreen)
   - Click "More info"
   - Click "Run anyway"
   - This is normal for unsigned executables

2. The app will start and show the main window

3. Configure settings (File → Settings):
   - Set path to signtool.exe if needed
   - Set timestamp server (default is fine)
   - Choose log file location

4. You're ready to sign files!

## Troubleshooting

### "Python is not recognized"
- Python is not installed or not in PATH
- Reinstall Python and check "Add Python to PATH"

### "pip is not recognized"
- pip is part of Python
- Try: `python -m pip install pyinstaller`

### Build takes a long time
- First build can take 2-3 minutes
- Subsequent builds are faster
- Be patient!

### .exe file is large
- This is normal (includes Python runtime)
- Typical size: 10-15 MB
- Can't be reduced without losing functionality

### Antivirus blocks the .exe
- Some antivirus tools are suspicious of PyInstaller .exe files
- Add exception for CertumSigner.exe
- Or run the Python script directly instead

## Need Help?

1. Check the main README.md
2. Make sure you have:
   - Python 3.8 or higher
   - Internet connection (first time only)
   - Windows 10/11

3. For signing issues:
   - Ensure Certum SimplySign Desktop is installed
   - Check signtool.exe is accessible
   - Test signing manually first

---

**That's it!** You now have a standalone .exe file ready to use.
