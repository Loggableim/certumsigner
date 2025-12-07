# Troubleshooting Guide

## Build Issues

### Issue: "pyinstaller is not recognized" or "Der Befehl 'pyinstaller' ist entweder falsch geschrieben..."

**Cause**: PyInstaller is installed but not in your system PATH, or the wrong command syntax is being used.

**Solution**:
1. Use `python -m pyinstaller` instead of just `pyinstaller`
2. The SETUP.bat and build.bat scripts have been updated to use this syntax
3. If you're building manually, use:
   ```batch
   python -m pyinstaller --onefile --windowed --name CertumSigner certum_signer.py
   ```

### Issue: Python not found

**Cause**: Python is not installed or not in PATH.

**Solution**:
1. Download Python from https://www.python.org/downloads/
2. During installation, **check the box** "Add Python to PATH"
3. Restart your command prompt after installation
4. Verify with: `python --version`

### Issue: pip not found

**Cause**: pip is not installed or Python installation is incomplete.

**Solution**:
1. Try: `python -m pip --version`
2. If that fails, reinstall Python with "pip" selected
3. Or download get-pip.py and run: `python get-pip.py`

### Issue: Build is very slow or hangs

**Cause**: PyInstaller analyzes all dependencies, which takes time.

**Solution**:
- Be patient - first build can take 2-5 minutes
- Don't interrupt the process
- Subsequent builds are faster

### Issue: Antivirus blocks the build process

**Cause**: Antivirus software may block PyInstaller.

**Solution**:
1. Temporarily disable antivirus
2. Add exceptions for:
   - Python folder
   - Project folder
   - PyInstaller
3. Re-enable antivirus after build

## Signing Issues

### Issue: "Das System kann die angegebene Datei nicht finden" (File not found)

**Cause**: signtool.exe is not found in your system PATH.

**Solution 1** - Install Windows SDK:
1. Download Windows SDK from Microsoft
2. Install "Windows SDK Signing Tools"
3. Add SDK bin folder to PATH, or...

**Solution 2** - Configure full path in Settings:
1. Find signtool.exe on your system:
   - Typical location: `C:\Program Files (x86)\Windows Kits\10\bin\10.0.xxxxx.0\x64\signtool.exe`
   - Search: Open File Explorer, search for "signtool.exe"
2. In CertumSigner: File → Settings
3. Set "Signing Command" to the full path:
   ```
   C:\Program Files (x86)\Windows Kits\10\bin\10.0.22621.0\x64\signtool.exe
   ```
4. Click Save

**Solution 3** - Add signtool to PATH:
1. Find signtool.exe location
2. Add that folder to your system PATH environment variable
3. Restart CertumSigner

### Issue: "No certificates found" or signing fails with certificate error

**Cause**: SimplySign Desktop is not configured or certificate is not installed.

**Solution**:
1. Install Certum SimplySign Desktop
2. Run SimplySign Desktop
3. Configure your certificate
4. Test manually:
   ```batch
   signtool sign /tr http://time.certum.pl /td sha256 /fd sha256 /a test.exe
   ```
5. If manual signing works, try CertumSigner again

### Issue: "Timestamp server error" or timeout

**Cause**: Cannot reach timestamp server (internet issue or server down).

**Solution 1** - Check internet connection:
- Ensure you have internet access
- Check firewall settings

**Solution 2** - Try different timestamp server:
1. File → Settings
2. Change "Timestamp Server" to alternative:
   - `http://timestamp.digicert.com`
   - `http://timestamp.sectigo.com`
   - `http://timestamp.globalsign.com`
3. Save and try again

**Solution 3** - Temporarily sign without timestamp (not recommended):
- Edit the command in Settings to remove `/tr` parameter
- Note: Signature will be invalid after certificate expires

### Issue: OTP prompt doesn't appear

**Cause**: SimplySign Desktop is not running or not configured properly.

**Solution**:
1. Start SimplySign Desktop manually
2. Check SimplySign Desktop settings
3. Verify certificate is active and valid
4. Try signing one file manually to test OTP flow
5. If OTP works manually, try CertumSigner again

### Issue: Signing works but signature is invalid

**Cause**: Wrong signing parameters or certificate issues.

**Solution**:
1. Verify signature manually:
   ```batch
   signtool verify /pa /v signed_file.exe
   ```
2. Check that timestamp was applied
3. Ensure certificate is valid and not expired
4. Verify signing parameters in Settings

### Issue: File is in use / access denied

**Cause**: The file you're trying to sign is running or locked.

**Solution**:
1. Close the application/service using the file
2. Use Task Manager to end the process
3. Try signing again
4. Copy file to different location and sign the copy

### Issue: "Invalid file format" or "Not a valid PE file"

**Cause**: Trying to sign a file that isn't a Windows executable.

**Solution**:
- Only sign: .exe, .dll, .msi, .cab, .ocx, .sys files
- Check file is actually a Windows executable
- Verify file is not corrupted

## Runtime Issues

### Issue: Application crashes on startup

**Cause**: Missing dependencies or corrupted installation.

**Solution 1** - Run from Python directly:
```batch
python certum_signer.py
```
This will show detailed error messages.

**Solution 2** - Rebuild the executable:
```batch
python -m pyinstaller --onefile --windowed --name CertumSigner certum_signer.py --clean
```

**Solution 3** - Check Python version:
- Requires Python 3.8 or higher
- Update Python if needed

### Issue: Settings don't save

**Cause**: No write permissions to home directory.

**Solution**:
1. Run as Administrator
2. Or change log file location to a folder you can write to
3. Check if `certum_signer_settings.json` exists in `%USERPROFILE%`

### Issue: Log file not created

**Cause**: Invalid log file path or no permissions.

**Solution**:
1. File → Settings
2. Set log file to a valid, writable location:
   ```
   C:\Users\YourName\Documents\certum_signer.log
   ```
3. Ensure the folder exists
4. Check write permissions

### Issue: Can't add files to list

**Cause**: File dialog not working or files not in supported format.

**Solution**:
1. Check file extensions are supported (.exe, .dll, .msi, etc.)
2. Try "Select Folder" instead
3. Check file permissions
4. Try running as Administrator

### Issue: UI is slow or frozen

**Cause**: Signing is in progress or thread issue.

**Solution**:
1. Wait for signing to complete (check log output)
2. Don't close the application during signing
3. If truly frozen, close and restart
4. Check log file for errors

## Windows Security Issues

### Issue: Windows SmartScreen blocks the .exe

**Cause**: Executable is not digitally signed.

**Solution**:
1. Click "More info"
2. Click "Run anyway"
3. This is normal for unsigned .exe files
4. Optionally: Sign CertumSigner.exe itself with your certificate!

### Issue: Antivirus deletes or quarantines CertumSigner.exe

**Cause**: False positive detection (common with PyInstaller executables).

**Solution**:
1. Add exception in your antivirus
2. Restore from quarantine
3. Submit as false positive to antivirus vendor
4. Optionally: Sign the .exe with your certificate to reduce false positives

## Getting Help

### Before Asking for Help

1. Check this troubleshooting guide
2. Read README.md for detailed documentation
3. Check QUICKSTART.md for setup instructions
4. Review USAGE_EXAMPLES.md for common scenarios

### Test Signing Manually

Before reporting issues, test signing manually:

```batch
REM Find signtool
where signtool

REM Test signing a file
signtool sign /tr http://time.certum.pl /td sha256 /fd sha256 /a test.exe

REM Verify signature
signtool verify /pa /v test.exe
```

If manual signing fails, the issue is with your signing setup (certificate, SimplySign Desktop, signtool), not with CertumSigner.

### Information to Include When Reporting Issues

1. **Error message** - Exact error text from log
2. **Python version** - Output of `python --version`
3. **Operating System** - Windows version
4. **What you tried** - Steps you followed
5. **Log file** - Contents of certum_signer.log
6. **Manual test** - Results of manual signtool test

### Common Support Resources

- **Python issues**: https://www.python.org/community/
- **PyInstaller issues**: https://github.com/pyinstaller/pyinstaller
- **Certum SimplySign**: Contact Certum support
- **signtool issues**: Microsoft documentation
- **Certificate issues**: Contact Certum support

## Quick Fixes Checklist

If something doesn't work, try these in order:

- [ ] Restart the application
- [ ] Check internet connection
- [ ] Verify Python is in PATH: `python --version`
- [ ] Verify signtool is accessible: `signtool /?`
- [ ] Start SimplySign Desktop manually
- [ ] Test signing one file manually with signtool
- [ ] Check log file for detailed errors
- [ ] Run as Administrator
- [ ] Temporarily disable antivirus
- [ ] Rebuild the executable with `--clean` flag
- [ ] Run from Python source: `python certum_signer.py`

## Still Having Issues?

1. **Check GitHub Issues** - Someone may have had the same problem
2. **Read documentation again** - README.md, QUICKSTART.md, USAGE_EXAMPLES.md
3. **Test components separately**:
   - Python installation
   - PyInstaller
   - signtool
   - SimplySign Desktop
   - Your certificate
4. **Ask for help** with detailed information (see above)

---

**Most Common Issues and Quick Fixes**:

| Issue | Quick Fix |
|-------|-----------|
| pyinstaller not found | Use `python -m pyinstaller` instead |
| signtool not found | Install Windows SDK or set full path in Settings |
| No OTP prompt | Start SimplySign Desktop manually |
| Build very slow | Be patient, first build takes 2-5 minutes |
| Antivirus blocks | Add exception for Python, project folder, and .exe |
| SmartScreen warning | Click "More info" → "Run anyway" |
