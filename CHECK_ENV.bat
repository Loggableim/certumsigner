@echo off
REM Environment check script for Certum Signer
REM Verifies that all prerequisites are met before building

echo ========================================
echo Certum Signer - Environment Check
echo ========================================
echo.

set ERROR_COUNT=0

REM Check Python
echo [1/5] Checking Python...
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo   [FAIL] Python not found
    echo   Install from: https://www.python.org/downloads/
    set /a ERROR_COUNT+=1
) else (
    python --version
    echo   [OK] Python found
)
echo.

REM Check pip
echo [2/5] Checking pip...
python -m pip --version >nul 2>&1
if %errorlevel% neq 0 (
    echo   [FAIL] pip not found
    set /a ERROR_COUNT+=1
) else (
    python -m pip --version
    echo   [OK] pip found
)
echo.

REM Check PyInstaller
echo [3/5] Checking PyInstaller...
python -c "import PyInstaller; print('  Version:', PyInstaller.__version__)" 2>nul
if %errorlevel% neq 0 (
    echo   [WARN] PyInstaller not installed
    echo   Run SETUP.bat or: pip install pyinstaller
) else (
    echo   [OK] PyInstaller installed
)
echo.

REM Check signtool (optional for building, required for signing)
echo [4/5] Checking signtool...
where signtool >nul 2>&1
if %errorlevel% neq 0 (
    echo   [WARN] signtool.exe not in PATH
    echo   You'll need to configure the full path in Settings
    echo   Or install Windows SDK
) else (
    for /f "tokens=*" %%i in ('where signtool') do echo   [OK] signtool found: %%i
)
echo.

REM Check Certum SimplySign Desktop (can't easily check, just inform)
echo [5/5] Certum SimplySign Desktop check...
echo   [INFO] Please ensure SimplySign Desktop is installed
echo   This check cannot be automated
echo.

REM Summary
echo ========================================
echo Summary
echo ========================================
if %ERROR_COUNT% equ 0 (
    echo [SUCCESS] All required components found!
    echo.
    echo You can now:
    echo   - Run SETUP.bat to build the .exe
    echo   - Run build.bat to build manually
    echo   - Run: python src\certum_signer.py directly
) else (
    echo [ERROR] %ERROR_COUNT% required component(s) missing
    echo Please install the missing components and run this check again
)
echo ========================================
echo.

pause
