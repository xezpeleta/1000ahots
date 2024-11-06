import pandas as pd
import argparse

def match_segments_with_speakers(good_segments_file, diarization_file, output_file):
    # Load the segments data
    good_segments = pd.read_csv(good_segments_file)
    diarization_segments = pd.read_csv(diarization_file)
    
    # Ensure column names are as expected
    good_segments.columns = ['start_time', 'end_time']
    diarization_segments.columns = ['start', 'stop', 'speaker']
    
    # Create a list to store matched segments
    matched_segments = []

    # For each good segment, find overlapping diarization segments
    for _, good_row in good_segments.iterrows():
        good_start = good_row['start_time']
        good_end = good_row['end_time']
        
        # Find diarization segments that overlap with the current good segment
        overlapping_segments = diarization_segments[
            (diarization_segments['stop'] > good_start) & (diarization_segments['start'] < good_end)
        ]
        
        # Extract unique speakers from overlapping segments
        speakers = overlapping_segments['speaker'].unique().tolist()
        
        # Append the merged result to matched_segments
        matched_segments.append({
            'start_time': good_start,
            'end_time': good_end,
            'speakers': ", ".join(speakers)  # Join speakers with a comma if multiple
        })

    # Convert to DataFrame and save
    matched_df = pd.DataFrame(matched_segments)
    matched_df.to_csv(output_file, index=False)
    print(f"Matched segments with speakers saved to {output_file}")

if __name__ == "__main__":
    # Set up argument parser
    parser = argparse.ArgumentParser(description="Match filtered audio segments with speaker diarization info.")
    parser.add_argument("good_segments_file", help="Path to the CSV file with good time segments.")
    parser.add_argument("diarization_file", help="Path to the CSV file with diarization segments and speakers.")
    parser.add_argument("output_file", help="Path to the output CSV file with matched segments.")
    
    # Parse arguments
    args = parser.parse_args()
    
    # Run the matching function
    match_segments_with_speakers(args.good_segments_file, args.diarization_file, args.output_file)
