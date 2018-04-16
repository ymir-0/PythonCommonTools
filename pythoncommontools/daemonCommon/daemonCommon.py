# coding=utf-8
# imports
from argparse import ArgumentParser
from os import kill , remove
from os.path import isfile
from signal import SIGTERM
from psutil import Process , pid_exists
# global initialization
runMarkup = "-r"
# common daemon
def daemonize ( customStart, customStop, customStatus ):
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
def start ( commandName, **commandArguments ):
    # parse arguments
    argumentsParser = ArgumentParser()
    argumentsParser.add_argument( "module" )
    argumentsParser.add_argument( runMarkup, help = "running (not unit test)", action = "store_true" )
    argumentsParser.add_argument( "--port" )
    argumentsParser.add_argument( "--verbosity" )
    arguments = argumentsParser.parse_args()
    # run if specified
    if arguments.r: commandName( **commandArguments )
def stop( pidFile ):
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
def status( pidFile ):
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
    # return state
    return stateFrozenset
