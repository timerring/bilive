# kill the previous scan and upload process
kill -9 $(ps aux | grep 'src.burn.scan' | grep -v grep | awk '{print $2}')
kill -9 $(ps aux | grep '[u]pload' | awk '{print $2}')
# start new process
nohup python3 -m src.burn.scan > ./logs/runtime/scan-$(date +%Y%m%d-%H%M%S).log 2>&1 &
nohup python3 -m src.upload.upload > ./logs/runtime/upload-$(date +%Y%m%d-%H%M%S).log 2>&1 &
# Check if the last command was successful
if [ $? -eq 0 ]; then
    echo "Success! Please ignore the 'kill: usage....' if it displays"
else
    echo "An error occurred while starting scanSegments. Check the logs for details."
fi