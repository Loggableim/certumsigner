# Certum Official Documentation Reference

## Source Document

The official Certum documentation for code signing is available at:
**CS-Code_Signing_in_the_Cloud_Signtool_jarsigner_signing.pdf**

This document provides Certum's official instructions for using signtool and jarsigner with their SimplySign Desktop solution.

## Key Information from Certum Documentation

### Signtool Signing Command (Certum Official)

```batch
signtool sign /sha1 "<thumbprint>" /tr <timestamp_server> /td sha256 /fd sha256 /v "<file>"
```

**Parameters:**
- `/sha1 <thumbprint>` - Certificate thumbprint (fingerprint)
- `/tr <timestamp_server>` - Timestamp server URL
- `/td sha256` - Timestamp digest algorithm
- `/fd sha256` - File digest algorithm
- `/v` - Verbose output

**Example:**
```batch
signtool sign /sha1 "90986e3ac5febff4cf998f174e82cb4c9e6ffc19" /tr http://time.certum.pl /td sha256 /fd sha256 /v "file.exe"
```

### Our Implementation vs Certum's Documentation

**Certum Documentation Uses:**
- `/sha1 <thumbprint>` to explicitly specify the certificate

**Our Implementation Uses:**
- `/a` to automatically select the best certificate

**Why we use `/a`:**
1. Simpler for users - no need to find thumbprint
2. Works perfectly with SimplySign Desktop
3. Automatically selects the appropriate certificate
4. Less error-prone

Both approaches are valid and work with SimplySign Desktop.

### Verification Command (Certum Official)

```batch
signtool verify /pa /all <file>
```

**Our Implementation:**
```batch
signtool verify /pa /all /v <file>
```

We added `/v` (verbose) for more detailed output in logs.

## Finding Certificate Thumbprint (If Needed)

If you want to use `/sha1 <thumbprint>` instead of `/a`:

1. Open Certificate Manager (certmgr.msc)
2. Navigate to: Personal → Certificates
3. Double-click your Certum certificate
4. Go to "Details" tab
5. Scroll to "Thumbprint" field
6. Copy the thumbprint value (e.g., "90986e3ac5febff4cf998f174e82cb4c9e6ffc19")

Then modify the signing command in Settings to use:
```
signtool sign /sha1 "YOUR_THUMBPRINT_HERE" /tr http://time.certum.pl /td sha256 /fd sha256 /v
```

## Batch Signing (Certum Approach)

Certum's documentation shows batch signing by:
1. Creating a .bat file with multiple signtool commands
2. Each command signs a different file
3. Running the .bat file once

**Our Approach:**
- GUI-based batch signing
- Add multiple files to the list
- Click "Sign All Files" once
- Tool automatically signs each file sequentially

Both achieve the same result - our approach is more user-friendly.

## Timestamp Server

Certum's official timestamp server: **http://time.certum.pl**

This is the default in our application.

## File Types Supported

According to Certum documentation:
- .exe (executables)
- .dll (libraries)
- .msi (installers)
- .cab (cabinet files)
- .ocx (ActiveX controls)
- .sys (system drivers)

Our application supports all these file types.

## References

- Certum Documentation: CS-Code_Signing_in_the_Cloud_Signtool_jarsigner_signing.pdf
- Certum Support: https://support.certum.eu/
- Certum Website: https://www.certum.pl/

## Implementation Notes

The Certum Signer tool follows Certum's official guidelines with some user-friendly enhancements:
1. **Automatic certificate selection** (`/a` instead of manual thumbprint)
2. **GUI instead of command-line** batch files
3. **Automatic verification** after each signing
4. **Detailed logging** of all commands and outputs
5. **Error detection** to catch false positives

All enhancements are compatible with Certum SimplySign Desktop and follow the same underlying signtool principles documented by Certum.
