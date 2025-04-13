#!/bin/bash

LOGS_DIR="./logs"
SUBDIRS=("record" "runtime" "scan" "upload")

for subdir in "${SUBDIRS[@]}"; do
    FULL_PATH="$LOGS_DIR/$subdir"
    if [ ! -d "$FULL_PATH" ]; then
        mkdir -p "$FULL_PATH"
        echo "Created directory: $FULL_PATH"
    else
        echo "Directory already exists: $FULL_PATH"
    fi
done

# Run the record script
./record.sh

# Start the scan process in the background
nohup python -m src.burn.scan > ./logs/runtime/scan-$(date +%Y%m%d-%H%M%S).log 2>&1 &

# Start the upload process
exec python -m src.upload.upload