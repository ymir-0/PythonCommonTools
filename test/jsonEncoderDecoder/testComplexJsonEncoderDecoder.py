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
class simpleBoolean():
    # sample function
    def sampleFunction(self, externalBoolean):
        return self.sampleBoolean and externalBoolean
    # contructor
    def __init__(self, sampleBoolean=False):
        self.sampleBoolean=sampleBoolean
class simpleNumeric():
    # sample function
    def sampleFunction(self, externalNumeric):
        return self.sampleInt + self.sampleFloat + self.sampleComplex + externalNumeric
    # contructor
    def __init__(self, sampleInt=0, sampleFloat=0.0, sampleComplex=complex(0, 0)):
        self.sampleInt=sampleInt
        self.sampleFloat=sampleFloat
        self.sampleComplex=sampleComplex
class simpleSequence():
    # sample function
    def sampleFunction(self):
        return len(self.sampleList) + len(self.sampleTuple) + len(self.sampleRange)
    # contructor
    def __init__(self, sampleList=list(), sampleTuple=tuple(), sampleRange=range(0, 0)):
        self.sampleList=sampleList
        self.sampleTuple=sampleTuple
        self.sampleRange=sampleRange
# define test
#TODO: use the 'objectComparison' method defined in 'objectUtil' ?
#I do not use the 'objectComparison' method defined in 'objectUtil' module because it is not tested yet
class testComplexJsonEncoderDecoder(unittest.TestCase):
    # test simpe boolean
    def testSimpleBoolean(self):
        # create object
        testObject=simpleBoolean(True)
        # encode it
        testJson=ComplexJsonEncoder.dumpComplexObject(testObject)
        # decode it
        decodedObject=ComplexJsonDecoder.loadComplexObject(testJson)
        # check result
        self.assertEqual(type(simpleBoolean()),type(decodedObject),"types do not match")
        self.assertTrue(testObject.sampleBoolean,"attribute does not match")
        self.assertFalse(testObject.sampleFunction(False),"method does not match")
    # test simpe numeric
    def testSimpleNumeric(self):
        # create object
        sampleInt = 1
        sampleFloat = 2.3
        sampleComplex = complex(4, 5)
        testObject=simpleNumeric(sampleInt,sampleFloat,sampleComplex)
        # encode it
        testJson=ComplexJsonEncoder.dumpComplexObject(testObject)
        # decode it
        decodedObject=ComplexJsonDecoder.loadComplexObject(testJson)
        # check result
        self.assertEqual(type(simpleNumeric()),type(decodedObject),"types do not match")
        self.assertEqual(sampleInt,testObject.sampleInt,"attribute sampleInt does not match")
        self.assertEqual(sampleFloat,testObject.sampleFloat,"attribute sampleFloat does not match")
        self.assertEqual(sampleComplex,testObject.sampleComplex,"attribute sampleComplex does not match")
        externalNumeric=6
        expectedResult=sampleInt+sampleFloat+sampleComplex+externalNumeric
        self.assertEqual(expectedResult,testObject.sampleFunction(externalNumeric),"method does not match")
    # test simpe sequence
    def testSimpleSequence(self):
        # create object
        sampleList = [0,1.2]
        sampleTuple = (3,4.5)
        sampleRange = range(1,10)
        testObject=simpleSequence(sampleList,sampleTuple,sampleRange)
        # encode it
        testJson=ComplexJsonEncoder.dumpComplexObject(testObject)
        # decode it
        decodedObject=ComplexJsonDecoder.loadComplexObject(testJson)
        # check result
        self.assertEqual(type(simpleSequence()),type(decodedObject),"types do not match")
        self.assertEqual(sampleList,testObject.sampleList,"attribute sampleList does not match")
        self.assertEqual(sampleTuple,testObject.sampleTuple,"attribute sampleTuple does not match")
        self.assertEqual(sampleRange,testObject.sampleRange,"attribute sampleRange does not match")
        expectedResult=len(sampleList)+len(sampleTuple)+len(sampleRange)
        self.assertEqual(expectedResult,testObject.sampleFunction(),"method does not match")
    pass
# run test
if __name__ == '__main__':
    unittest.main()
