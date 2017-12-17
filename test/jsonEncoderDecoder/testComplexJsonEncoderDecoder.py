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
logger.loadLogger("MinstDataSetExtractor", CONFIGURATION_FILE)
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
        return self.sampleInt + self.sampleIn + self.sampleInt + externalNumeric
    # contructor
    def __init__(self, sampleInt=0, sampleFloat=0.0, sampleComplex=complex(0, 0)):
        self.sampleInt=sampleInt
        self.sampleFloat=sampleFloat
        self.sampleComplex=sampleComplex
# define test
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
    pass
# run test
if __name__ == '__main__':
    unittest.main()
