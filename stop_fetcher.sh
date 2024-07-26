#!/bin/bash

# Path to the PID file
PID_FILE="fetcher.pid"

# Check if the PID file exists
if [ -f $PID_FILE ]; then
    # Read the PID from the file
    PID=$(cat $PID_FILE)
    
    # Kill the process
    kill $PID
    
    # Remove the PID file
    rm $PID_FILE
    
    echo "Fetcher process $PID has been stopped."
else
    echo "No fetcher process is currently running."
fi
