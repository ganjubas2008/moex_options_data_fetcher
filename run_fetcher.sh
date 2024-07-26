#!/bin/bash

# Path to the Python script
SCRIPT_PATH="main.py"

# Path to the log file
LOG_FILE_STDOUT="fetcher_stdout.log"
LOG_FILE_STDERR="fetcher_stderr.log"

# Path to the PID file
PID_FILE="fetcher.pid"

# Run the Python script in the background, redirect stdout and stderr, and store the PID
nohup python3 $SCRIPT_PATH > $LOG_FILE_STDOUT 2> $LOG_FILE_STDERR & echo $! > $PID_FILE

echo Fetcher process $! started.
echo $! > $PID_FILE
