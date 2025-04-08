#!/bin/bash

# Query the project path
CURRENT_PATH=$(pwd)
# Export the project path to the .bashrc file for the current user using the bash shell
echo "export BILIVE_PATH=$CURRENT_PATH # This for timerring/bilive project path" >> ~/.bashrc
# Make the changes to the .bashrc file immediately effective
echo " Have set the project path $CURRENT_PATH to .bashrc for the current user."
source ~/.bashrc

# kill the previous scan and upload process
kill -9 $(ps aux | grep 'src.burn.scan' | grep -v grep | awk '{print $2}')
kill -9 $(ps aux | grep '[u]pload' | awk '{print $2}')
# start new process
nohup python -m src.burn.scan > $BILIVE_PATH/logs/runtime/scan-$(date +%Y%m%d-%H%M%S).log 2>&1 &
nohup python -m src.upload.upload > $BILIVE_PATH/logs/runtime/upload-$(date +%Y%m%d-%H%M%S).log 2>&1 &
# Check if the last command was successful
if [ $? -eq 0 ]; then
    echo "Success! Please ignore the 'kill: usage....' if it displays"
else
    echo "An error occurred while starting scanSegments. Check the logs for details."
fi