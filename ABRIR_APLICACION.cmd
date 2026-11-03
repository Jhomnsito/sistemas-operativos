@echo off
setlocal
cd /d "%~dp0codigo"
py -3 -c "import sys; sys.exit(sys.version_info < (3, 10))" >nul 2>&1
if not errorlevel 1 (
    py -3 app_visual.py %*
    goto :fin
)
if exist "%USERPROFILE%\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe" (
    "%USERPROFILE%\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe" app_visual.py %*
    goto :fin
)
python -c "import sys; sys.exit(sys.version_info < (3, 10))" >nul 2>&1
if not errorlevel 1 (
    python app_visual.py %*
    goto :fin
)
echo No se encontro Python 3.10 o posterior. Consulta README.md.
set "SO_RESULT=1"
goto :cerrar
:fin
set "SO_RESULT=%errorlevel%"
:cerrar
if /I not "%~1"=="--sin-pausa" pause
exit /b %SO_RESULT%

