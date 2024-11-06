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
        
        # For each overlapping segment, create a sub-segment
        for _, diar_row in overlapping_segments.iterrows():
            # Calculate the intersection of the segments
            sub_start = max(good_start, diar_row['start'])
            sub_end = min(good_end, diar_row['stop'])
            
            # Only add if there's a valid intersection
            if sub_end > sub_start:
                matched_segments.append({
                    'start_time': sub_start,
                    'end_time': sub_end,
                    'speaker': diar_row['speaker']
                })

    # Convert to DataFrame and save
    matched_df = pd.DataFrame(matched_segments)
    # Sort by start time and speaker
    matched_df = matched_df.sort_values(['start_time', 'speaker'])
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
