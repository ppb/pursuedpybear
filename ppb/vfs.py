"""
Handles opening files from the Python "VFS".
"""
try:
    import importlib.resources as impres
except ImportError:
    # Backport
    import importlib_resources as impres


def _splitpath(filepath):
    if '/' in filepath:
        slashed, filename = filepath.rsplit('/', 1)
        modulename = slashed.replace('/', '.')
    else:
        modulename = '__main__'
        filename = filepath

    return modulename, filename


def open(filepath, *, encoding=None, errors='strict'):
    """
    Opens the given file, whose name is resolved with the import machinery.

    If you want a text file, pass an encoding argument.

    Returns the open file and the base filename (suitable for filename-based type hinting).
    """
    modulename, filename = _splitpath(filepath)

    if encoding is None:
        return impres.open_binary(modulename, filename), filename
    else:
        return impres.open_text(modulename, filename, encoding, errors), filename


def exists(filepath):
    """
    Checks if the given resource exists and is a resources.
    """
    modulename, filename = _splitpath(filepath)
    return impres.is_resource(modulename, filepath)


def iterdir(modulepath):
    modname = modulepath.replace('/', '.')
    yield from impres.contents(modname)


def walk(modulepath):
    """
    Generates all the resources in the given package.
    """
    for name in iterdir(modulepath):
        fullname = f"{modulepath}/{name}"
        if exists(fullname):
            yield fullname
        else:
            yield from walk(fullname)
