# coding=utf-8
# global initialization
dictAttr = "__dict__"
# common functions
def convertObjetTodict( objectToConvert ):
	objectDict = objectToConvert
	if hasattr( objectToConvert, dictAttr ):
		objectDict = objectToConvert.__dict__
	return objectDict
def objectHash( objectToHash ):
	# assume object to hash is null
	objectDict = None
	# if object to hash is really an object
	if hasattr( objectToHash, dictAttr ):
		# transform fields & values to dictonary 
		objectDict = objectToHash.__dict__
		# check each value
		for field, value in objectDict.items():
			# if value is a (unhashable) list
			if isinstance ( value , list ) :
				# transform (unhashable) list to (hashable) tuple
				valueTuple = tuple(value)
				objectDict[field] = valueTuple
			# if value is a (unhashable) dictionary
			elif isinstance ( value , dict ) :
				# transform (unhashable) list to (hashable) tuple
				valueFrozenSet = frozenset(value.items())
				objectDict[field] = valueFrozenSet
	# transform (unhashable) dictionary to (hashable) frozen set
	objectFrozenSet = frozenset(objectDict.items())
	# compute and return hash
	hashedObject = hash ( objectFrozenSet )
	return hashedObject
def objectComparison( objectOriginal, objectModel ):
	comparison = type( objectOriginal ) == type( objectModel )
	if comparison:
		# dictionarize original & model objects
		objectOriginalDict = convertObjetTodict( objectOriginal )
		objectModelDict = convertObjetTodict( objectModel )
		# compare & return objects
		comparison = objectOriginalDict == objectModelDict
	return comparison
def objectStringRepresentation( objectToStr ):
	# dictiarize object
	objectDict = convertObjetTodict( objectToStr )
	# stringize & return objects
	objectStr = str( {"type": type( objectToStr ), "value": objectDict} )
	return objectStr
def methodArgsStringRepresentation( parametersList , localValuesDict ):
	# assume methods has no parameters
	methodArgsDict = dict()
	# keep only method parameters matching local ones
	for parameter in parametersList:
		parameterName = parameter
		if hasattr( parameter, "name" ):
			parameterName = parameter.name
		if parameterName in localValuesDict:
			methodArgsDict[parameterName] = localValuesDict[parameterName]
	# stringize & return method parameters
	methodArgsString = str( methodArgsDict )
	return methodArgsString
''' POPO
INFO : it is not the French word for poop, but an equivalent of POJO'''
class POPO :
	# representations
	def __repr__( self ):
		return objectStringRepresentation( self )
	def __str__( self ):
		return self.__repr__()
# bean
class Bean( POPO ):
	# comparison
	def __hash__( self ):
		return objectHash( self )
	def __eq__( self, other ):
		return objectComparison( self, other )
