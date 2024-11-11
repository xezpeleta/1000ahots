"""
This script will use Transformers library and fine-tuned Whisper
model to transcribe basque audio files.
"""

import os
import torch
import argparse
from pathlib import Path
from transformers import AutoModelForSpeechSeq2Seq, AutoProcessor, pipeline

def process_audio(pipe, audio_path):
    """Process a single audio file and return its transcription"""
    transcription = pipe(str(audio_path))
    
    results = []
    if "chunks" in transcription:
        current_time = 0.0
        for chunk in transcription["chunks"]:
            if len(chunk["timestamp"]) >= 2:
                chunk_duration = chunk["timestamp"][1] - chunk["timestamp"][0]
                start_time = current_time
                end_time = current_time + chunk_duration
                current_time = end_time
                text = chunk["text"]
                results.append(f"{start_time:.2f}, {end_time:.2f}, {text}")
    else:
        results.append(f"0, 0, {transcription['text']}")
    
    return results

def main():
    # Parse arguments
    parser = argparse.ArgumentParser(description='Transcribe audio files using Whisper model.')
    parser.add_argument('input', type=str, help='Input audio file or directory')
    args = parser.parse_args()

    device = "cuda:0" if torch.cuda.is_available() else "cpu"
    torch_dtype = torch.float16 if torch.cuda.is_available() else torch.float32

    # Load model
    model_name_or_path = "xezpeleta/whisper-medium-eu"
    processor = AutoProcessor.from_pretrained(model_name_or_path)
    model = AutoModelForSpeechSeq2Seq.from_pretrained(
        model_name_or_path,
        torch_dtype=torch_dtype,
        low_cpu_mem_usage=True,
    )
    model.to(device)

    # Init pipeline
    pipe = pipeline(
        "automatic-speech-recognition",
        model=model,
        feature_extractor=processor.feature_extractor,
        tokenizer=processor.tokenizer,
        torch_dtype=torch_dtype,
        device=device,
        # chunk_length_s=30,  # for long-form transcription
        max_new_tokens=128,
        return_timestamps=True,
        generate_kwargs={"language":"basque"},
    )

    # Process input path
    input_path = Path(args.input)
    if input_path.is_file():
        # Process single file
        results = process_audio(pipe, input_path)
        for line in results:
            print(line)
    elif input_path.is_dir():
        # Process all audio files in directory
        for audio_file in input_path.glob('*.wav'):  # Add more extensions if needed
            print(f"\nProcessing {audio_file}:")
            results = process_audio(pipe, audio_file)
            for line in results:
                print(line)
    else:
        print(f"Error: {args.input} is not a valid file or directory")

if __name__ == "__main__":
    main()