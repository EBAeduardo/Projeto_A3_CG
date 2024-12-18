# Projeto A3 CG | Espada Aerondight - The Witcher

## Autores

* Pedro Henrique Kunz Gomes
* Julia Colares Pereira
* Eduardo Bianchini de Almeida
* Matheus Kremis Serdiuk Gazzana
* Thais Pires Gabriel

# Instalação e Execução do Projeto

Este projeto requer o Python na versão **3.12.0** ou superior. Para verificar a versão do Python instalada em sua máquina, execute o comando:

- **Windows:** `python --version`
- **macOS/Linux:** `python3 --version`

## Passos para Instalação

### 1. Preparação do Ambiente

O projeto inclui arquivos de instalação que automatizam a criação de um ambiente virtual (venv) e a instalação das dependências necessárias.

#### Para macOS ou Linux:

1. Adicione permissões para executar o script de instalação:
   
   `chmod +x install_env_mac_or_linux.sh`

2. Execute o script de instalação:

   `./install_env_mac_or_linux.sh`

#### Para Windows:

Execute o arquivo de instalação:

   `.\install_env_windows.bat`

### 2. Ativando o Ambiente Virtual (venv)

Após a execução do script de instalação, ative o ambiente virtual com o comando correspondente ao seu sistema operacional:

- **macOS/Linux:** `source venv/bin/activate`

- **Windows:** `venv\Scripts\activate`

Se você encontrar o erro "A execução de scripts foi desabilitada neste sistema" ao tentar ativar o ambiente virtual no Windows, será necessário ajustar a política de execução no PowerShell utilizando o seguinte comando:

   `Set-ExecutionPolicy -ExecutionPolicy Bypass -Scope Process`

Feito este ajuste, o script de ativação deve funcionar normalmente.

### 3. Executando o Projeto

Com o ambiente virtual ativado, você pode executar o projeto usando o seguinte comando:

- **macOS/Linux:** `python3 main.py`
- **Windows:** `python main.py`

