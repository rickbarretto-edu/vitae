# Vitae

## Requirements

- [PostgreSQL](https://www.postgresql.org/)
- [Python Poetry](https://python-poetry.org/)

## How to run it

1. **Install all dependencies**

```
poetry install
```

2. **Create a new Environment Settings**
    

```bash
cp vitae.example.toml vitae.toml
# Now edit it to use your own settings
```

3. **Enter the virtual environment**

```bash
poetry shell
```

On *Visual Studio Code*: <kbd>Ctrl</kbd> + <kbd>Shift</kbd> + <kbd>P</kbd>,
then search for: *"Python: Select Interpreter"* and choose the one from Poetry's isolated environment.

4. **Set PYTHONPATH**


```bash
export PYTHONPATH="/path/to/your/project/"
```

5. **Execute**

```bash
python -m src
```

## Tooling Recomentation

1. **DBA tools**
  - [Beekeeper Studio](https://www.beekeeperstudio.io/) for SQL Queries. (Community ed. for Free)
  - [ChartDB](https://github.com/chartdb/chartdb) for Diagram visualization. (Self-hosted for free)
  - **pgAdmin 4**, general purpose. Comes with PostgreSQL. (Free)
2. **Python Linters, Formatters, Static Analysis**
  - [`ruff`](https://docs.astral.sh/ruff/) linter and code formatter. (lightweight alternative)
  - [`ty`](https://github.com/astral-sh/ty) Python type checking. (lightweight alternative)
  - [Pylance](https://marketplace.visualstudio.com/items?itemName=ms-python.vscode-pylance) VsCode's Extension 
    as language server.