# coding=utf-8
# imports
from enum import Enum , unique

from pythoncommontools.objectUtil.objectUtil import objectStringRepresentation
# common REST WS response wrapper
class CommonRestWrap :
    # representations
    def __repr__( self ):
        return objectStringRepresentation( self )
    def __str__( self ):
        return self.__repr__()
    # constructors
    def __init__( self, errors = None, warnings = None, dataArea = None ):
        self.errors = errors
        self.warnings = warnings
        self.dataArea = dataArea
# common REST WS response markups
@unique
class CommonRestWrapMarkup( Enum ):
    errorsArea = "errorsArea"
    warningsArea = "warningsArea"
    dataArea = "dataArea"
