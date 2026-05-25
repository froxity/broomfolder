@echo off
setlocal
set "SCRIPT_DIR=%~dp0"
set "REPO_DIR=%SCRIPT_DIR%.."

where py >nul 2>nul
if %ERRORLEVEL%==0 (
  py -3 "%REPO_DIR%\broomfolder.py" %*
  exit /b %ERRORLEVEL%
)

where python >nul 2>nul
if %ERRORLEVEL%==0 (
  python "%REPO_DIR%\broomfolder.py" %*
  exit /b %ERRORLEVEL%
)

echo Python 3 is required to run broomfolder. 1>&2
exit /b 1
