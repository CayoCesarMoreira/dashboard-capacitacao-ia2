@echo off
chcp 65001 > nul
title Dashboard de Capacitação em IA & ML

echo =======================================================
echo   Iniciando Dashboard de Capacitação em IA & ML
echo =======================================================
echo.

cd /d "%~dp0"

:: 1. Verifica se o Python está instalado
python --version > nul 2>&1
if %errorlevel% neq 0 (
    echo [ERRO] Python não foi encontrado no sistema!
    echo Por favor, instale o Python em: https://www.python.org/downloads/
    echo Certifique-se de marcar a opção "Add Python to PATH" durante a instalação.
    echo.
    pause
    exit /b
)

:: 2. Instala dependências automaticamente se necessário
echo [1/3] Verificando dependências necessárias...
python -m pip install -q --disable-pip-version-check -r requirements.txt

:: 3. Consolida as planilhas (une as duas bases e gera base_consolidada_final.xlsx)
echo [2/3] Consolidando planilhas de dados...
python consolidar.py
if %errorlevel% neq 0 (
    echo [AVISO] O script de consolidação retornou um erro. O dashboard tentará usar a base existente.
    echo.
)

:: 4. Executa o Dashboard
echo [3/3] Abrindo o Dashboard no seu navegador...
echo.
echo Para encerrar o painel, feche esta janela.
echo.

python -m streamlit run app.py --server.port 8501 --browser.gatherUsageStats false

pause
