# Simple FastAPI and REACT Inventory Management App

## Create a Virtual Conda Environment

```bash
conda create -p venv python=3.8 -y
```

## Create required files and folders.

1 - Run `template.py` file.
2 - In `main.py` file, include the API code. 
3 - Spin up the FastAPI server.
```bash
uvicorn main:app --reload --port <any unused port>
```
4 - Include all of the definitions of database fieldnames in `models.py` residing in models folder. Accordingly, include details in `main.py` file for accessing the details included in `models.py` file.
