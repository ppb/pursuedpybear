from setuptools import setup


def readme():
    with open('README.md') as f:
        return f.read()

setup(
    name='ppb',
    version='0.2.0',
    packages=['ppb'],
    install_requires=[
        'pygame',
    ],
    url='https://github.com/pathunstrom/pursuedpybear',
    license='',
    author='Piper Thunstrom',
    author_email='pathunstrom@gmail.com',
    description='An Event Driven Python Game Engine',
    long_description=readme(),
)
