@echo off
echo Starting Thai PDF Searcher...
"C:\Program Files\Python312\python.exe" -m streamlit run app.py
if %ERRORLEVEL% NEQ 0 (
    echo.
    echo Attempting alternative launch...
    python -m streamlit run app.py
)
if %ERRORLEVEL% NEQ 0 (
    echo.
    echo Failed to start. Please ensure Python and Streamlit are installed.
)
pause
