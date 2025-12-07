@echo off
REM Quick setup script for Certum Signer
REM This script will help you create the standalone CertumSigner.exe

echo ========================================
echo Certum Signer - Quick Setup
echo ========================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERROR] Python is not installed or not in PATH.
    echo.
    echo Please install Python 3.8 or higher from:
    echo https://www.python.org/downloads/
    echo.
    echo Make sure to check "Add Python to PATH" during installation.
    echo.
    pause
    exit /b 1
)

echo [OK] Python found
python --version

REM Check if pip is available
python -m pip --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERROR] pip is not available
    pause
    exit /b 1
)

echo [OK] pip found
echo.

REM Install PyInstaller
echo Installing PyInstaller (this may take a moment)...
python -m pip install --upgrade pyinstaller

echo.
echo Creating standalone executable...
echo This may take 1-2 minutes...
echo.

REM Create the executable
pyinstaller --onefile --windowed --name CertumSigner certum_signer.py

echo.
echo ========================================
if exist "dist\CertumSigner.exe" (
    echo [SUCCESS] Build completed!
    echo.
    echo The executable is located at:
    echo   %CD%\dist\CertumSigner.exe
    echo.
    echo You can now:
    echo   1. Copy CertumSigner.exe to any location
    echo   2. Run it directly - no installation needed
    echo   3. Delete the build/ folder to save space
    echo.
    echo Note: The first run may be slow while Windows scans the file.
) else (
    echo [ERROR] Build failed!
    echo Please check the error messages above.
)
echo ========================================
echo.

pause
