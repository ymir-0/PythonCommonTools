#!/usr/bin/env python3
# PY test script file name must start with "test" to allow automatic recognition by PyCharm
# import
import unittest
from os import sep
from os.path import join, realpath
from pythoncommontools.configurationLoader import configurationLoader
from pythoncommontools.logger import logger
from pythoncommontools.jsonEncoderDecoder.complexJsonEncoderDecoder import ComplexJsonEncoder,ComplexJsonDecoder
# contants
CURRENT_DIRECTORY = realpath(__file__).rsplit(sep, 1)[0]
CONFIGURATION_FILE=join(CURRENT_DIRECTORY,"..","..","pythoncommontools","conf","pythoncommontools.conf")
# load configuration
configurationLoader.loadConfiguration(CONFIGURATION_FILE)
logger.loadLogger("surrogate types", CONFIGURATION_FILE)
# create sample classes to encode/decode
class SampleBoolean():
    # sample function
    def sampleFunction(self, externalBoolean):
        return self.sampleBoolean and externalBoolean
    # contructor
    def __init__(self, sampleBoolean=False):
        self.sampleBoolean=sampleBoolean
class SampleNumeric():
    # sample function
    def sampleFunction(self, externalNumeric):
        return self.sampleInt + self.sampleFloat + self.sampleComplex + externalNumeric
    # contructor
    def __init__(self, sampleInt=0, sampleFloat=0.0, sampleComplex=complex(0, 0)):
        self.sampleInt=sampleInt
        self.sampleFloat=sampleFloat
        self.sampleComplex=sampleComplex
class SampleSequence():
    # sample function
    def sampleFunction(self):
        return len(self.sampleList) + len(self.sampleTuple) + len(self.sampleRange)
    # contructor
    def __init__(self, sampleList=list(), sampleTuple=tuple(), sampleRange=range(0, 0)):
        self.sampleList=sampleList
        self.sampleTuple=sampleTuple
        self.sampleRange=sampleRange
class SampleString():
    # sample function
    def sampleFunction(self):
        return len(self.sampleString)
    # contructor
    def __init__(self, sampleString=""):
        self.sampleString=sampleString
class SampleBinary():
    # sample function
    def sampleFunction(self):
        return len(self.sampleBytes) + len(self.sampleBytearray) + len(self.sampleMemoryview)
    # contructor
    def __init__(self, sampleBytes=bytes(), sampleBytearray=bytearray(), sampleMemoryview=memoryview(b'')):
        self.sampleBytes=sampleBytes
        self.sampleBytearray=sampleBytearray
        self.sampleMemoryview=sampleMemoryview
class SampleSet():
    # sample function
    def sampleFunction(self):
        return len(self.sampleSet) + len(self.sampleFrozenset)
    # contructor
    def __init__(self, sampleSet=set(), sampleFrozenset=frozenset()):
        self.sampleSet=sampleSet
        self.sampleFrozenset=sampleFrozenset
class SampleDictionnary():
    # sample function
    def sampleFunction(self):
        return len(self.sampleDictionnary)
    # contructor
    def __init__(self, sampleDictionnary=dict()):
        self.sampleDictionnary=sampleDictionnary
# define test
#TODO: use the 'objectComparison' method defined in 'objectUtil' ?
#I do not use the 'objectComparison' method defined in 'objectUtil' module because it is not tested yet
class testComplexJsonEncoderDecoder(unittest.TestCase):
    # test simpe boolean
    def testSampleBoolean(self):
        # create object
        testObject=SampleBoolean(True)
        # encode it
        testJson=ComplexJsonEncoder.dumpComplexObject(testObject)
        # decode it
        decodedObject=ComplexJsonDecoder.loadComplexObject(testJson)
        # check result
        self.assertEqual(SampleBoolean,type(decodedObject),"object types do not match")
        self.assertEqual(bool,type(decodedObject.sampleBoolean),"attribute type does not match")
        self.assertTrue(decodedObject.sampleBoolean,"attribute value does not match")
        self.assertFalse(decodedObject.sampleFunction(False),"method does not match")
    # test simpe numeric
    def testSampleNumeric(self):
        # create object
        sampleInt = 1
        sampleFloat = 2.3
        sampleComplex = complex(4, 5)
        testObject=SampleNumeric(sampleInt,sampleFloat,sampleComplex)
        # encode it
        testJson=ComplexJsonEncoder.dumpComplexObject(testObject)
        # decode it
        decodedObject=ComplexJsonDecoder.loadComplexObject(testJson)
        # check result
        self.assertEqual(SampleNumeric,type(decodedObject),"object types do not match")
        self.assertEqual(int,type(decodedObject.sampleInt),"attribute type sampleInt does not match")
        self.assertEqual(sampleInt,decodedObject.sampleInt,"attribute value sampleInt does not match")
        self.assertEqual(float,type(decodedObject.sampleFloat),"attribute type sampleFloat does not match")
        self.assertEqual(sampleFloat,decodedObject.sampleFloat,"attribute value sampleFloat does not match")
        self.assertEqual(complex,type(decodedObject.sampleComplex),"attribute type sampleComplex does not match")
        self.assertEqual(sampleComplex,decodedObject.sampleComplex,"attribute value sampleComplex does not match")
        externalNumeric=6
        expectedResult=sampleInt+sampleFloat+sampleComplex+externalNumeric
        self.assertEqual(expectedResult,decodedObject.sampleFunction(externalNumeric),"method does not match")
    # test simpe sequence
    def testSampleSequence(self):
        # create object
        # TODO: upgrade lists & set & map
        sampleList = [0,1.2]#complex(3,4)
        sampleTuple = (3,4.5)
        sampleRange = range(1,10)
        testObject=SampleSequence(sampleList,sampleTuple,sampleRange)
        # encode it
        testJson=ComplexJsonEncoder.dumpComplexObject(testObject)
        # decode it
        decodedObject=ComplexJsonDecoder.loadComplexObject(testJson)
        # check result
        self.assertEqual(SampleSequence,type(decodedObject),"object types do not match")
        self.assertEqual(list,type(decodedObject.sampleList),"attribute type sampleList does not match")
        self.assertEqual(sampleList,decodedObject.sampleList,"attribute value sampleList does not match")
        # TODO : after encode/decode, make tuple be tupla agin, not list
        self.assertEqual(list,type(decodedObject.sampleTuple),"attribute type sampleTuple does not match")
        self.assertEqual(list(sampleTuple),decodedObject.sampleTuple,"attribute value sampleTuple does not match")
        self.assertEqual(range,type(decodedObject.sampleRange),"attribute type sampleRange does not match")
        self.assertEqual(sampleRange,decodedObject.sampleRange,"attribute value sampleRange does not match")
        expectedResult=len(sampleList)+len(sampleTuple)+len(sampleRange)
        self.assertEqual(expectedResult,decodedObject.sampleFunction(),"method does not match")
    # test simpe string
    def testSampleString(self):
        # create object
        sampleString = "hello world!"
        testObject=SampleString(sampleString)
        # encode it
        testJson=ComplexJsonEncoder.dumpComplexObject(testObject)
        # decode it
        decodedObject=ComplexJsonDecoder.loadComplexObject(testJson)
        # check result
        self.assertEqual(SampleString,type(decodedObject),"object types do not match")
        self.assertEqual(str,type(decodedObject.sampleString),"attribute type does not match")
        self.assertEqual(sampleString,decodedObject.sampleString,"attribute value does not match")
        expectedResult=len(sampleString)
        self.assertEqual(expectedResult,decodedObject.sampleFunction(),"method does not match")
    # test simpe binary
    def testSampleBinary(self):
        # create object
        # TODO: upgrade lists & set & map
        sampleBytes = b'\xf0\xf1\xf2'
        sampleBytearray = bytearray.fromhex('2Ef0 F1f2  ')
        sampleMemoryview = memoryview(b'abcefg')
        testObject=SampleBinary(sampleBytes,sampleBytearray,sampleMemoryview)
        # encode it
        testJson=ComplexJsonEncoder.dumpComplexObject(testObject)
        # decode it
        decodedObject=ComplexJsonDecoder.loadComplexObject(testJson)
        # check result
        self.assertEqual(SampleBinary,type(decodedObject),"object types do not match")
        self.assertEqual(bytes,type(decodedObject.sampleBytes),"attribute type sampleBytes does not match")
        self.assertEqual(sampleBytes,decodedObject.sampleBytes,"attribute value sampleBytes does not match")
        self.assertEqual(bytearray,type(decodedObject.sampleBytearray),"attribute type sampleBytearray does not match")
        self.assertEqual(sampleBytearray,decodedObject.sampleBytearray,"attribute value sampleBytearray does not match")
        self.assertEqual(memoryview,type(decodedObject.sampleMemoryview),"attribute type sampleMemoryview does not match")
        self.assertEqual(sampleMemoryview,decodedObject.sampleMemoryview,"attribute value sampleMemoryview does not match")
        expectedResult=len(sampleBytes)+len(sampleBytearray)+len(sampleMemoryview)
        self.assertEqual(expectedResult,decodedObject.sampleFunction(),"method does not match")
    # test simpe set
    def testSampleSet(self):
        # create object
        # TODO: upgrade lists & set
        sampleSet = set((0,1.2))
        sampleFrozenset = frozenset((3,4.5))
        testObject=SampleSet(sampleSet,sampleFrozenset)
        # encode it
        testJson=ComplexJsonEncoder.dumpComplexObject(testObject)
        # decode it
        decodedObject=ComplexJsonDecoder.loadComplexObject(testJson)
        # check result
        self.assertEqual(SampleSet,type(decodedObject),"object types do not match")
        self.assertEqual(set,type(decodedObject.sampleSet),"attribute type sampleSet does not match")
        self.assertEqual(sampleSet,decodedObject.sampleSet,"attribute value sampleSet does not match")
        self.assertEqual(frozenset,type(decodedObject.sampleFrozenset),"attribute type sampleFrozenset does not match")
        self.assertEqual(sampleFrozenset,decodedObject.sampleFrozenset,"attribute value sampleFrozenset does not match")
        expectedResult=len(sampleSet)+len(sampleFrozenset)
        self.assertEqual(expectedResult,decodedObject.sampleFunction(),"method does not match")
    # test simpe dictionnary
    def testSampleDictionnary(self):
        # create object
        # TODO: upgrade lists & set & map
        sampleDictionnary = {'one': 1, 'two': 2, 'three': 3}
        testObject=SampleDictionnary(sampleDictionnary)
        # encode it
        testJson=ComplexJsonEncoder.dumpComplexObject(testObject)
        # decode it
        decodedObject=ComplexJsonDecoder.loadComplexObject(testJson)
        # check result
        self.assertEqual(SampleDictionnary,type(decodedObject),"object types do not match")
        self.assertEqual(dict,type(decodedObject.sampleDictionnary),"attribute type does not match")
        self.assertEqual(sampleDictionnary,decodedObject.sampleDictionnary,"attribute value does not match")
        expectedResult=len(sampleDictionnary)
        self.assertEqual(expectedResult,decodedObject.sampleFunction(),"method does not match")
    pass
# run test
if __name__ == '__main__':
    unittest.main()
