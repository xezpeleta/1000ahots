import pandas as pd
import argparse

def filter_and_group_segments(input_file, output_file, max_gap=0.4, filter_type="music", music_min_threshold=None, music_max_threshold=None, speech_min_threshold=None, speech_max_threshold=None, min_duration=0.0):
    # Read data from CSV
    df = pd.read_csv(input_file)
    
    if filter_type == "music":
        # If music_threshold and speech_threshold are not provided, use default values
        if music_min_threshold is None:
            music_min_threshold = 0.4
        if speech_max_threshold is None:
            speech_max_threshold = 0.9
        filtered_df = df[(df['music_prob'] > music_min_threshold) & (df['speech_prob'] < speech_max_threshold)]
    elif filter_type == "speech":
        # If music_threshold and speech_threshold are not provided, use default values
        if music_max_threshold is None:
            music_max_threshold = 0.2
        if speech_min_threshold is None:
            speech_min_threshold = 0.8
        filtered_df = df[(df['music_prob'] < music_max_threshold) & (df['speech_prob'] > speech_min_threshold)]
    
    # Select only start_time and end_time columns
    result = filtered_df[['start_time_s', 'end_time_s']]
    
    # Rename columns for output
    result.columns = ['start_time', 'end_time']
    
    # Sort by start_time to ensure ordering
    result = result.sort_values(by="start_time").reset_index(drop=True)
    
    # Group segments that are consecutive or close (within max_gap)
    grouped_segments = []
    current_start = result.iloc[0]['start_time']
    current_end = result.iloc[0]['end_time']
    
    for i in range(1, len(result)):
        row = result.iloc[i]
        # Check if the current segment is close enough to merge
        if row['start_time'] <= current_end + max_gap:
            # Extend the current segment
            current_end = row['end_time']
        else:
            # Append the current segment and start a new one
            grouped_segments.append((current_start, current_end))
            current_start = row['start_time']
            current_end = row['end_time']
    
    # Append the last segment
    grouped_segments.append((current_start, current_end))
    
    # Filter out segments shorter than min_duration
    grouped_segments = [(start, end) for start, end in grouped_segments if end - start >= min_duration]
    
    # Convert to DataFrame and save to CSV
    grouped_df = pd.DataFrame(grouped_segments, columns=['start_time', 'end_time'])
    grouped_df.to_csv(output_file, index=False)
    print(f"Grouped segments saved to {output_file}")

if __name__ == "__main__":
    # Set up argument parser
    parser = argparse.ArgumentParser(description="Filter and group audio segments based on music and speech probabilities.")
    parser.add_argument("input_file", help="Path to the input CSV file.")
    parser.add_argument("output_file", help="Path to the output CSV file.")
    parser.add_argument("--filter_type", choices=["music", "speech"], help="Type of filter to apply.")
    parser.add_argument("--music_max_threshold", type=float, help="Threshold for music probability.")
    parser.add_argument("--music_min_threshold", type=float, help="Threshold for music probability.")
    parser.add_argument("--speech_min_threshold", type=float, help="Threshold for speech probability.")
    parser.add_argument("--speech_max_threshold", type=float, help="Threshold for speech probability.")
    parser.add_argument("--max_gap", type=float, default=0.4, help="Maximum gap (in seconds) between segments to consider for grouping.")
    parser.add_argument("--min_duration", type=float, default=0.0, help="Minimum duration (in seconds) for a segment to be considered.")

    # Parse arguments
    args = parser.parse_args()
    
    # Run the filtering and grouping function
    filter_and_group_segments(args.input_file, args.output_file, args.max_gap, args.filter_type, args.music_min_threshold, args.music_max_threshold, args.speech_min_threshold, args.speech_max_threshold, args.min_duration)

