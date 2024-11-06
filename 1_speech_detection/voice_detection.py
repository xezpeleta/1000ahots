import argparse
from pyannote.audio import Pipeline
from pyannote.core import Segment

def voice_detection(input_file):
    # Load the pre-trained voice activity detection model
    pipeline = Pipeline.from_pretrained("pyannote/voice-activity-detection")

    # Apply the pipeline to your audio file
    audio_file = input_file
    vad_result = pipeline(audio_file)

    # Post-process to keep only segments marked as voice
    voice_segments = []
    for segment, track, label in vad_result.itertracks(yield_label=True):
        if label == "SPEECH":  # or other label if you train a specific model
            voice_segments.append(segment)

    # voice_segments now contains only speech segments without background noise
    for segment in voice_segments:
        print(segment.start, segment.end)  # Start and end times for each voice-only segment


if __name__ == "__main__":
    # Parse arguments
    parser = argparse.ArgumentParser(description="Voice detection")
    parser.add_argument("input", help="Input audio file")
    args = parser.parse_args()
    input_file = args.input

    # Run voice detection
    voice_detection(input_file)