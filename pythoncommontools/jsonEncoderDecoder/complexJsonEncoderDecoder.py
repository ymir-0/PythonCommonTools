# coding=utf-8
# @see : https://pymotw.com/2/json/ (it is for python 2, but it is adaptable for python 3)
# imports
from abc import ABC, abstractmethod
from copy import  copy
from enum import Enum , unique
from importlib import import_module
from json import dumps , loads
from uuid import uuid4
# encryption markup
NONE="null"
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
class AbstractSurrogate(ABC):
    @abstractmethod
    def convertToFinalObject(self):
        pass
class ComplexeSurrogate(AbstractSurrogate):
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
class RangeSurrogate(AbstractSurrogate):
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
        self.end=originalObject[-1]+1 # INFO : range end is exclusive
class BytesSurrogate(AbstractSurrogate):
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
class BytearraySurrogate(AbstractSurrogate):
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
class MemoryviewSurrogate(AbstractSurrogate):
    @staticmethod
    def convertToFinalObject(dictObject):
        # update the attributes
        surrogateObject=MemoryviewSurrogate()
        surrogateObject.__dict__.update(dictObject)
        # convert to final type
        # INFO : memory view requires bytes as input
        finalObject=memoryview(bytes(surrogateObject.integers))
        return finalObject
    def __init__(self,originalObject=memoryview(b'')):
        setattr(self, EncryptionMarkup.SURROGATE_TYPE.value, MemoryviewSurrogate.__name__)
        self.integers=list(originalObject)
class SetSurrogate(AbstractSurrogate):
    @staticmethod
    def convertToFinalObject(dictObject):
        # update the attributes
        surrogateObject=SetSurrogate()
        surrogateObject.__dict__.update(dictObject)
        # convert to final type
        finalObject=set(surrogateObject.list)
        return finalObject
    def __init__(self,originalObject=set()):
        setattr(self, EncryptionMarkup.SURROGATE_TYPE.value, SetSurrogate.__name__)
        self.list=list(originalObject)
class FrozensetSurrogate(AbstractSurrogate):
    @staticmethod
    def convertToFinalObject(dictObject):
        # update the attributes
        surrogateObject=FrozensetSurrogate()
        surrogateObject.__dict__.update(dictObject)
        # convert to final type
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
#INFO: tuple is serializable by default, but it becomes a list
class TupleSurrogate(AbstractSurrogate):
    @staticmethod
    def convertToFinalObject(dictObject):
        # update the attributes
        surrogateObject=TupleSurrogate()
        surrogateObject.__dict__.update(dictObject)
        # convert to final type
        finalObject=frozenset(surrogateObject.list)
        return finalObject
    def __init__(self,originalObject=tuple()):
        setattr(self, EncryptionMarkup.SURROGATE_TYPE.value, TupleSurrogate.__name__)
        self.list=list(originalObject)
# encode from objects to JSON
class ComplexJsonEncoder(  ):
    # methods
    @staticmethod
    def dumpComplexObject ( rawObject ):
        # encode None object
        if rawObject is None:
            jsonObject = ComplexJsonEncoder.dumpNoneObject()
        # encode JSON primitive object
        elif type(rawObject) in (bool,int,float,str):
            jsonObject = ComplexJsonEncoder.dumpJsonPrimitiveObject(rawObject)
        # encode unserializable primitive object
        elif type(rawObject) in UNSERIALIZABLE_TYPES.keys():
            jsonObject = ComplexJsonEncoder.dumpUnserializablePrimitiveObject(rawObject)
        # encode iterable object
        elif type(rawObject) in (list,tuple):
            jsonObject = ComplexJsonEncoder.dumpIterableObject(rawObject)
        # encode dictionnary object
        elif type(rawObject)==dict:
            jsonObject = ComplexJsonEncoder.dumpDictionnaryObject(rawObject)
        # encode standard object
        else:
            jsonObject = ComplexJsonEncoder.dumpStandardObject(rawObject)
        # return
        return jsonObject
    @staticmethod
    def dumpNoneObject (  ):
        # encode identical
        jsonObject = NONE
        # return
        return jsonObject
    @staticmethod
    def dumpJsonPrimitiveObject ( rawObject ):
        # encode identical
        jsonObject = rawObject
        # return
        return jsonObject
    @staticmethod
    def dumpUnserializablePrimitiveObject ( rawObject ):
        # encode with surrogate
        rawObjectType = type(rawObject)
        surrogateClass = UNSERIALIZABLE_TYPES[rawObjectType]
        surrogateValue = surrogateClass(rawObject)
        # (frozen)set is iterable
        if surrogateClass in (SetSurrogate,FrozensetSurrogate):
            surrogateValue.list=ComplexJsonEncoder.dumpIterableObject(surrogateValue.list)
        # encode object
        jsonObject = dumps(surrogateValue.__dict__)
        # return
        return jsonObject
    @staticmethod
    def dumpIterableObject ( rawObject ):
        # initialize encoded attributs
        jsonObject = list()
        # execute recursive encryption
        for rawAttributElement in rawObject:
            encodedAttributElement = ComplexJsonEncoder.dumpComplexObject(rawAttributElement)
            jsonObject.append(encodedAttributElement)
        # encode tuple with surrogate
        if type(rawObject)==tuple:
            surrogateTuple=TupleSurrogate(jsonObject)
            jsonObject = dumps(surrogateTuple.__dict__)
        # return
        return jsonObject
    @staticmethod
    def dumpDictionnaryObject ( rawObject ):
        # initialize encoded attributs
        jsonObject = dict()
        # execute recursive encryption
        for rawAttributKey,rawAttributValue in rawObject.items():
            # INFO: in JSON, keys are always string when it can be everything in python
            jsonKey=str(uuid4())
            encodedAttributKey = ComplexJsonEncoder.dumpComplexObject(rawAttributKey)
            encodedAttributValue = ComplexJsonEncoder.dumpComplexObject(rawAttributValue)
            jsonObject[jsonKey]=[encodedAttributKey,encodedAttributValue]
        # return
        return jsonObject
    @staticmethod
    def dumpStandardObject ( rawObject ):
        # encode standard object
        ugradedObject = copy(rawObject)
        for attributeName, attributeValue in ugradedObject.__dict__.items():
            jsonAttributValue = ComplexJsonEncoder.dumpComplexObject(attributeValue)
            setattr(ugradedObject, attributeName, jsonAttributValue)
            pass
        # add module & class references
        setattr(ugradedObject, EncryptionMarkup.CLASS.value, rawObject.__class__.__name__)
        setattr(ugradedObject, EncryptionMarkup.MODULE.value, rawObject.__module__)
        # encode object
        jsonObject = dumps(ugradedObject.__dict__)
        # return
        return jsonObject
    pass
# decode from JSON to objects
class ComplexJsonDecoder(  ):
    @staticmethod
    def loadComplexObject ( jsonObject):
        # type of JSON object
        jsonObjectType=type(jsonObject)
        # filter the kind of string : primitive or complexe
        stringComplexeFilterage=frozenset([encryptionMarkup in str(jsonObject) for encryptionMarkup in EncryptionMarkup.listValues()])
        # decode None object
        if jsonObject==NONE:
            instantiatedObject = ComplexJsonDecoder.loadNoneObject()
        # decode JSON primitive object
        elif jsonObjectType in (bool,int,float) or (jsonObjectType==str and True not in stringComplexeFilterage):
            instantiatedObject = ComplexJsonDecoder.loadJsonPrimitiveObject(jsonObject)
        # decode iterable object
        elif jsonObjectType == list:
            instantiatedObject = ComplexJsonDecoder.loadIterableObject(jsonObject)
        # decode dictionnary object
        elif jsonObjectType==dict:
            instantiatedObject = ComplexJsonDecoder.loadDictionaryObject(jsonObject)
        # decode standard or 'unserializable primitive' object
        else:
            dictObject=loads(jsonObject)
            # decode unserializable primitive object
            if EncryptionMarkup.SURROGATE_TYPE.value in dictObject:
                instantiatedObject = ComplexJsonDecoder.loadUnserializablePrimitiveObject(dictObject)
            # decode standard object
            else:
                instantiatedObject = ComplexJsonDecoder.loadStandardObject(dictObject)
        # return
        return instantiatedObject
    @staticmethod
    def loadNoneObject (  ):
        # encode identical
        instantiatedObject = None
        # return
        return instantiatedObject
    @staticmethod
    def loadJsonPrimitiveObject ( jsonObject ):
        # decode identical
        instantiatedObject = jsonObject
        # return
        return instantiatedObject
    @staticmethod
    def loadUnserializablePrimitiveObject ( dictObject ):
        # load class
        instantiationClass = ComplexJsonDecoder.loadClass(__name__,dictObject[EncryptionMarkup.SURROGATE_TYPE.value])
        # decode with surrogate
        instantiatedObject=instantiationClass.convertToFinalObject(dictObject)
        # (frozen)set and tuple are iterable
        if instantiationClass in (SetSurrogate,FrozensetSurrogate,TupleSurrogate):
            instantiatedObject=ComplexJsonDecoder.loadIterableObject(instantiatedObject)
            if instantiationClass==SetSurrogate:
                instantiatedObject=set(instantiatedObject)
            elif instantiationClass==FrozensetSurrogate:
                instantiatedObject = frozenset(instantiatedObject)
            else :
                instantiatedObject = tuple(instantiatedObject)
        # return
        return instantiatedObject
    @staticmethod
    def loadIterableObject ( jsonObject ):
        # initialize decode attributs
        instantiatedObject = list()
        # execute recursive decode
        for rawAttributElement in jsonObject:
            instantiatedAttributElement = ComplexJsonDecoder.loadComplexObject(rawAttributElement)
            instantiatedObject.append(instantiatedAttributElement)
        # return
        return instantiatedObject
    @staticmethod
    def loadDictionaryObject ( rawObject ):
        # initialize encoded attributs
        instantiatedObject = dict()
        # execute recursive encryption
        for rawAttributKey,rawAttributValue in rawObject.items():
            instantiatedAttributPair = ComplexJsonDecoder.loadComplexObject(rawAttributValue)
            instantiatedAttributKey=instantiatedAttributPair[0]
            instantiatedAttributValue=instantiatedAttributPair[1]
            instantiatedObject[instantiatedAttributKey]=instantiatedAttributValue
        # return
        return instantiatedObject
    @staticmethod
    def loadStandardObject ( dictObject ):
        # instanciate object
        instantiationClass = ComplexJsonDecoder.loadClass(dictObject[EncryptionMarkup.MODULE.value],dictObject[EncryptionMarkup.CLASS.value])
        instantiatedObject = instantiationClass()
        # remove markups
        del dictObject[EncryptionMarkup.MODULE.value]
        del dictObject[EncryptionMarkup.CLASS.value]
        # instanciate all attributes recursively
        for attributeName, attributeValue in dictObject.items():
            instantiatedAttributValue = ComplexJsonDecoder.loadComplexObject(attributeValue)
            setattr(instantiatedObject, attributeName, instantiatedAttributValue)
        pass
        # return
        return instantiatedObject
    @staticmethod
    def loadClass(moduleName,className):
        # load class
        importedModule = import_module(moduleName)
        loadedClass = getattr(importedModule, className)
        # return
        return loadedClass
