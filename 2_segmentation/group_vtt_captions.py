import argparse
import webvtt
from datetime import timedelta

def vtt_time_to_timedelta(vtt_time):
    hours, minutes, seconds = vtt_time.split(':')
    seconds, milliseconds = seconds.split('.')
    return timedelta(hours=int(hours), minutes=int(minutes), seconds=int(seconds), milliseconds=int(milliseconds))

def timedelta_to_vtt_time(td):
    hours, remainder = divmod(td.total_seconds(), 3600)
    minutes, seconds = divmod(remainder, 60)
    milliseconds = int((seconds % 1) * 1000)
    return f"{int(hours):02}:{int(minutes):02}:{int(seconds):02}.{milliseconds:03}"

def group_vtt_captions(input_vtt, output_vtt, min_duration=7, max_duration=18):
    grouped_captions = []
    current_group = []
    group_start = None
    group_duration = timedelta()

    for caption in webvtt.read(input_vtt):
        caption_duration = vtt_time_to_timedelta(caption.end) - vtt_time_to_timedelta(caption.start)
        
        if not group_start:
            group_start = caption.start

        # Check if adding the caption exceeds max duration
        if group_duration + caption_duration > timedelta(seconds=max_duration):
            # Only finalize group if it meets minimum duration
            if group_duration >= timedelta(seconds=min_duration):
                grouped_captions.append({
                    'start': group_start,
                    'end': current_group[-1].end,
                    'text': ' '.join([c.text for c in current_group])
                })
                # Reset for new group
                current_group = [caption]  # Start new group with current caption
                group_start = caption.start
                group_duration = caption_duration
            else:
                # If min duration not met, keep current group and continue adding
                current_group.append(caption)
                group_duration += caption_duration
            continue

        # Add caption to the current group
        current_group.append(caption)
        group_duration += caption_duration

    # Add the last group if it meets minimum duration
    if current_group and group_duration >= timedelta(seconds=min_duration):
        grouped_captions.append({
            'start': group_start,
            'end': current_group[-1].end,
            'text': ' '.join([c.text for c in current_group])
        })

    # Create WebVTT object directly without context manager
    vtt = webvtt.WebVTT()
    for group in grouped_captions:
        caption = webvtt.Caption(
            start=group['start'],
            end=group['end'],
            text=group['text']
        )
        vtt.captions.append(caption)
    vtt.save(output_vtt)

    return grouped_captions


if __name__ == "__main__":
    # Parse arguments
    parser = argparse.ArgumentParser(description="Group VTT captions")
    parser.add_argument("input", help="Input VTT file")
    parser.add_argument("output", help="Output VTT file")
    parser.add_argument("--min_duration", type=int, default=5, help="Minimum duration for each group")
    parser.add_argument("--max_duration", type=int, default=10, help="Maximum duration for each group")
    args = parser.parse_args()


    input_vtt = args.input
    output_vtt = args.output
    group_vtt_captions(input_vtt, output_vtt, max_duration=10)
