from setuptools import setup, find_packages

setup(
    name='ws_bridge',
    version='1.0.0',
    url='https://github.com/iwanders/ws_bridge',
    author='Ivor Wanders',
    author_email='ivor@iwanders.net',
    description='This module provides a way to transfer a tcp connection through a websocket.',
    packages=find_packages(),    
    install_requires=['websockets==8.1'],
)
