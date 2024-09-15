import atexit

from setuptools import find_packages, setup


def print_message():
    print('Type `amber` in the CLI to start searching file content.')


atexit.register(print_message)

with open('requirements.txt') as f:
    requirements = [line for line in f.read().splitlines() if line]

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name='amber',
    version="0.1.0",
    description='File search tool using OpenAI assistant.',
    long_description=long_description,
    long_description_content_type="text/markdown",
    url='https://github.com/hansololz/amber',
    keywords=["amber", 'openai', 'file search'],
    packages=find_packages(),
    include_package_data=True,
    python_requires='>=3.12',
    install_requires=requirements,
    entry_points={
        'console_scripts': [
            'amber = amber.amber:main',
        ]
    },
    license='GPL',
)
