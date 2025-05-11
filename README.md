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
