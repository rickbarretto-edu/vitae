# Guia de Execução do Projeto

## Pré-requisitos

- Windows 10/11 com [WSL (Windows Subsystem for Linux)](https://learn.microsoft.com/en-us/windows/wsl/install) instalado
- Distribuição do Ubuntu instalada via WSL
- Python 3 instalado no Ubuntu
- `requirements.txt` com as dependências do projeto

## Passo a passo para rodar o projeto

1. **Abrir o Ubuntu via WSL**

   No terminal do Windows (CMD ou PowerShell), execute:

   ```bash
   wsl -d Ubuntu
    ```

2. **Criar .env com base no .env.example**
    
    No terminal do Ubuntu, execute:

    ```bash
    cp .env.example .env
    ```

    e set as as variáveis de ambiente necessárias no arquivo `.env`.

2. **Configurar o PYTHONPATH**

   No terminal do Ubuntu, execute:

   ```bash
   export PYTHONPATH="${PYTHONPATH}:/path/to/your/project/"
   ```

3. **Criar um ambiente virtual**

   No terminal do Ubuntu, execute:

   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```

4. **Instalar as dependências**
    
    No terminal do Ubuntu, execute:
    
    ```bash
    pip install -r requirements.txt
    ```

5. **Executar o projeto**  

   No terminal do Ubuntu, execute:

   ```bash
   python3 -m src.main
   ```
