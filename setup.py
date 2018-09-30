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
    version='0.4.0',
    packages=['ppb'],
    install_requires=[
        'pygame',
        'ppb-vector',
    ] + backports,
    url='https://github.com/ppb/pursuedpybear',
    license='Artistic-2.0',
    author='Piper Thunstrom',
    author_email='pathunstrom@gmail.com',
    description='An Event Driven Python Game Engine',
    long_description=readme(),
    long_description_content_type="text/markdown",
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Education",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: Artistic License",
        "Natural Language :: English",
        "Programming Language :: Python :: 3.7",
        "Topic :: Games/Entertainment",
        "Topic :: Software Development :: Libraries",
    ]
)
