"""
Handles opening files from the Python "VFS".

The VFS is the same file space that Python modules are imported from, so the
module spam.eggs comes from spam/eggs.py, and you can load spam/foo.png that
lives next to it.
"""
import logging
from pathlib import Path
import sys
try:
    import importlib.resources as impres
except ImportError:
    # Backport for Python 3.6
    import importlib_resources as impres

logger = logging.getLogger(__name__)


def _main_path():
    main = sys.modules['__main__']
    mainpath = getattr(main, '__file__')
    if mainpath:
        mainpath = Path(mainpath)
        return mainpath.absolute().parent
    else:
        # This primarily happens in REPL-ish situations, where __main__ isn't a
        # script but a purely virtual namespace.
        return Path.cwd()


def _splitpath(filepath):
    if filepath.startswith('/'):
        filepath = filepath[1:]
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

    logger.debug("Opening %s (%s, %s)", filepath, modulename, filename)

    if modulename == '__main__':
        # __main__ never has __spec__, so it can't resolve
        dirpath = _main_path()
        filepath = dirpath / filename
        if encoding is None:
            return filepath.open('rb')
        else:
            return filepath.open('rt', encoding=encoding, errors=errors)
    else:
        try:
            if encoding is None:
                return impres.open_binary(modulename, filename)
            else:
                return impres.open_text(modulename, filename, encoding, errors)
        except FileNotFoundError as exc:
            # Package is importable, but either:
            # * The file doesn't exist under it
            # * The package is a namespace, and has no single location
            if 'Package' in str(exc):  # "Package has no location ..."
                logger.warning("Did you forget __init__.py?")
            raise
        except ModuleNotFoundError:
            # The package is not importable
            # (This has to come after above to prevent multiple handlers)
            raise FileNotFoundError(f"Directory for {filepath} not found")


def exists(filepath):
    """
    Checks if the given resource exists and is a resources.
    """
    modulename, filename = _splitpath(filepath)
    if modulename == '__main__':
        # __main__ never has __spec__, so it can't resolve
        dirpath = _main_path()
        return (dirpath / filename).is_file()
    else:
        return impres.is_resource(modulename, filepath)


def iterdir(modulepath):
    modname = modulepath.replace('/', '.')
    if modname == '__main__':
        dirpath = _main_path()
        for item in dirpath.iterdir():
            yield item.name
    else:
        yield from impres.contents(modname)


def walk(modulepath):
    """
    Generates all the resources in the given package.
    """
    for name in iterdir(modulepath):
        fullname = f"{modulepath}/{name}"
        if exists(fullname):
            yield fullname
        elif modulepath != '__main__':
            # Don't recurse from __main__, that would be all installed packages.
            yield from walk(fullname)
