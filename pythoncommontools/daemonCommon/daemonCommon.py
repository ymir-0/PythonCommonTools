# coding=utf-8
# imports
from argparse import ArgumentParser
from inspect import signature
from os import kill , remove
from os.path import isfile
from signal import SIGTERM

from pythoncommontools.logger import logger
from pythoncommontools.objectUtil.objectUtil import methodArgsStringRepresentation
from psutil import Process , pid_exists
# global initialization
runMarkup = "-r"
# common daemon
def daemonize ( customStart, customStop, customStatus ):
	# logger context
	argsStr = methodArgsStringRepresentation( signature( daemonize ).parameters, locals() )
	# logger input
	logger.loadedLogger.input ( __name__ , functionOrmethod = daemonize.__name__ , message = argsStr )
	# parse parameters
	parser = ArgumentParser()
	parser.add_argument( "action", help = "start|stop|status", type = str )
	args = parser.parse_args()
	# start
	if args.action == "start":
		customStart()
	# stop
	elif args.action == "stop":
		customStop()
	# status
	elif args.action == "status":
		customStatus()
	# bad action
	else:
		raise Exception ( "Unknown command" )
	# logger output
	logger.loadedLogger.output ( __name__ , functionOrmethod = daemonize.__name__ )
def start ( commandName, **commandArguments ):
	# logger context
	argsStr = methodArgsStringRepresentation( signature( start ).parameters, locals() )
	# logger input
	logger.loadedLogger.input ( __name__ , functionOrmethod = start.__name__ , message = argsStr )
	# parse arguments
	argumentsParser = ArgumentParser()
	argumentsParser.add_argument( "module" )
	argumentsParser.add_argument( runMarkup, help = "running (not unit test)", action = "store_true" )
	argumentsParser.add_argument( "--port" )
	argumentsParser.add_argument( "--verbosity" )
	arguments = argumentsParser.parse_args()
	# run if specified
	if arguments.r:
		commandName( **commandArguments )
	else:
		logger.loadedLogger.info ( __name__ , functionOrmethod = start.__name__ , message = "running as unit test" )
	# logger output
	logger.loadedLogger.output ( __name__ , functionOrmethod = start.__name__ )
def stop( pidFile ):
	# logger context
	argsStr = methodArgsStringRepresentation( signature( stop ).parameters, locals() )
	# logger input
	logger.loadedLogger.input ( __name__ , functionOrmethod = stop.__name__ , message = argsStr )
	# only if a PID is registered
	if isfile( pidFile ) :
		# read PID file
		with open( pidFile ) as pidFileContent:
			pidTuple = tuple( pidFileContent.readlines() )
		# kill process (if exists)
		for pidString in pidTuple:
			pidNumber = int( pidString )
			# only if a process is associated to PID
			if pid_exists( pidNumber ):
				kill ( pidNumber, SIGTERM )
		# remove files
		remove( pidFile )
	# logger output
	logger.loadedLogger.output ( __name__ , functionOrmethod = stop.__name__ )
def status( pidFile ):
	# logger context
	argsStr = methodArgsStringRepresentation( signature( status ).parameters, locals() )
	# logger input
	logger.loadedLogger.input ( __name__ , functionOrmethod = status.__name__ , message = argsStr )
	# initialize state set
	stateSet = set()
	# only if a PID is registered
	if isfile( pidFile ) :
		# read PID file
		with open( pidFile ) as pidFileContent:
			pidTuple = tuple( pidFileContent.readlines() )
		# check process
		stateSet = set()
		for pidString in pidTuple:
			pidNumber = int( pidString )
			state = None
			# only if a process is associated to PID
			if pid_exists( pidNumber ):
				process = Process( pidNumber )
				state = process.status
				stateSet.add( state )
	# set state frozen set
	stateFrozenset = frozenset( stateSet )
	# logger output
	logger.loadedLogger.output ( __name__ , functionOrmethod = status.__name__ , message = stateFrozenset )
	# return state
	return stateFrozenset
