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
        innerSampleSet = set((True,7,4.8,complex(1,5),b'\x1a\x2b\x3c',memoryview(b'mplokij')))
        innerSampleFrozenset = frozenset((True,9,2.6,complex(3,0),b'\x4d\x5e\x6f',memoryview(b'wqaxszcd')))
        innerList = [False,5,6.7,complex(8,9),b'\x0f\x1f\x2f',bytearray(b'\x3e\x4e\x5e'),memoryview(b'azerty'),
                     innerSampleSet,innerSampleFrozenset]
        sampleSet = set((True,3,2.6,complex(1,5),b'\xa1\xb2\xc3',memoryview(b'poiuytr'),innerSampleFrozenset))
        sampleFrozenset = frozenset((True,9,4.8,complex(7,0),b'\xd4\xe5\xf6',memoryview(b'mlkjhgf'),innerSampleFrozenset))
        sampleList = [True,0,1.2,complex(3,4),b'\xf0\xf1\xf2',bytearray(b'\xe3\xe4\xe5'),memoryview(b'abcefg'),
                      innerList,sampleSet,sampleFrozenset]
        #TODO: test inner tuple
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
        sampleBytearray = bytearray(b'\xe3\xe4\xe5')
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
        # INFO : some object are not hashable, so can not be in a (frozen)set : bytearray, list, set
        # TODO: upgrade lists & set
        innerFrozenset = frozenset((True,3,2.6,complex(1,9),b'\x3e\x4e\x5e',memoryview(b'wqazsxc')))
        sampleSet = set((True,0,1.2,complex(3,4),b'\xf0\xf1\xf2',memoryview(b'abcefg'),innerFrozenset))
        sampleFrozenset = frozenset((True,9,8.7,complex(6,5),b'\xe3\xe4\xe5',memoryview(b'azerty'),innerFrozenset))
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
        innerSampleSet = set((True,7,4.8,complex(1,5),b'\x1a\x2b\x3c',memoryview(b'mplokij')))
        innerSampleFrozenset = frozenset((True,9,2.6,complex(3,0),b'\x4d\x5e\x6f',memoryview(b'wqaxszcd')))
        innerList = [False,5,6.7,complex(8,9),b'\x0f\x1f\x2f',bytearray(b'\x3e\x4e\x5e'),memoryview(b'azerty'),
                     innerSampleSet,innerSampleFrozenset]
        sampleSet = set((True,3,2.6,complex(1,5),b'\xa1\xb2\xc3',memoryview(b'poiuytr')))
        sampleFrozenset = frozenset((True,9,4.8,complex(7,0),b'\xd4\xe5\xf6',memoryview(b'mlkjhgf')))
        sampleList = [True,0,1.2,complex(3,4),b'\xf0\xf1\xf2',bytearray(b'\xe3\xe4\xe5'),memoryview(b'abcefg'),
                      innerList,sampleSet,sampleFrozenset]
        # INFO : some object are not hashable, so can not be in dictionnary key : bytearray, list, set
        innerDictionnary = {
            False:True,
            'a': 9,
            'b': 8.7,
            'c': complex(6,5),
            'd': "azerty",
            'e': b'\xf0\xf1\xf2',
            'f': bytearray(b'\xe3\xe4\xe5'),
            'g': memoryview(b'abcefg'),
            'h': innerList,
            #'i': (3,4.5),
            0: 9,
            1: 8.7,
            2: complex(6, 5),
            3: "azerty",
            4: b'\xf0\xf1\xf2',
            5: bytearray(b'\xe3\xe4\xe5'),
            6: memoryview(b'abcefg'),
            7: innerList,
            # 8: (3,4.5),
            10.: 9,
            9.1: 8.7,
            8.2: complex(6, 5),
            7.3: "azerty",
            6.4: b'\xf0\xf1\xf2',
            5.5: bytearray(b'\xe3\xe4\xe5'),
            4.6: memoryview(b'abcefg'),
            3.7: innerList,
            # 8: (3,4.5),
            complex(1,0): 9,
            complex(9,1): 8.7,
            complex(8,2): complex(6, 5),
            complex(7,3): "azerty",
            complex(6,4): b'\xf0\xf1\xf2',
            complex(5,5): bytearray(b'\xe3\xe4\xe5'),
            complex(4,6): memoryview(b'abcefg'),
            complex(3,7): innerList,
            # complex(8: (3,4.5),
            b'az': 9,
            b'by': 8.7,
            b'cx': complex(6, 5),
            b'dw': "azerty",
            b'ev': b'\xf0\xf1\xf2',
            b'fu': bytearray(b'\xe3\xe4\xe5'),
            b'gt': memoryview(b'abcefg'),
            b'hs': innerList,
            # 'i': (3,4.5),
            memoryview(b'er'): 1,
            memoryview(b'ty'): 2.3,
            memoryview(b'ui'): complex(4, 5),
            memoryview(b'op'): "azerty",
            memoryview(b'qs'): b'\xf0\xf1\xf2',
            memoryview(b'df'): bytearray(b'\xe3\xe4\xe5'),
            memoryview(b'gh'): memoryview(b'abcefg'),
            memoryview(b'jk'): sampleList,
            # 'ir': (3,4.5),
            frozenset([0, 1]): 1,
            frozenset([2.0, 3.1]): 2.3,
            frozenset([complex(0, 1), complex(2, 3)]): complex(4, 5),
            frozenset(["0", "1"]): "azerty",
            frozenset([b'01', b'23']): b'\xf0\xf1\xf2',
            frozenset([b'32', 1]): bytearray(b'\xe3\xe4\xe5'),
            frozenset([memoryview(b'eswascz'), memoryview(b'plmoijk')]): memoryview(b'abcefg'),
            frozenset([2, 3]): sampleList,
            # tuple(X): (3,4.5),
        }
        sampleDictionnary = {
            True:False,
            'a': 1,
            'b': 2.3,
            'c': complex(4,5),
            'd': "azerty",
            'e': b'\xf0\xf1\xf2',
            'f': bytearray(b'\xe3\xe4\xe5'),
            'g': memoryview(b'abcefg'),
            'h': sampleList,
            #'i': (3,4.5),
            'k': innerDictionnary,
            0: 1,
            1: 2.3,
            2: complex(4,5),
            3: "azerty",
            4: b'\xf0\xf1\xf2',
            5: bytearray(b'\xe3\xe4\xe5'),
            6: memoryview(b'abcefg'),
            7: sampleList,
            #8: (3,4.5),
            10: innerDictionnary,
            10.: 1,
            9.1: 2.3,
            8.2: complex(4, 5),
            7.3: "azerty",
            6.4: b'\xf0\xf1\xf2',
            5.5: bytearray(b'\xe3\xe4\xe5'),
            4.6: memoryview(b'abcefg'),
            3.7: sampleList,
            # 2: (3,4.5),
            0.1: innerDictionnary,
            complex(1,0): 1,
            complex(9,1): 2.3,
            complex(8,2): complex(4, 5),
            complex(7,3): "azerty",
            complex(6,4): b'\xf0\xf1\xf2',
            complex(5,5): bytearray(b'\xe3\xe4\xe5'),
            complex(4,6): memoryview(b'abcefg'),
            complex(3,7): sampleList,
            # complex(2: (3,4.5),
            complex(0,1): innerDictionnary,
            b'az': 1,
            b'by': 2.3,
            b'cx': complex(4, 5),
            b'dw': "azerty",
            b'ev': b'\xf0\xf1\xf2',
            b'fu': bytearray(b'\xe3\xe4\xe5'),
            b'gt': memoryview(b'abcefg'),
            b'hs': sampleList,
            # 'ir': (3,4.5),
            b'ju': innerDictionnary,
            memoryview(b'er'): 1,
            memoryview(b'ty'): 2.3,
            memoryview(b'ui'): complex(4, 5),
            memoryview(b'op'): "azerty",
            memoryview(b'qs'): b'\xf0\xf1\xf2',
            memoryview(b'df'): bytearray(b'\xe3\xe4\xe5'),
            memoryview(b'gh'): memoryview(b'abcefg'),
            memoryview(b'jk'): sampleList,
            # 'ir': (3,4.5),
            memoryview(b'lm'): innerDictionnary,
            frozenset([0,1]): 1,
            frozenset([2.0,3.1]): 2.3,
            frozenset([complex(0, 1),complex(2, 3)]): complex(4, 5),
            frozenset(["0","1"]): "azerty",
            frozenset([b'01',b'23']): b'\xf0\xf1\xf2',
            frozenset([b'32',1]): bytearray(b'\xe3\xe4\xe5'),
            frozenset([memoryview(b'eswascz'),memoryview(b'plmoijk')]): memoryview(b'abcefg'),
            frozenset([2,3]): sampleList,
            # tuple(X): (3,4.5),
            frozenset({'jack': 4098, 12.3: complex(41,39)}): innerDictionnary,
        }
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
