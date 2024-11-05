"""
The following script removes the music segments from an audio file
"""

import argparse
import subprocess
import pandas as pd

"""
Remove segments from an audio file based on start and end times,
using ffmpeg with subprocess.
"""
def remove_segments(input_file, output_file, start_times, end_times, before, after):
    # Create a list of start and end time pairs with margins
    segments = list(zip(start_times - before, end_times + after))
    
    # Generate the filter string for ffmpeg
    filter_str = ""
    for i, (start, end) in enumerate(segments):
        filter_str += f"[0:a]atrim=start={start}:end={end},asetpts=PTS-STARTPTS[a{i}];"
    for i in range(len(segments)):
        filter_str += f"[a{i}]"
    filter_str += f"concat=n={len(segments)}:v=0:a=1[outa]"
    
    # Run ffmpeg to remove the segments
    cmd = [
        "ffmpeg",
        "-i", input_file,
        "-filter_complex", filter_str,
        "-map", "[outa]",
        output_file
    ]
    subprocess.run(cmd)

def remove_music_segments(input_file, output_file, music_segments_file, before, after):
    # Load music segments from CSV
    music_segments = pd.read_csv(music_segments_file)
    
    # Remove music segments from the audio file
    remove_segments(input_file, output_file, music_segments['start_time'], music_segments['end_time'], before, after)
    print(f"Music segments removed and saved to {output_file}")

if __name__ == "__main__":
    # Set up argument parser
    parser = argparse.ArgumentParser(description="Remove music segments from audio file.")
    parser.add_argument("input", help="Path to the input audio file.")
    parser.add_argument("output", help="Path to the output audio file without music.")
    parser.add_argument("music_segments", help="Path to the CSV file with music segments to remove.")
    parser.add_argument("--before", type=float, default=0, help="Margin time in seconds to add before each segment.")
    parser.add_argument("--after", type=float, default=0, help="Margin time in seconds to add after each segment.")

    # Parse arguments
    args = parser.parse_args()

    # Run the music removal function
    remove_music_segments(args.input, args.output, args.music_segments, args.before, args.after)
