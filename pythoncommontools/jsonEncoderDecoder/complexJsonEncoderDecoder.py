# coding=utf-8
# @see : https://pymotw.com/2/json/ (it is for python 2, but it is adaptable for python 3)
# imports
from collections import Iterable
from copy import deepcopy
from enum import Enum , unique
from importlib import import_module
from inspect import signature
from json import JSONDecoder , JSONEncoder , dumps , loads
from sys import maxsize
from pythoncommontools.logger import logger
from pythoncommontools.objectUtil.objectUtil import methodArgsStringRepresentation
# encryption markup
@unique
class EncryptionMarkup( Enum ):
    class_ = "className"
    module = "moduleName"
# encode from objects to JSON
class ComplexJsonEncoder(  ):
    # methods
    @staticmethod
    def dumpComplexObject ( rawObject ):
        # logger context
        argsStr = methodArgsStringRepresentation( signature( ComplexJsonEncoder.dumpComplexObject ).parameters,locals() )
        # logger input
        logger.loadedLogger.input ( __name__ , ComplexJsonEncoder.__name__ ,ComplexJsonEncoder.dumpComplexObject.__name__ , message = argsStr )
        # upgade object
        ugradedObject=deepcopy(rawObject)
        setattr(ugradedObject, EncryptionMarkup.class_.value, rawObject.__class__.__name__)
        setattr(ugradedObject, EncryptionMarkup.module.value, rawObject.__module__)
        # complex type
        # encode object
        jsonObject = dumps(ugradedObject.__dict__)
        # logger output
        logger.loadedLogger.output ( __name__ , ComplexJsonEncoder.__name__ ,ComplexJsonEncoder.dumpComplexObject.__name__ , message = jsonObject )
        # return
        return jsonObject
# decode from JSON to objects
class ComplexJsonDecoder(  ):
    @staticmethod
    def loadComplexObject ( jsonObject):
        # logger context
        argsStr = methodArgsStringRepresentation( signature( ComplexJsonDecoder.loadComplexObject ).parameters, locals() )
        # logger input
        logger.loadedLogger.input ( __name__ , ComplexJsonDecoder.__name__ ,ComplexJsonDecoder.loadComplexObject.__name__ , message = argsStr )
        # load json object into dictionnary
        dictObject = loads(jsonObject)
        # initiate instantiated object
        instantiatedObject=dictObject
        # warn if was not encoded with 'ComplexJsonEncoder'
        if EncryptionMarkup.class_.value not in dictObject or EncryptionMarkup.module.value not in dictObject:
            logger.loadedLogger.warning(__name__, ComplexJsonDecoder.__name__,ComplexJsonDecoder.loadComplexObject.__name__, message="This object was not encoded with 'ComplexJsonEncoder', so it will kept as dictionnary")
        # otherwise, continue decoding
        else:
            # load module
            moduleName=dictObject[EncryptionMarkup.module.value]
            importedModule=import_module(moduleName)
            # load class
            className=dictObject[EncryptionMarkup.class_.value]
            loadedClass=getattr(importedModule,className)
            # instanciate object
            instantiatedObject=loadedClass()
            # update class attributs
            instantiatedObject.__dict__.update(dictObject)
        # logger output
        logger.loadedLogger.output ( __name__ , ComplexJsonDecoder.__name__ ,ComplexJsonDecoder.loadComplexObject.__name__ , message = instantiatedObject )
        # return instantiated object
        return instantiatedObject
#------------------------------------------------
class ComplexJsonEncoder_ORIGINAL( JSONEncoder ):
    # methods
    @staticmethod
    def setBrokerObject ( objectRaw ):
        # logger context
        argsStr = methodArgsStringRepresentation( signature( ComplexJsonEncoder.setBrokerObject ).parameters, locals() )
        # logger input
        logger.loadedLogger.input ( __name__ , ComplexJsonEncoder.__name__ ,
                                    ComplexJsonEncoder.setBrokerObject.__name__ , message = argsStr )
        # create JSON object
        objectBroker = deepcopy( objectRaw )
        # transform objects
        if getattr( objectBroker, "__dict__", False ) :
            # dump each field
            for fieldName, fieldValue in objectBroker.__dict__.items():
                setattr( objectBroker, fieldName, ComplexJsonEncoder.setBrokerObject( fieldValue ) )
        # transform iterable field
        elif isinstance( objectBroker, ( tuple, set, frozenset ) ) :
            convertedList = list()
            for originalElement in objectBroker:
                convertedElement = ComplexJsonEncoder.setBrokerObject( originalElement )
                convertedList.append( convertedElement )
            objectBroker = convertedList
        # transform exception
        elif isinstance( objectBroker, Exception ) :
            objectBroker = ComplexJsonEncoder.setBrokerObject( objectBroker.args )
        # logger output
        logger.loadedLogger.output ( __name__ , ComplexJsonEncoder.__name__ ,
                                     ComplexJsonEncoder.setBrokerObject.__name__ , message = objectBroker )
        # return
        return objectBroker
    @staticmethod
    def dumpComplexObject ( objectRaw ):
        # logger context
        argsStr = methodArgsStringRepresentation( signature( ComplexJsonEncoder.dumpComplexObject ).parameters,
                                                  locals() )
        # logger input
        logger.loadedLogger.input ( __name__ , ComplexJsonEncoder.__name__ ,
                                    ComplexJsonEncoder.dumpComplexObject.__name__ , message = argsStr )
        # dump complex object
        objectBroker = ComplexJsonEncoder.setBrokerObject( objectRaw )
        objectJson = dumps( objectBroker, cls = ComplexJsonEncoder )
        # logger output
        logger.loadedLogger.output ( __name__ , ComplexJsonEncoder.__name__ ,
                                     ComplexJsonEncoder.dumpComplexObject.__name__ , message = objectJson )
        # return
        return objectJson
    def default( self, objectToENcodeJson ):
        # logger context
        argsStr = methodArgsStringRepresentation( signature( ComplexJsonEncoder.default ).parameters, locals() )
        # logger input
        logger.loadedLogger.input ( __name__ , ComplexJsonEncoder.__name__ , ComplexJsonEncoder.default.__name__ ,
                                    message = argsStr )
        # initialize JSON encoding
        encodingDict = dict()
        # encode object information
        encodingDict[EncryptionMarkup.class_.value] = objectToENcodeJson.__class__.__name__
        if hasattr( objectToENcodeJson, EncryptionMarkup.module.value ):
            encodingDict[EncryptionMarkup.module.value] = objectToENcodeJson.__module__
        # encode object fields
        encodingDict.update( objectToENcodeJson.__dict__ )
        # logger output
        logger.loadedLogger.output ( __name__ , ComplexJsonEncoder.__name__ , ComplexJsonEncoder.default.__name__ ,
                                     message = encodingDict )
        # return JSON encoding
        return encodingDict
class ComplexJsonDecoder_ORIGINAL( JSONDecoder ):
    # methods
    @staticmethod
    def recursiveConvertAttribut ( objectToInspect, convertionType, recursiveAttributsIterable ):
        # logger context
        argsStr = methodArgsStringRepresentation( signature( ComplexJsonDecoder.recursiveConvertAttribut ).parameters, locals() )
        # logger input
        logger.loadedLogger.input ( __name__ , ComplexJsonDecoder.__name__ ,
                                    ComplexJsonDecoder.recursiveConvertAttribut.__name__ , message = argsStr )
        # set an attributs list
        recursiveAttributsList = list( recursiveAttributsIterable )
        # convert iterable fields
        if type( objectToInspect ) != str and isinstance( objectToInspect, Iterable ):
            for objectElement in objectToInspect:
                ComplexJsonDecoder.recursiveConvertAttribut ( objectElement, convertionType, recursiveAttributsList )
        # convert non-iterable fields
        else:
            # get first field
            currentAttributName = recursiveAttributsList.pop( 0 )
            # check field is present in object
            if hasattr( objectToInspect, currentAttributName ):
                # get field value
                rawAttributValue = getattr( objectToInspect, currentAttributName )
                # skip none value
                if rawAttributValue:
                    # convert remaining sub-fields
                    if len( recursiveAttributsList ) > 0:
                        ComplexJsonDecoder.recursiveConvertAttribut ( rawAttributValue, convertionType,
                                                                      recursiveAttributsList )
                    # convert field
                    else :
                        convertedAttributValue = convertionType( rawAttributValue )
                        setattr( objectToInspect, currentAttributName, convertedAttributValue )
        # logger output
        logger.loadedLogger.output ( __name__ , ComplexJsonDecoder.__name__ ,
                                     ComplexJsonDecoder.recursiveConvertAttribut.__name__ )
    @staticmethod
    def loadComplexObject ( objectJson, convertingDict = dict(), rootIterationType = None ):
        # logger context
        argsStr = methodArgsStringRepresentation( signature( ComplexJsonDecoder.loadComplexObject ).parameters, locals() )
        # logger input
        logger.loadedLogger.input ( __name__ , ComplexJsonDecoder.__name__ ,
                                    ComplexJsonDecoder.loadComplexObject.__name__ , message = argsStr )
        # load instantiated object
        convertedObjectJson = objectJson.replace( ": None", ": null" )
        # double quotes must be used as string delimiters in JSON
        singleQuoteMarkup = "'"
        doubleQuoteMarkup = '"'
        indiceSingleQuote = maxsize
        if singleQuoteMarkup in objectJson:
            indiceSingleQuote = objectJson.index( singleQuoteMarkup )
        indiceDoubleQuote = maxsize
        if doubleQuoteMarkup in objectJson:
            indiceDoubleQuote = objectJson.index( doubleQuoteMarkup )
        if indiceSingleQuote < indiceDoubleQuote:
            convertedObjectJson = objectJson.replace( singleQuoteMarkup, doubleQuoteMarkup ).replace( "None", "null" )
        instantiatedObject = loads( convertedObjectJson, cls = ComplexJsonDecoder )
        # convert fields
        for convertionType, fieldsTupleFrozenset in convertingDict.items():
            for fieldsTuple in fieldsTupleFrozenset:
                ComplexJsonDecoder.recursiveConvertAttribut ( instantiatedObject, convertionType, fieldsTuple )
        # convert root iteration type
        if rootIterationType and isinstance( instantiatedObject, Iterable ):
            instantiatedObject = rootIterationType(instantiatedObject)
        # logger output
        logger.loadedLogger.output ( __name__ , ComplexJsonDecoder.__name__ ,
                                     ComplexJsonDecoder.loadComplexObject.__name__ , message = instantiatedObject )
        # return instantiated object
        return instantiatedObject
    @staticmethod
    def dict_to_object ( encodedJsonObject ) :
        # logger context
        argsStr = methodArgsStringRepresentation( signature( ComplexJsonDecoder.dict_to_object ).parameters, locals() )
        # logger input
        logger.loadedLogger.input ( ComplexJsonDecoder.__name__ ,
                                    ComplexJsonDecoder.dict_to_object.__name__ , message = argsStr )
        # by default, return the JSON encryption
        # INFO : do not remove, usefull for complete encoding/decoding
        instantiateObject = encodedJsonObject
        # decode fully if encryption markups are present
        if EncryptionMarkup.class_.value in encodedJsonObject and EncryptionMarkup.module.value in encodedJsonObject:
            # load class
            className = encodedJsonObject.pop( EncryptionMarkup.class_.value )
            moduleName = encodedJsonObject.pop( EncryptionMarkup.module.value )
            importedModule = import_module ( moduleName )
            loadedClass = getattr ( importedModule , className )
            # instanciate object
            instantiateObject = loadedClass( **encodedJsonObject )
        # logger output
        logger.loadedLogger.output ( ComplexJsonDecoder.__name__ ,
                                     ComplexJsonDecoder.dict_to_object.__name__ , message = instantiateObject )
        # return JSON encoding
        return instantiateObject
    # constructors
    def __init__(self):
        JSONDecoder.__init__( self, object_hook = self.dict_to_object )
