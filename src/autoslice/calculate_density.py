import re
from collections import defaultdict
from src.config import SLICE_DURATION

def parse_time(time_str):
    """Convert ASS time format to seconds with milliseconds."""
    h, m, s = time_str.split(':')
    s, ms = s.split('.')
    return int(h) * 3600 + int(m) * 60 + int(s) + int(ms) / 100

def format_time(seconds):
    """Format seconds to hh:mm:ss.xx."""
    h = int(seconds // 3600)
    m = int((seconds % 3600) // 60)
    s = int(seconds % 60)
    ms = int((seconds - int(seconds)) * 100)
    return f"{h:02}:{m:02}:{s:02}.{ms:02}"

def extract_dialogues(file_path):
    """Extract dialogue start times from the ASS file."""
    dialogues = []
    with open(file_path, 'r', encoding='utf-8') as file:
        for line in file:
            if line.startswith('Dialogue:'):
                parts = line.split(',')
                start_time = parse_time(parts[1].strip())
                dialogues.append(start_time)
    return dialogues

def calculate_density(dialogues, window_size=SLICE_DURATION):
    """Calculate the maximum density of dialogues in a given window size."""
    time_counts = defaultdict(int)
    for time in dialogues:
        time_counts[time] += 1

    max_density = 0
    max_start_time = 0

    # Use a sliding window to calculate density
    sorted_times = sorted(time_counts.keys())
    for i in range(len(sorted_times)):
        start_time = sorted_times[i]
        end_time = start_time + window_size
        current_density = sum(count for time, count in time_counts.items() if start_time <= time < end_time)
        if current_density > max_density:
            max_density = current_density
            max_start_time = start_time

    return max_start_time, max_density