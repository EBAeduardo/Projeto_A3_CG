@echo off

set VENV_NAME=venv

python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo Python3 não está instalado. Por favor, instale o Python3 para continuar.
    exit /b 1
)

echo Criando o ambiente virtual: %VENV_NAME%
python -m venv %VENV_NAME%

echo Ativando o ambiente virtual
call %VENV_NAME%\Scripts\activate

if exist requirements.txt (
    echo Instalando as dependências do requirements.txt
    pip install --upgrade pip
    pip install -r requirements.txt
) else (
    echo Arquivo requirements.txt não encontrado. Nenhuma dependência foi instalada.
)

echo Ambiente virtual configurado com sucesso.
echo Use "%VENV_NAME%\Scripts\activate" para ativá-lo.
echo Após isso, execute o comando "python main.py" para iniciar o programa.
pause
