"""
Use pyannote to obtain speech detection and diarization results
"""

import argparse
from pyannote.audio import Pipeline


def speech_detection(input_file, output_type="text"):
    pipeline = Pipeline.from_pretrained(
        "pyannote/speaker-diarization-3.1",
        use_auth_token="")

    # send pipeline to GPU (when available)
    import torch
    pipeline.to(torch.device("cuda"))

    # apply pretrained pipeline
    diarization = pipeline(input_file)

    if output_type == "csv":
        extension = input_file.split(".")[-1]
        csv_file_path = input_file.replace(f".{extension}", ".csv")
        with open(csv_file_path, "w") as f:
            f.write("start, stop, speaker\n")

    # print the result
    for turn, _, speaker in diarization.itertracks(yield_label=True):
        if output_type == "text":
            print(f"start={turn.start:.1f}s stop={turn.end:.1f}s speaker={speaker}")
        elif output_type == "csv":
            with open(csv_file_path, "a") as f:
                f.write(f"{turn.start:.1f}, {turn.end:.1f}, {speaker}\n")


if __name__ == "__main__":
    # Parse arguments
    parser = argparse.ArgumentParser(description="Speech detection and diarization")
    parser.add_argument("input", help="Input audio file")
    parser.add_argument("-ot", "--output-type", help="Output type (text or csv)", default="text")
    args = parser.parse_args()
    input_file = args.input
    output_type = args.output_type

    # Run speech detection
    speech_detection(input_file, output_type)
