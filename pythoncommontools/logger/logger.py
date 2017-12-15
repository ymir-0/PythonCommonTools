# coding=utf-8
# imports
import logging
from logging import Logger as DefaultLogger
from logging.config import fileConfig
# global initialization
loadedLogger = None
# read configuration
def loadLogger( name, logConfigurationFilePath ):
	global loadedLogger
	if not loadedLogger:
		loadedLogger = Logger( name, logConfigurationFilePath )
# logger class
class Logger( DefaultLogger ):
	# static fields
	methodSeparator = '.'
	# methods
	def input ( self , moduleName , className = '' , functionOrmethod = '' , message = '' ) :
		DefaultLogger.info ( self , "INPUT - " + Logger.format ( moduleName , className , functionOrmethod ,
		                                                         message ) )
	def output ( self , moduleName , className = '' , functionOrmethod = '' , message = '' ) :
		DefaultLogger.info ( self ,
		                     "OUTPUT - " + Logger.format ( moduleName , className , functionOrmethod , message ) )
	def debug ( self , moduleName , className = '' , functionOrmethod = '' , message = '' ) :
		DefaultLogger.debug ( self , Logger.format ( moduleName , className , functionOrmethod , message ) )
	def info ( self , moduleName , className = '' , functionOrmethod = '' , message = '' ) :
		DefaultLogger.info ( self , Logger.format ( moduleName , className , functionOrmethod , message ) )
	def warning ( self , moduleName , className = '' , functionOrmethod = '' , message = '' ) :
		DefaultLogger.warning ( self , Logger.format ( moduleName , className , functionOrmethod , message ) )
	def error ( self , moduleName , className = '' , functionOrmethod = '' , message = '' ) :
		DefaultLogger.error ( self , Logger.format ( moduleName , className , functionOrmethod , message ) )
	def critical ( self , moduleName , className = '' , functionOrmethod = '' , message = '' ) :
		DefaultLogger.critical ( self , Logger.format ( moduleName , className , functionOrmethod , message ) )
	@staticmethod
	def format ( moduleName , className , functionOrmethod , rawMessage ) :
		# initialize formatted message
		formattedMessage = moduleName
		# add class if exists
		if len( className ) > 0:
			formattedMessage = Logger.methodSeparator.join( ( formattedMessage , className, ) )
		# add function/method if exists
		if len( functionOrmethod ) > 0:
			formattedMessage = Logger.methodSeparator.join( ( formattedMessage , functionOrmethod, ) )
		# add raw message only if exists
		rawMessageStr = str( rawMessage )
		if len( rawMessageStr ) > 0:
			formattedMessage = " : ".join( ( formattedMessage , rawMessageStr, ) )
		# return formatted message
		return formattedMessage
	# constructors
	def __init__( self, name, logConfigurationFilePath ):
		# load logging configuration
		fileConfig( logConfigurationFilePath )
		# initialize from upper class
		super().__init__( name )
		# add default "root" handler
		self.addHandler( logging.getLogger() )
