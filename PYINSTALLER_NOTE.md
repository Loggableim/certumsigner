# Important Note About PyInstaller

## Module Name vs Package Name

PyInstaller has a **case-sensitive** difference between its pip package name and Python module name:

- **pip package name**: `pyinstaller` (all lowercase)
- **Python module name**: `PyInstaller` (capital P and I)

## What This Means

### Installing PyInstaller ✅
```bash
pip install pyinstaller
# or
python -m pip install pyinstaller
```
Use **lowercase** when installing.

### Running PyInstaller ✅
```bash
python -m PyInstaller --onefile --windowed certum_signer.py
```
Use **capital P and I** when running as a module.

### Common Errors

❌ **Wrong**: `python -m pyinstaller` (lowercase)
```
No module named pyinstaller
```

✅ **Correct**: `python -m PyInstaller` (capital P and I)

❌ **Wrong**: Just `pyinstaller` (if not in PATH)
```
'pyinstaller' is not recognized as an internal or external command
```

✅ **Correct**: `python -m PyInstaller` (always works)

## Why Use `python -m PyInstaller`?

1. **Works without PATH**: PyInstaller scripts may not be in your system PATH
2. **Explicit Python version**: Uses the same Python that you used to install packages
3. **Portable**: Works on any system where PyInstaller is installed
4. **Reliable**: Doesn't depend on PATH configuration

## Quick Reference

| Task | Command |
|------|---------|
| Install | `pip install pyinstaller` (lowercase) |
| Run | `python -m PyInstaller script.py` (capital P and I) |
| Check if installed | `python -c "import PyInstaller"` (capital P and I) |

## Already Updated

All scripts in this project now use the correct capitalization:
- ✅ SETUP.bat
- ✅ build.bat
- ✅ README.md
- ✅ QUICKSTART.md
- ✅ TROUBLESHOOTING.md

You don't need to change anything - just use the provided scripts!
