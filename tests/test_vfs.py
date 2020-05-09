import contextlib
import os
import tempfile

import __main__  # The pytest entry point

import pytest

import ppb.vfs


@contextlib.contextmanager
def save_main_file():
    value = __main__.__file__
    try:
        yield
    finally:
        __main__.__file__ = value


@pytest.fixture
def cwd_file():
    # Windows doesn't like multiple open handles, so we need to close and
    # delete the temp file manually.

    with tempfile.NamedTemporaryFile(dir=os.getcwd(), delete=False) as ntf:
        ntf.close()
        yield os.path.basename(ntf.name)
        os.remove(ntf.name)


def test_main_normal(cwd_file):
    with pytest.raises(FileNotFoundError):
        with ppb.vfs.open(cwd_file):
            pass


def test_main_none(cwd_file):
    with save_main_file():
        __main__.__file__ = None
        with ppb.vfs.open(cwd_file):
            pass


def test_main_missing(cwd_file):
    with save_main_file():
        del __main__.__file__
        with ppb.vfs.open(cwd_file):
            pass
