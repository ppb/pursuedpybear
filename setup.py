from setuptools import setup


def readme():
    with open('README.md') as file:
        return file.read()

setup(
    name='ppb',
    version='0.3.0',
    packages=['ppb'],
    install_requires=[
        'pygame',
        'ppb-vector',
    ],
    url='https://github.com/ppb/pursuedpybear',
    license='Artistic-2.0',
    author='Piper Thunstrom',
    author_email='pathunstrom@gmail.com',
    description='A Python Game Engine',
    long_description=readme(),
    long_description_content_type="text/markdown",
    classifiers=[
        'License :: OSI Approved :: Artistic License',
        'Programming Language :: Python :: 3.6',
        'Topic :: Games/Entertainment',
        'Topic :: Education'
    ]
)
