#!/bin/bash

VENV_NAME="venv"

if ! command -v python3 &> /dev/null; then
    echo "Python3 não está instalado. Por favor, instale o Python3 para continuar."
    exit 1
fi

echo "Criando o ambiente virtual: $VENV_NAME"
python3 -m venv $VENV_NAME

echo "Ativando o ambiente virtual"
source $VENV_NAME/bin/activate

if [ -f "requirements.txt" ]; then
    echo "Instalando as dependências do requirements.txt"
    pip install --upgrade pip
    pip install -r requirements.txt
else
    echo "Arquivo requirements.txt não encontrado. Nenhuma dependência foi instalada."
fi

echo "Ambiente virtual configurado com sucesso. Use 'source $VENV_NAME/bin/activate' para ativá-lo. Após isso, você deve executar o comando 'python3 main.py' para iniciar o programa."
