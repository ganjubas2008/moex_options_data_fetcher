#!/bin/bash

# Path to the Python script
SCRIPT_PATH="main.py"

# Path to the log file
LOG_FILE="fetcher.log"

# Path to the PID file
PID_FILE="fetcher.pid"

# Run the Python script in the background, redirect stdout and stderr, and store the PID
nohup python3 $SCRIPT_PATH > /dev/null 2>> $LOG_FILE &
echo Fetcher process $! started.
echo $! > $PID_FILE
