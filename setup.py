#!/usr/bin/env python3
import os

import setuptools

module_path = os.path.join(os.path.dirname(__file__), 'pythoncommontools/version.py')
version_line = [line for line in open(module_path)
                if line.startswith('__version__')][0]

__version__ = version_line.split('__version__ = ')[-1][1:][:-2]

setuptools.setup(
    name="PythonCommonTools",
    version=__version__,
    description="common tolls for Python",
    packages=[""],
    install_requires=["psutil"],
    classifiers=[
        'Programming Language :: Python :: 3',
    ],
    # py_modules=['helloworldpython3.HelloWorldPython3'],
    #package_dir=["pythoncommontools"],
)
