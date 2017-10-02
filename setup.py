from setuptools import Command, find_packages, setup
from dj import __version__


setup(
    name='dj',
    version=__version__,
    description='CLI for managing django project',
    url='',
    author='Avinash',
    author_email='avistylein3105@gmail.com',
    license='MIT',
    keywords='cli',
    packages=find_packages(exclude=['docs', 'tests*']),
    entry_points={
        'console_scripts': [
            'dj=dj.cli:main',
        ],
    },
)
