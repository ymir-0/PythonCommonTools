#!/usr/bin/env python3
import os

import setuptools

module_path = os.path.join(os.path.dirname(__file__), 'pythoncommontools/version.py')
version_line = [line for line in open(module_path)
                if line.startswith('__version__')][0]

__version__ = version_line.split('__version__ = ')[-1][1:][:-2]

import importlib
import pkgutil
import pythoncommontools
from os.path import isdir

# this code is an adaptation from https://stackoverflow.com/questions/3365740/how-to-import-all-submodules
def import_submodules(package, recursive=True):
    if isinstance(package, str):
        package = importlib.import_module(package)
    results = list()
    for loader, name, is_pkg in pkgutil.walk_packages(package.__path__):
        full_name = package.__name__ + '.' + name
        # continue recurtion only if module is folder
        print("loader.path="+loader.path)
        full_path=loader.path+"/"+name
        print("full_path="+full_path)
        if isdir(full_path):
            results.append(full_name)
            if recursive and is_pkg:
                results=results+(import_submodules(full_name))
    return results

package=pythoncommontools
results=[package.__name__]+import_submodules (package)
print("results="+str(results))

setuptools.setup(
    name="PythonCommonTools",
    version=__version__,
    description="common tools for Python",
    packages=results,
    install_requires=["psutil"],
    classifiers=[
        'Programming Language :: Python :: 3',
    ],
)
