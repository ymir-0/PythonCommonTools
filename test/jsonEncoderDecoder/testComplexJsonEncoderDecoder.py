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
        self.assertEqual(bool,type(testObject.sampleBoolean),"attribute type does not match")
        self.assertTrue(testObject.sampleBoolean,"attribute value does not match")
        self.assertFalse(testObject.sampleFunction(False),"method does not match")
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
        self.assertEqual(sampleInt,testObject.sampleInt,"attribute value sampleInt does not match")
        self.assertEqual(sampleFloat,testObject.sampleFloat,"attribute value sampleFloat does not match")
        self.assertEqual(sampleComplex,testObject.sampleComplex,"attribute value sampleComplex does not match")
        externalNumeric=6
        expectedResult=sampleInt+sampleFloat+sampleComplex+externalNumeric
        self.assertEqual(expectedResult,testObject.sampleFunction(externalNumeric),"method does not match")
    # test simpe sequence
    def testSampleSequence(self):
        # create object
        # TODO: upgrade lists & set & map
        sampleList = [0,1.2]
        sampleTuple = (3,4.5)
        sampleRange = range(1,10)
        testObject=SampleSequence(sampleList,sampleTuple,sampleRange)
        # encode it
        testJson=ComplexJsonEncoder.dumpComplexObject(testObject)
        # decode it
        decodedObject=ComplexJsonDecoder.loadComplexObject(testJson)
        # check result
        self.assertEqual(SampleSequence,type(decodedObject),"object types do not match")
        self.assertEqual(sampleList,testObject.sampleList,"attribute value sampleList does not match")
        self.assertEqual(sampleTuple,testObject.sampleTuple,"attribute value sampleTuple does not match")
        self.assertEqual(sampleRange,testObject.sampleRange,"attribute value sampleRange does not match")
        expectedResult=len(sampleList)+len(sampleTuple)+len(sampleRange)
        self.assertEqual(expectedResult,testObject.sampleFunction(),"method does not match")
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
        self.assertEqual(str,type(testObject.sampleString),"attribute type does not match")
        self.assertEqual(sampleString,testObject.sampleString,"attribute value does not match")
        expectedResult=len(sampleString)
        self.assertEqual(expectedResult,testObject.sampleFunction(),"method does not match")
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
        self.assertEqual(sampleBytes,testObject.sampleBytes,"attribute value sampleBytes does not match")
        self.assertEqual(sampleBytearray,testObject.sampleBytearray,"attribute value sampleBytearray does not match")
        self.assertEqual(sampleMemoryview,testObject.sampleMemoryview,"attribute value sampleMemoryview does not match")
        expectedResult=len(sampleBytes)+len(sampleBytearray)+len(sampleMemoryview)
        self.assertEqual(expectedResult,testObject.sampleFunction(),"method does not match")
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
        self.assertEqual(sampleSet,testObject.sampleSet,"attribute value sampleBytes does not match")
        self.assertEqual(sampleFrozenset,testObject.sampleFrozenset,"attribute value sampleBytearray does not match")
        expectedResult=len(sampleSet)+len(sampleFrozenset)
        self.assertEqual(expectedResult,testObject.sampleFunction(),"method does not match")
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
        self.assertEqual(dict,type(testObject.sampleDictionnary),"attribute type does not match")
        self.assertEqual(sampleDictionnary,testObject.sampleDictionnary,"attribute value does not match")
        expectedResult=len(sampleDictionnary)
        self.assertEqual(expectedResult,testObject.sampleFunction(),"method does not match")
    pass
# run test
if __name__ == '__main__':
    unittest.main()
