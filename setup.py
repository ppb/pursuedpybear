from setuptools import setup
import sys


def readme():
    with open('README.md') as file:
        return file.read()

backports = []

if sys.version_info < (3, 7):
    backports += ['dataclasses']

setup(
    name='ppb',
    version='0.3.0',
    packages=['ppb'],
    install_requires=[
        'pygame',
        'ppb-vector',
    ] + backports,
    url='https://github.com/pathunstrom/pursuedpybear',
    license='',
    author='Piper Thunstrom',
    author_email='pathunstrom@gmail.com',
    description='An Event Driven Python Game Engine',
    long_description=readme(),
)
