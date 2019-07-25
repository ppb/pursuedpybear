import ast
from pathlib import Path
import subprocess
import sys


def get_docstring(path):
    tree = ast.parse(path.read_text(), path.name, mode='exec')

    return ast.get_docstring(tree)


for script in Path(__file__).resolve().parent.glob('*.py'):
    if script.name.startswith('_'):
        continue
    ds = get_docstring(script)
    print("=" * len(script.name))
    print(script.name)
    print("=" * len(script.name))
    print("")
    if ds is not None:
        print(ds)
        print("")
    subprocess.run([sys.executable, str(script)], check=True)
