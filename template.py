import os

dirs = [
    os.path.join("webapp", "static"),
    os.path.join("webapp", "templates"),
    "models",
    "utils",
    "project"
]

for dir_ in dirs:
    os.makedirs(dir_, exist_ok=True)
    with open(os.path.join(dir_, ".gitkeep"), "w") as f:
        pass


files = [
    os.path.join("project", "__init__.py"),
    os.path.join("utils", "__init__.py"),
    os.path.join("models", "__init__.py"),
    os.path.join("models", "models.py"),
    os.path.join("webapp", "static", "style.css"),
    os.path.join("webapp", "templates", "index.html"),
    "requirements.txt"
]

for file_ in files:
    with open(file_, "w") as f:
        pass