"""
The following script extracts speech segments from an audio file using a CSV file containing speech segment timestamps,
then splits them further based on silence detection
"""

import argparse
import subprocess
import pandas as pd
import os
import tempfile
from pydub import AudioSegment
from pydub.silence import split_on_silence

def split_on_silence_threshold(audio_segment, min_silence_len, silence_thresh):
    """
    Split an audio segment on silence using pydub
    """
    chunks = split_on_silence(
        audio_segment,
        min_silence_len=min_silence_len,
        silence_thresh=silence_thresh,
        keep_silence=True
    )
    return chunks

def extract_speech_segments(input_file, output_dir, speech_segments_file, before, after, min_silence_len, silence_thresh):
    """
    Extract speech segments and split them further based on silence detection
    """
    # Load speech segments from CSV
    speech_segments = pd.read_csv(speech_segments_file)
    
    # Create output directory if it doesn't exist
    os.makedirs(output_dir, exist_ok=True)
    
    # Get base filename without extension
    base_name = os.path.splitext(os.path.basename(input_file))[0]
    
    # Get audio duration
    duration = float(subprocess.check_output([
        'ffprobe', '-v', 'quiet', '-show_entries', 'format=duration',
        '-of', 'default=noprint_wrappers=1:nokey=1', input_file
    ]).decode().strip())
    
    # Extract each speech segment
    segment_counter = 0
    with tempfile.TemporaryDirectory() as temp_dir:
        for i, row in speech_segments.iterrows():
            temp_file = os.path.join(temp_dir, f"temp_segment_{i}.wav")
            
            # Adjust segment times with margins
            adj_start = max(0, row['start_time'] - before)
            adj_end = min(duration, row['end_time'] + after)
            
            # Extract segment to temporary file
            cmd = [
                "ffmpeg",
                "-i", input_file,
                "-ss", str(adj_start),
                "-to", str(adj_end),
                "-c", "copy",
                temp_file
            ]
            subprocess.run(cmd)
            
            # Load temporary file with pydub
            audio = AudioSegment.from_wav(temp_file)
            
            # Split on silence
            chunks = split_on_silence_threshold(audio, min_silence_len, silence_thresh)
            
            # Save chunks
            for chunk in chunks:
                output_file = os.path.join(output_dir, f"{base_name}_speech_{segment_counter:03d}.wav")
                chunk.export(output_file, format="wav")
                print(f"Created speech segment: {output_file}")
                segment_counter += 1

if __name__ == "__main__":
    # Set up argument parser
    parser = argparse.ArgumentParser(description="Extract speech segments from audio file.")
    parser.add_argument("input", help="Path to the input audio file.")
    parser.add_argument("output_dir", help="Directory to save speech segment files.")
    parser.add_argument("speech_segments", help="Path to the CSV file with speech segments data.")
    parser.add_argument("--before", type=float, default=0, help="Margin time in seconds to add before each segment.")
    parser.add_argument("--after", type=float, default=0, help="Margin time in seconds to add after each segment.")
    parser.add_argument("--min-silence-len", type=int, default=500,
                      help="Minimum length of silence (in ms) to split on.")
    parser.add_argument("--silence-thresh", type=int, default=-40,
                      help="Silence threshold in dBFS.")

    # Parse arguments
    args = parser.parse_args()

    # Run the speech extraction function
    extract_speech_segments(
        args.input, 
        args.output_dir, 
        args.speech_segments, 
        args.before, 
        args.after,
        args.min_silence_len,
        args.silence_thresh
    )
