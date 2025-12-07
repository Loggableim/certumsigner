@echo off
REM Build script for creating standalone CertumSigner.exe
REM Requires Python 3.8+ and PyInstaller

echo Building Certum Signer executable...
echo.

REM Check if PyInstaller is installed
python -m pip show pyinstaller >nul 2>&1
if %errorlevel% neq 0 (
    echo PyInstaller not found. Installing...
    python -m pip install pyinstaller
)

REM Build the executable
echo Creating standalone executable...
pyinstaller --onefile --windowed --name CertumSigner --icon=NONE certum_signer.py

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
