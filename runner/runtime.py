import os

def detect_runtime(path):

    files = os.listdir(path)

    # Python
    if (
        "requirements.txt" in files
        or "pyproject.toml" in files
        or "setup.py" in files
        or any(f.endswith(".py") for f in files)
    ):
        return "python"

    # Node
    if "package.json" in files:
        return "node"

    # PHP
    if "index.php" in files:
        return "php"

    return "unknown"
