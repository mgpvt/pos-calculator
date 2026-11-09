@echo off
setlocal
title Shop Calculator - Backup
rem ------------------------------------------------------------------
rem  Double-click to back up the Shop Calculator project and signing key.
rem  - Asks where to save (a USB drive or any folder).
rem  - Makes a NEW dated folder each time, and never deletes anything.
rem  - Skips rebuildable clutter (node_modules, build, .gradle, www).
rem  Test options (not needed normally):  set DRYRUN=1  = list only,  set KEYSRC=...  = other key folder
rem ------------------------------------------------------------------

set "PROJ=%~dp0.."
pushd "%PROJ%"
set "PROJ=%CD%"
popd
if not defined KEYSRC set "KEYSRC=D:\Dev\keys\shopcalculator"

echo.
echo  SHOP CALCULATOR - BACKUP
echo  ------------------------
echo  Project folder : %PROJ%
echo  Signing key    : %KEYSRC%
echo.

set "DEST=%~1"
if "%DEST%"=="" set /p "DEST=Where should the backup go? (for example F:\ShopCalculator-Backup): "
if "%DEST%"=="" (
  echo.
  echo  Nothing was entered, so no backup was made.
  pause
  exit /b 1
)
set "DEST=%DEST:"=%"
if "%DEST:~-1%"=="\" set "DEST=%DEST:~0,-1%"

for /f %%i in ('powershell -NoProfile -Command "Get-Date -Format yyyy-MM-dd_HHmm"') do set "STAMP=%%i"
set "OUT=%DEST%\%STAMP%"
set "OPT="
if defined DRYRUN set "OPT=/L"

if not defined DRYRUN mkdir "%OUT%" 2>nul
if not defined DRYRUN if not exist "%OUT%" (
  echo.
  echo  Could not create "%OUT%". Check that the drive is plugged in and not full.
  pause
  exit /b 1
)

echo  Saving to: %OUT%
echo.
echo  [1/2] Copying the project ...
robocopy "%PROJ%" "%OUT%\project" /E /XD node_modules .gradle build www /XF local.properties /R:1 /W:1 /NFL /NDL /NP /NJH %OPT%
set "RC1=%ERRORLEVEL%"

echo.
echo  [2/2] Copying the signing key ...
set "RC2=0"
if exist "%KEYSRC%" (
  robocopy "%KEYSRC%" "%OUT%\keys" /E /R:1 /W:1 /NFL /NDL /NP /NJH %OPT%
  set "RC2=%ERRORLEVEL%"
) else (
  echo  WARNING: the signing key folder was not found: %KEYSRC%
)

echo.
echo  ----------------------------------------------------------
if %RC1% GEQ 8 goto :failed
if %RC2% GEQ 8 goto :failed
if defined DRYRUN (
  echo  TEST RUN ONLY - nothing was copied.
) else (
  echo  BACKUP FINISHED:  %OUT%
  echo.
  echo  Reminder: keep the "keys" folder in TWO places
  echo  - for example this drive AND a private cloud drive.
)
echo  ----------------------------------------------------------
echo.
pause
exit /b 0

:failed
echo  BACKUP HAD ERRORS (a file could not be copied).
echo  Check the messages above, then run this again.
echo  ----------------------------------------------------------
echo.
pause
exit /b 1
