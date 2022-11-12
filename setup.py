#!/usr/bin/env python3
from setuptools import setup


# See setup.cfg for the actual configuration.
setup(
    use_scm_version={
        'local_scheme': 'dirty-tag',
    },
)
