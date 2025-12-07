# Usage Examples

## Example 1: Sign a Single .exe File

1. Run CertumSigner.exe
2. Click "Select Files"
3. Browse to your .exe file (e.g., `MyApp.exe`)
4. Click "Open"
5. Click "Sign All Files"
6. SimplySign Desktop will prompt for your OTP
7. Enter your OTP code
8. File is signed!

**Log output:**
```
[2025-12-07 10:30:00] Starting signing process for 1 files...
[2025-12-07 10:30:00] Signing: MyApp.exe
[2025-12-07 10:30:15] ✓ Successfully signed: MyApp.exe
[2025-12-07 10:30:15] === Signing Complete ===
[2025-12-07 10:30:15] Successful: 1
[2025-12-07 10:30:15] Failed: 0
[2025-12-07 10:30:15] Total: 1
```

## Example 2: Sign Multiple Files

1. Click "Select Files"
2. Hold Ctrl and select multiple files:
   - `app.exe`
   - `library.dll`
   - `installer.msi`
3. Click "Open"
4. All 3 files appear in the list
5. Click "Sign All Files"
6. Enter OTP when prompted (once for all files)
7. All files are signed sequentially

## Example 3: Sign All Files in a Folder

1. Click "Select Folder"
2. Browse to your build output folder: `C:\Projects\MyApp\bin\Release`
3. Click "Select Folder"
4. All .exe, .dll, .msi, etc. files are automatically added (including subfolders)
5. Click "Sign All Files"
6. Enter OTP
7. All files in the folder are signed

**Tip:** This is great for signing all files in a build directory!

## Example 4: Configure Settings for First Use

If signtool.exe is not in your PATH:

1. Click "File" → "Settings"
2. For "Signing Command", enter full path:
   ```
   C:\Program Files (x86)\Windows Kits\10\bin\10.0.22000.0\x64\signtool.exe
   ```
3. Leave "Timestamp Server" as default: `http://time.certum.pl`
4. Set "Log File Location" to where you want logs:
   ```
   C:\Logs\certum_signer.log
   ```
5. Click "Save"

## Example 5: Batch Signing with Log Review

Scenario: You have 20 DLL files to sign

1. Click "Select Files"
2. Select all 20 DLL files
3. Click "Sign All Files"
4. Wait for signing to complete
5. Review the log output in the bottom panel
6. Check for any failures:
   - ✓ = Success
   - ✗ = Failed
7. See summary at the end

**If some files fail:**
- Check the error message in the log
- Common issues:
  - File is in use (close the application)
  - No internet connection (for timestamp server)
  - Wrong file type (not a PE file)

## Example 6: Using Different Timestamp Servers

If Certum's timestamp server is down:

1. File → Settings
2. Change "Timestamp Server" to alternative:
   - DigiCert: `http://timestamp.digicert.com`
   - Sectigo: `http://timestamp.sectigo.com`
   - GlobalSign: `http://timestamp.globalsign.com`
3. Click "Save"
4. Try signing again

## Example 7: Verifying Signed Files

After signing, verify the signature:

**Option 1: Windows Explorer**
- Right-click the signed file
- Choose "Properties"
- Go to "Digital Signatures" tab
- You should see your Certum certificate

**Option 2: signtool (recommended)**
```batch
signtool verify /pa /v MyApp.exe
```

Expected output:
```
Verifying: MyApp.exe
Signature Index: 0 (Primary Signature)
Hash of file (sha256): ...
Signing Certificate Chain:
    ...
    Issued to: Your Company Name
    ...
Successfully verified: MyApp.exe
```

## Example 8: Automating with Command Line

While CertumSigner is a GUI tool, you can still automate signing:

**Create a list of files:**
1. Add files to the tool
2. Save the session (note: this feature can be added if needed)
3. Click "Sign All Files"

**Alternative: Use signtool directly in scripts:**
```batch
for %%f in (*.exe *.dll) do (
    signtool sign /tr http://time.certum.pl /td sha256 /fd sha256 /a %%f
)
```

## Example 9: Signing Files from Different Locations

You can add files from multiple folders:

1. Click "Select Files" → Choose files from `C:\Project1\bin\`
2. Click "Select Files" again → Choose files from `C:\Project2\build\`
3. Click "Select Folder" → Add folder `C:\ThirdParty\libs\`
4. All files from all locations are in the list
5. Click "Sign All Files" → Signs everything at once

## Example 10: Troubleshooting a Failed Signing

If a file fails to sign:

1. Check the log output for the specific error
2. Common errors:

**"No certificates found"**
- SimplySign Desktop not configured
- Certificate not installed
- Solution: Run SimplySign Desktop, check configuration

**"File in use"**
- Application is running
- Solution: Close the application, try again

**"Invalid file format"**
- File is not a PE executable
- Solution: Only sign .exe, .dll, .msi, .cab, etc.

**"Timestamp server error"**
- No internet connection
- Timestamp server is down
- Solution: Check internet, try different timestamp server

3. Try signing the file manually:
```batch
signtool sign /tr http://time.certum.pl /td sha256 /fd sha256 /a "C:\path\to\file.exe"
```

4. If manual signing works, the issue is with the tool configuration
5. If manual signing fails, the issue is with your signing setup

## Tips and Best Practices

1. **Always use timestamp servers** - Signatures remain valid even after certificate expires
2. **Test signing on a copy first** - Make backups before bulk signing
3. **Check the log after signing** - Verify all files were signed successfully
4. **Keep your OTP device handy** - You'll need it every time you sign
5. **Use "Select Folder" for builds** - Easier than selecting individual files
6. **Review failed files** - Don't ignore errors in the log
7. **Verify signatures** - Always check a few signed files to ensure they're properly signed

## Need More Help?

- Check README.md for detailed documentation
- Check QUICKSTART.md for setup instructions
- Test signtool manually to verify your setup
- Contact Certum support for certificate/OTP issues
