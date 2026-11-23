@echo off
title Dashboard Capacitacao IA
echo Iniciando Dashboard de Capacitacao em IA, ML e Ciencia de Dados...
cd /d "%~dp0"
python -m streamlit run app.py --server.port 8501
pause
