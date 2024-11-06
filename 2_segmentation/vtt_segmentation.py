import argparse
import subprocess
from datetime import datetime, timedelta
import webvtt

# Function to convert VTT time to seconds
def vtt_time_to_seconds(vtt_time):
    hours, minutes, seconds = vtt_time.split(':')
    seconds, milliseconds = seconds.split('.')
    return int(hours) * 3600 + int(minutes) * 60 + int(seconds) + int(milliseconds) / 1000

def segmentate(input_file, output_file, start_time, end_time):
    command = [
        'ffmpeg', '-i', input_file,
        '-ss', str(start_time), '-to', str(end_time),
        '-c', 'copy', output_file
    ]
    subprocess.run(command)
    print(f"Created segment: {segment_file} - {caption.text}")


if __name__ == "__main__":
    # Parse arguments
    parser = argparse.ArgumentParser(description="VTT segmentation")
    parser.add_argument("vtt", help="Input VTT file")
    parser.add_argument("audio", help="Input audio file")
    args = parser.parse_args()
    vtt_file = args.vtt
    audio_file = args.audio

    # Run VTT segmentation
    for i, caption in enumerate(webvtt.read(vtt_file)):
        start_time = vtt_time_to_seconds(caption.start)
        end_time = vtt_time_to_seconds(caption.end)
        segment_file = f'segment_{i+1}.mp3'

        # Create segment
        segmentate(audio_file, segment_file, start_time, end_time)
