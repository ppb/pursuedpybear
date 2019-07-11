import concurrent.futures
import ppb.vfs as vfs


_executor = concurrent.futures.ThreadPoolExecutor()
_resources = {}  # maps resource names to futures


def _load(filename):
    with vfs.open(filename) as file:
        return file.read()


def hint(filename):
    """
    Hint that a resource will probably be needed
    """
    _resources[filename] = _executor.submit(_load, filename)


def load(filename):
    """
    Get the contents of a resource
    """
    if filename not in _resources:
        hint(filename)
    return _resources[filename].result()
