@echo off
REM Build script for creating standalone CertumSigner.exe
REM Requires Python 3.8+ and PyInstaller

echo Building Certum Signer executable...
echo.

REM Check if Python is available
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ERROR: Python is not installed or not in PATH
    echo Please install Python from https://www.python.org/downloads/
    echo.
    pause
    exit /b 1
)

REM Check if PyInstaller is installed, install if not
echo Checking for PyInstaller...
python -c "import pyinstaller" 2>nul
if %errorlevel% neq 0 (
    echo PyInstaller not found. Installing...
    python -m pip install --upgrade pip
    python -m pip install pyinstaller
    echo.
)

REM Build the executable
echo Creating standalone executable...
python -m pyinstaller --onefile --windowed --name CertumSigner certum_signer.py

echo.
if exist "dist\CertumSigner.exe" (
    echo Build successful!
    echo Executable location: dist\CertumSigner.exe
    echo.
    echo You can now copy CertumSigner.exe from the dist folder to any location.
) else (
    echo Build failed. Please check the errors above.
)

pause
