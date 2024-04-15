@echo off

pyinstaller --onefile ".\\main.py"

if ERRORLEVEL 1 (
  echo Error: Failed to create executable with pyinstaller.
  exit /b 1
)

echo Executable created successfully!
