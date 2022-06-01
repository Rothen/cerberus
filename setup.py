from setuptools import setup

setup(
    name='cerberus',
    version='0.1',
    description='A useful module',
    author='Benajmin Ricchiuto',
    author_email='beni.ricchiuto@gmail.com',
    packages=['cerberus'],
    install_requires=['spidev', 'pybind11', 'reactivex', 'RPi.GPIO', 'websockets', 'asyncio'],
    entry_points={
        'console_scripts': [
            'cerberus = cerberus.__main__:main',
        ],
    }
)