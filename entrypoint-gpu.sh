#!/bin/bash
if [ ! -f /app/config/cookies.json ]; then
    cp /app/src/utils/cookies.json /app/config/cookies.json
else    
    cp /app/config/cookies.json /app/src/utils/cookies.json
fi

if [ ! -f /app/config/settings.toml ]; then
    cp /app/settings.toml /app/config/settings.toml
else    
    cp /app/config/settings.toml /app/settings.toml
fi

if [ ! -f /app/config/config.py ]; then
    cp /app/src/config.py /app/config/config.py
else    
    cp /app/config/config.py /app/src/config.py
fi

# Check if the logs folder exists, and whether there are four subfolders: blrec, runtime, scan, upload. If not, create them
if [ ! -d /app/logs ]; then
    mkdir /app/logs
fi

log_sub_dir=("blrec" "runtime" "scan" "upload")
for sub_dir in ${log_sub_dir[@]}; do
    if [ ! -d /app/logs/$sub_dir ]; then
        mkdir /app/logs/$sub_dir
    fi
done


./record.sh && ./scan.sh

python -m src.upload.upload