#!/bin/bash
# DESCRIPTION:
#   The script mainly burns danmaku into new video and delete original files, along with starting video uploading.
#
# PARAMETERS:
#   INPUT: 
#       $1 - the full path of the video
#   OUTPUT:
#       $formatVideoName - eg:/path/to/video/roomid_YYYY-MM-DD-HH.mp4

# check if the filename is provided.
if [ $# -ne 1 ]; then
    echo "Usage: $0 filename"
    exit 1
fi

# obtain full path
fullPath=$1

# delete json files
filenameWithoutExt="${fullPath%.*}"
jsonlPath="${filenameWithoutExt}.jsonl"
rm $jsonlPath

# use dirname to obtain the path，along with basename to obtain filename.
path=$(dirname "$fullPath")
filename=$(basename "$fullPath")

# extract the extonsion name.
extension="${filename##*.}"

roomid=$(echo "$filename" | cut -d'_' -f1)
timestamp=$(echo "$filename" | cut -d'_' -f2)

# retrieve parameters. 
year=${timestamp:0:4}
month=${timestamp:4:2}
day=${timestamp:6:2}
hour=${timestamp:9:2}

# format the file name
formatVideoName="${path}/${roomid}_${year}-${month}-${day}-${hour}.${extension}"

# generate the converted subtitle file name
assPath="${path}/${roomid}_${year}-${month}-${day}-${hour}.ass"

# use DanmakuFactory to convert the xml file
xmlPath="${filenameWithoutExt}.xml"
if [ -f "$xmlPath" ]; then
    $BILIVE_PATH/src/utils/DanmakuFactory -o "$assPath" -i "$xmlPath" --msgboxfontsize 30 --ignore-warnings
    rm $xmlPath
    echo “danmaku convert success!”
    export ASS_PATH="$assPath"
    python3 $BILIVE_PATH/src/utils/removeEmojis.py >> $BILIVE_PATH/logs/removeEmojis.log 2>&1
fi

# Burn danmaku into video.
if [ -f "$assPath" ]; then
    # The only cpu version
    # ffmpeg -y -i $fullPath -vf ass=$assPath -preset ultrafast $formatVideoName > $BILIVE_PATH/logs/burningLog/burn-$(date +%Y%m%d%H%M%S).log 2>&1
    # The Nvidia GPU accelerating version
    ffmpeg -y -hwaccel cuda -c:v h264_cuvid -i $fullPath -c:v h264_nvenc -vf ass=$assPath $formatVideoName > $BILIVE_PATH/logs/burningLog/burn-$(date +%Y%m%d%H%M%S).log 2>&1
    rm $assPath
else
    # The only cpu version
    # ffmpeg -y -i $fullPath -vf -preset ultrafast $formatVideoName > $BILIVE_PATH/logs/burningLog/burn-$(date +%Y%m%d%H%M%S).log 2>&1
    # The Nvidia GPU acceleting version
    ffmpeg -y -hwaccel cuda -c:v h264_cuvid -i $fullPath -c:v h264_nvenc $formatVideoName > $BILIVE_PATH/logs/burningLog/burn-$(date +%Y%m%d%H%M%S).log 2>&1
fi

echo "ffmpeg successfully complete!"

# Delete the original video.
rm $fullPath

python $BILIVE_PATH/src/subtitle/generate.py $formatVideoName > $BILIVE_PATH/logs/burningLog/subtitlesGenerate-$(date +%Y%m%d%H%M%S).log 2>&1
srtPath=${formatVideoName%.*}".srt"
videoUploadPath=${formatVideoName%.*}"-s.mp4"
ffmpeg -hwaccel cuda -c:v h264_cuvid -i "$formatVideoName" -c:v h264_nvenc -vf "subtitles=$srtPath" "$videoUploadPath" -y -nostdin > $BILIVE_PATH/logs/burningLog/subtitlesRender-$(date +%Y%m%d%H%M%S).log 2>&1
rm $srtPath
rm $formatVideoName

echo "==================== add $videoUploadPath to upload queue ===================="
echo "$videoUploadPath" >> $BILIVE_PATH/src/uploadProcess/uploadVideoQueue.txt