# coding=utf-8
# imports
from configparser import ConfigParser
# global initialization
loadedConfiguration = None
# read configuration
def loadConfiguration( configurationFilePath ):
    global loadedConfiguration
    if not loadedConfiguration:
        loadedConfiguration = ConfigParser ( )
        loadedConfiguration.read( configurationFilePath )
