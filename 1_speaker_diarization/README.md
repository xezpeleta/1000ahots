# Speech diarization

## Introduction

Speech diarization is the process of partitioning an input audio stream into homogeneous segments according to the speaker identity. The goal is to determine "who spoke when" in the audio stream. The output of a diarization system is a set of speaker labels, one for each audio segment.

## Diarization using Pyannote-audio

Pyannote-audio is an open-source toolkit for speaker diarization. It provides a simple interface to train and apply diarization models. The toolkit is built on top of PyTorch and Pyannote-core.

## Installation

To install Pyannote-audio, run the following command:

```bash
pip install -r requirements.txt
```

## Usage

To perform speaker diarization using Pyannote-audio, you can use the following script:

```bash
python3 speaker_diarization.py ../examples/myfile.wav -ot csv
```

This will generate a CSV file on the same directory as the input file. The CSV file will contain the speaker labels for each segment of the audio stream.

## Match speaker diarization with SMAD output

To match the speaker diarization output with the SMAD output, you can use the following script:

```bash
python3 match_voice_speakers_segments.py filtered.csv speakers.csv joined_segments.csv
```