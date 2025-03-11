# kill the previous scanSegments process
kill -9 $(ps aux | grep '[u]pload' | awk '{print $2}')
kill -9 $(ps aux | grep '[b]iliup' | awk '{print $2}')
# start the scanSegments process
# nohup $BILIVE_PATH/src/upload/uploadQueue.sh > $BILIVE_PATH/logs/uploadQueue.log 2>&1 &
python -m src.upload.upload
# Check if the last command was successful
if [ $? -eq 0 ]; then
    echo "success"
else
    echo "An error occurred while starting upload. Check the logs for details."
fi