from setuptools import setup


def readme():
    with open('README.md') as file:
        return file.read()

def requirements(section=None):
    if section is None:
        filename = "requirements.txt"
    else:
        filename = f"requirements-{section}.txt"

    with open(filename) as file:
        return [line.strip() for line in file]

setup(
    name='ppb',
    version='0.5.0',
    packages=['ppb', 'ppb.systems'],
    install_requires=requirements(),
    tests_require=requirements('tests'),
    python_requires=">=3.6",
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
