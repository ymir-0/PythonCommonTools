#!/usr/bin/env python3
# import generic modules
from os.path import join, dirname, isdir
from setuptools import setup
from importlib import import_module
from pkgutil import walk_packages
# parse recursively a module
# this code is an adaptation from https://stackoverflow.com/questions/3365740/how-to-import-all-submodules
def import_submodules(package):
    if isinstance(package, str):
        package = import_module(package)
    modules = list()
    for loader, name, is_pkg in walk_packages(package.__path__):
        full_name = package.__name__ + '.' + name
        full_path=join(loader.path,name)
        # continue recursion only if module is folder
        if is_pkg and isdir(full_path):
            modules.append(full_name)
            modules=modules+(import_submodules(full_name))
    return modules
# import and parse dedicated module
import pythoncommontools
rootPackage=pythoncommontools
module_path = join(dirname(__file__), rootPackage.__name__ , "version.py")
version_line = [line for line in open(module_path) if line.startswith("__version__")][0]
__version__ = version_line.split('__version__ = ')[-1][1:][:-2]
modules=[rootPackage.__name__]+import_submodules (rootPackage)
print("loaded modules : " + str(modules))
# define setup parameters
setup(
    name="PythonCommonTools",
    version=__version__,
    description="common tools for Python",
    packages=modules,
    install_requires=["psutil"],
    classifiers=[
        'Programming Language :: Python :: 3',
    ],
)
