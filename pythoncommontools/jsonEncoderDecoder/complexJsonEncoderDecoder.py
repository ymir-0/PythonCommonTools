# coding=utf-8
# @see : https://pymotw.com/2/json/ (it is for python 2, but it is adaptable for python 3)
# imports
from collections import Iterable
from copy import deepcopy, copy
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
    CLASS = "className"
    MODULE = "moduleName"
    SURROGATE_TYPE = "surrogateType"
    @staticmethod
    def listValues():
        values=list()
        for encryptionMarkup in EncryptionMarkup: values.append(encryptionMarkup.value)
        return tuple(values)
# serializable surrogate types
#TODO: use a super class for all surrogate types ?
class ComplexeSurrogate():
    @staticmethod
    def convertToFinalObject(dictObject):
        # update the attributes
        surrogateObject=ComplexeSurrogate()
        surrogateObject.__dict__.update(dictObject)
        # convert to final type
        finalObject=complex(surrogateObject.real,surrogateObject.imaginary)
        return finalObject
    def __init__(self,originalObject=complex(0,0)):
        setattr(self, EncryptionMarkup.SURROGATE_TYPE.value, ComplexeSurrogate.__name__)
        self.real=originalObject.real
        self.imaginary=originalObject.imag
class RangeSurrogate():
    @staticmethod
    def convertToFinalObject(dictObject):
        # update the attributes
        surrogateObject=RangeSurrogate()
        surrogateObject.__dict__.update(dictObject)
        # convert to final type
        finalObject=range(surrogateObject.start,surrogateObject.end)
        return finalObject
    def __init__(self,originalObject=range(0,1)):
        setattr(self, EncryptionMarkup.SURROGATE_TYPE.value, RangeSurrogate.__name__)
        self.start=originalObject[0]
        self.end=originalObject[-1]+1 # WARNING : range end is exclusive
class BytesSurrogate():
    @staticmethod
    def convertToFinalObject(dictObject):
        # update the attributes
        surrogateObject=BytesSurrogate()
        surrogateObject.__dict__.update(dictObject)
        # convert to final type
        finalObject=bytes(surrogateObject.integers)
        return finalObject
    def __init__(self,originalObject=bytes()):
        setattr(self, EncryptionMarkup.SURROGATE_TYPE.value, BytesSurrogate.__name__)
        self.integers=list(originalObject)
class BytearraySurrogate():
    @staticmethod
    def convertToFinalObject(dictObject):
        # update the attributes
        surrogateObject=BytearraySurrogate()
        surrogateObject.__dict__.update(dictObject)
        # convert to final type
        finalObject=bytearray(surrogateObject.integers)
        return finalObject
    def __init__(self,originalObject=bytearray()):
        setattr(self, EncryptionMarkup.SURROGATE_TYPE.value, BytearraySurrogate.__name__)
        self.integers=list(originalObject)
class MemoryviewSurrogate():
    @staticmethod
    def convertToFinalObject(dictObject):
        # update the attributes
        surrogateObject=MemoryviewSurrogate()
        surrogateObject.__dict__.update(dictObject)
        # convert to final type
        # WARNING : memory view requires bytes as input
        finalObject=memoryview(bytes(surrogateObject.integers))
        return finalObject
    def __init__(self,originalObject=memoryview(b'')):
        setattr(self, EncryptionMarkup.SURROGATE_TYPE.value, MemoryviewSurrogate.__name__)
        self.integers=list(originalObject)
class SetSurrogate():
    @staticmethod
    def convertToFinalObject(jsonEncryption):
        # load it in a dictionnary
        dictObject = loads(jsonEncryption)
        # update the attributes
        surrogateObject=SetSurrogate()
        surrogateObject.__dict__.update(dictObject)
        # convert to final type
        # WARNING : memory view requires bytes as input
        finalObject=set(surrogateObject.list)
        return finalObject
    def __init__(self,originalObject=set()):
        setattr(self, EncryptionMarkup.SURROGATE_TYPE.value, SetSurrogate.__name__)
        self.list=list(originalObject)
class FrozensetSurrogate():
    @staticmethod
    def convertToFinalObject(jsonEncryption):
        # load it in a dictionnary
        dictObject = loads(jsonEncryption)
        # update the attributes
        surrogateObject=FrozensetSurrogate()
        surrogateObject.__dict__.update(dictObject)
        # convert to final type
        # WARNING : memory view requires bytes as input
        finalObject=frozenset(surrogateObject.list)
        return finalObject
    def __init__(self,originalObject=set()):
        setattr(self, EncryptionMarkup.SURROGATE_TYPE.value, FrozensetSurrogate.__name__)
        self.list=list(originalObject)
UNSERIALIZABLE_TYPES={
    complex:ComplexeSurrogate,
    range:RangeSurrogate,
    bytes:BytesSurrogate,
    bytearray:BytearraySurrogate,
    memoryview:MemoryviewSurrogate,
    set:SetSurrogate,
    frozenset:FrozensetSurrogate
}
#TODO: remove class & static methos for encode / decode
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
        # WARNING : can not (deep) copy a 'memory view'
        if type(rawObject)==memoryview:
            ugradedObject = memoryview(rawObject)
        else:
            ugradedObject = copy(rawObject)
        # encode JSON primitive object
        if type(rawObject) in (bool,int,float,str):
            jsonObject = ComplexJsonEncoder.dumpJsonPrimitiveObject(rawObject)
        # encode unserializable primitive object
        elif type(rawObject) in UNSERIALIZABLE_TYPES.keys():
            jsonObject = ComplexJsonEncoder.dumpUnserializablePrimitiveObject(rawObject)
        # encode iterable object
        elif type(rawObject) in (list,tuple):
            jsonObject = ComplexJsonEncoder.dumpIterableObject(rawObject)
        # encode complex object
        else:
            # encode all attributes
            for attributeName, attributeValue in ugradedObject.__dict__.items():
                jsonAttributValue=ComplexJsonEncoder.dumpComplexObject(attributeValue)
                setattr(ugradedObject, attributeName, jsonAttributValue)
                pass
            # add module & class references
            setattr(ugradedObject, EncryptionMarkup.CLASS.value, rawObject.__class__.__name__)
            setattr(ugradedObject, EncryptionMarkup.MODULE.value, rawObject.__module__)
            # encode object
            jsonObject = dumps(ugradedObject.__dict__)
            pass
        # logger output
        logger.loadedLogger.output ( __name__ , ComplexJsonEncoder.__name__ ,ComplexJsonEncoder.dumpComplexObject.__name__ , message = jsonObject )
        # return
        return jsonObject
    @staticmethod
    def dumpJsonPrimitiveObject ( rawObject ):
        # logger context
        argsStr = methodArgsStringRepresentation( signature( ComplexJsonEncoder.dumpJsonPrimitiveObject ).parameters,locals() )
        # logger input
        logger.loadedLogger.input ( __name__ , ComplexJsonEncoder.__name__ ,ComplexJsonEncoder.dumpJsonPrimitiveObject.__name__ , message = argsStr )
        # encode identical
        jsonObject = rawObject
        # logger output
        logger.loadedLogger.output ( __name__ , ComplexJsonEncoder.__name__ ,ComplexJsonEncoder.dumpJsonPrimitiveObject.__name__ , message = jsonObject )
        # return
        return jsonObject
    @staticmethod
    def dumpUnserializablePrimitiveObject ( rawObject ):
        # logger context
        argsStr = methodArgsStringRepresentation( signature( ComplexJsonEncoder.dumpUnserializablePrimitiveObject ).parameters,locals() )
        # logger input
        logger.loadedLogger.input ( __name__ , ComplexJsonEncoder.__name__ ,ComplexJsonEncoder.dumpUnserializablePrimitiveObject.__name__ , message = argsStr )
        # encode with surrogate
        rawObjectType = type(rawObject)
        surrogateClass = UNSERIALIZABLE_TYPES[rawObjectType]
        surrogateValue = surrogateClass(rawObject)
        jsonObject = dumps(surrogateValue.__dict__)
        # logger output
        logger.loadedLogger.output ( __name__ , ComplexJsonEncoder.__name__ ,ComplexJsonEncoder.dumpUnserializablePrimitiveObject.__name__ , message = jsonObject )
        # return
        return jsonObject
    @staticmethod
    def dumpIterableObject ( rawObject ):
        # logger context
        argsStr = methodArgsStringRepresentation( signature( ComplexJsonEncoder.dumpIterableObject ).parameters,locals() )
        # logger input
        logger.loadedLogger.input ( __name__ , ComplexJsonEncoder.__name__ ,ComplexJsonEncoder.dumpIterableObject.__name__ , message = argsStr )
        # initialize encoded attributs
        jsonObject = list()
        # execute recursive encryption
        for rawAttributElement in rawObject:
            encodedAttributElement = ComplexJsonEncoder.dumpComplexObject(rawAttributElement)
            jsonObject.append(encodedAttributElement)
        # logger output
        logger.loadedLogger.output ( __name__ , ComplexJsonEncoder.__name__ ,ComplexJsonEncoder.dumpIterableObject.__name__ , message = jsonObject )
        # return
        return jsonObject
    pass
# decode from JSON to objects
class ComplexJsonDecoder(  ):
    @staticmethod
    def loadComplexObject ( jsonObject):
        # logger context
        argsStr = methodArgsStringRepresentation( signature( ComplexJsonDecoder.loadComplexObject ).parameters, locals() )
        # logger input
        logger.loadedLogger.input ( __name__ , ComplexJsonDecoder.__name__ ,ComplexJsonDecoder.loadComplexObject.__name__ , message = argsStr )
        # type of JSON object
        jsonObjectType=type(jsonObject)
        # filter the kind of string : primitive or complexe
        stringComplexeFilterage=frozenset([encryptionMarkup in str(jsonObject) for encryptionMarkup in EncryptionMarkup.listValues()])
        # decode JSON primitive object
        if jsonObjectType in (bool,int,float) or (jsonObjectType==str and True not in stringComplexeFilterage):
            instantiatedObject = ComplexJsonDecoder.loadJsonPrimitiveObject(jsonObject)
        # decode iterable object
        elif jsonObjectType in (list,tuple):
            instantiatedObject = ComplexJsonDecoder.loadIterableObject(jsonObject)
        # decode complex object
        else:
            dictObject=loads(jsonObject)
            # decode unserializable primitive object
            if EncryptionMarkup.SURROGATE_TYPE.value in dictObject:
                instantiatedObject = ComplexJsonDecoder.loadUnserializablePrimitiveObject(dictObject)
            # decode real object
            else:
                # instanciate object
                instantiationClass=loadClass(dictObject[EncryptionMarkup.MODULE.value], dictObject[EncryptionMarkup.CLASS.value])
                instantiatedObject=instantiationClass()
                # remove markups
                del dictObject[EncryptionMarkup.MODULE.value]
                del dictObject[EncryptionMarkup.CLASS.value]
                # instanciate all attributes recursively
                for attributeName, attributeValue in dictObject.items():
                    instantiatedAttributValue = ComplexJsonDecoder.loadComplexObject(attributeValue)
                    setattr(instantiatedObject, attributeName, instantiatedAttributValue)
                pass
        # logger output
        logger.loadedLogger.output ( __name__ , ComplexJsonDecoder.__name__ ,ComplexJsonDecoder.loadComplexObject.__name__ , message = instantiatedObject )
        # return instantiated object
        return instantiatedObject
    @staticmethod
    def loadJsonPrimitiveObject ( jsonObject ):
        # logger context
        argsStr = methodArgsStringRepresentation( signature( ComplexJsonEncoder.dumpJsonPrimitiveObject ).parameters,locals() )
        # logger input
        logger.loadedLogger.input ( __name__ , ComplexJsonEncoder.__name__ ,ComplexJsonEncoder.dumpJsonPrimitiveObject.__name__ , message = argsStr )
        # decode identical
        instantiatedObject = jsonObject
        # logger output
        logger.loadedLogger.output ( __name__ , ComplexJsonEncoder.__name__ ,ComplexJsonEncoder.dumpJsonPrimitiveObject.__name__ , message = instantiatedObject )
        # return
        return instantiatedObject
    @staticmethod
    def loadUnserializablePrimitiveObject ( dictObject ):
        # logger context
        argsStr = methodArgsStringRepresentation( signature( ComplexJsonEncoder.dumpUnserializablePrimitiveObject ).parameters,locals() )
        # logger input
        logger.loadedLogger.input ( __name__ , ComplexJsonEncoder.__name__ ,ComplexJsonEncoder.dumpUnserializablePrimitiveObject.__name__ , message = argsStr )
        # load class
        instantiationClass = loadClass(__name__,dictObject[EncryptionMarkup.SURROGATE_TYPE.value])
        # decode with surrogate
        instantiatedObject=instantiationClass.convertToFinalObject(dictObject)
        # logger output
        logger.loadedLogger.output ( __name__ , ComplexJsonEncoder.__name__ ,ComplexJsonEncoder.dumpUnserializablePrimitiveObject.__name__ , message = instantiatedObject )
        # return
        return instantiatedObject
    @staticmethod
    def loadIterableObject ( jsonObject ):
        # logger context
        argsStr = methodArgsStringRepresentation( signature( ComplexJsonEncoder.dumpIterableObject ).parameters,locals() )
        # logger input
        logger.loadedLogger.input ( __name__ , ComplexJsonEncoder.__name__ ,ComplexJsonEncoder.dumpIterableObject.__name__ , message = argsStr )
        # initialize decode attributs
        instantiatedObject = list()
        # execute recursive decode
        for rawAttributElement in jsonObject:
            encodedAttributElement = ComplexJsonDecoder.loadComplexObject(rawAttributElement)
            instantiatedObject.append(encodedAttributElement)
        # logger output
        logger.loadedLogger.output ( __name__ , ComplexJsonEncoder.__name__ ,ComplexJsonEncoder.dumpIterableObject.__name__ , message = instantiatedObject )
        # return
        return instantiatedObject
    pass
    pass
def loadClass(moduleName,className):
    # logger context
    argsStr = methodArgsStringRepresentation(signature(loadClass).parameters, locals())
    # logger input
    logger.loadedLogger.input(__name__, functionOrmethod=loadClass.__name__, message=argsStr)
    # load class
    importedModule = import_module(moduleName)
    loadedClass = getattr(importedModule, className)
    # logger output
    logger.loadedLogger.output(__name__, functionOrmethod=loadClass.__name__,message=loadedClass)
    # return
    return loadedClass
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
