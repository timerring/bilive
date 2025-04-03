import os
import json
import re
import subprocess
from groq import Groq
from src.config import WHISPER_API_KEY

def seconds_to_srt_time(seconds):
    hours = int(seconds // 3600)
    minutes = int((seconds % 3600) // 60)
    secs = int(seconds % 60)
    millis = int((seconds - int(seconds)) * 1000)
    return f"{hours:02d}:{minutes:02d}:{secs:02d},{millis:03d}"

def write_to_srt(segments, output_file):
    with open(output_file, 'w', encoding='utf-8') as f:
        for i, segment in enumerate(segments, start=1):
            start_time = seconds_to_srt_time(segment['start'])
            end_time = seconds_to_srt_time(segment['end'])
            text = segment['text']
            # filter out the illusion
            if "请不吝" in text:
                text = ""
            f.write(f"{i}\n")
            f.write(f"{start_time} --> {end_time}\n")
            f.write(f"{text}\n\n")

def print_segment_info(segments):
    if segments:
        for segment in segments:
            start_time = segment.get('start')
            end_time = segment.get('end')
            text = segment.get('text')
            print(f"Start time: {start_time} seconds, End time: {end_time} seconds, Text: {text}")
    else:
        print("No valid segments data found.") 


def check_file_format(filename):
    if filename[-4:] != ".mp3":
        mp3filename = filename[:-4] + ".mp3"
        command = [
        'ffmpeg', '-i', filename, '-vn', '-acodec', 'libmp3lame', mp3filename
        ]
        subprocess.run(command, check=True, capture_output=True, text=True)
        return mp3filename
    else:
        return filename

# Groq API SDK: https://console.groq.com/docs/speech-to-text
# due to the limit of API, 40 MB (free tier), 100MB (dev tier)
# Requests per minute: 20, per day: 2000. And 7200 seconds / hour, 28800 seconds / day.
# more info: https://console.groq.com/docs/rate-limits
def generate_srt(filename, output_file=None):
    client = Groq(
        api_key=WHISPER_API_KEY
    )
    filename = check_file_format(filename)
    if output_file is None:
        output_file = filename[:-4] + ".srt"
    try:
        with open(filename, "rb") as file:
            transcription = client.audio.transcriptions.create(
            file=file, # Required audio file
            model="whisper-large-v3-turbo", # Required model to use for transcription
            prompt="以下是普通话的句子",  # Optional
            response_format="verbose_json",  # Optional
            timestamp_granularities = ["segment"], # Optional (must set response_format to "json" to use and can specify "word", "segment" (default), or both)
            #   language="zh",  # Optional
            temperature=0.0  # Optional
            )
            input_str = json.dumps(transcription, indent=2, default=str)
            # use index to segment the input_str
            start_index = input_str.find('segments=') + len('segments=')
            end_index = input_str.rfind(']') + 1
            segments_str = input_str[start_index:end_index]
            segments = json.loads(segments_str.replace("'", "\""))
            # print_segment_info(segments)
            write_to_srt(segments, output_file)
        # remove the audio file
        os.remove(filename)
        return output_file
    except Exception as e:
        print(f"Error: {e}")
        return None

if __name__ == "__main__":
    filename = ""
    generate_srt(filename)