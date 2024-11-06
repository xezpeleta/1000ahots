# Speech detection and speaker diarization

This is a simple example of how to use the `speech_detection` and `speaker_diarization` modules using Pyannote.

## Installation

Install the required dependencies:

```bash
pip install -r requirements.txt
```

## Usage

To run the example, simply execute the following command:

```bash
python speech_detection.py <audio_file>
```

Example output:

```
start=0.5s stop=1.0s speaker=SPEAKER_06
start=23.8s stop=60.8s speaker=SPEAKER_07
start=66.3s stop=73.9s speaker=SPEAKER_07
start=74.4s stop=84.7s speaker=SPEAKER_07
start=86.9s stop=94.9s speaker=SPEAKER_07
start=95.8s stop=103.3s speaker=SPEAKER_07
start=103.9s stop=110.7s speaker=SPEAKER_07
start=111.7s stop=123.6s speaker=SPEAKER_07
start=124.9s stop=134.5s speaker=SPEAKER_07
```

Parameters:

- `-ot` | `--output-type`: Output type. Default: text. Choices: text, csv.

## Matching the output with the SMAD output file

The SMAD tool can generate a CSV file with start and end times of each speech segment. To match the output of this script with the SMAD output file, you can use the following command:

```bash
python3 match_speech_segments.py <smad_segments_file> <diarization_output_file> <output_file>
```

The above command will generate a new file with the matched segments.

Example:

```csv
start_time,end_time,speakers
24.384, 59.904, SPEAKER_07
200.064, 212.736, SPEAKER_07
213.312, 220.8, SPEAKER_05
221.376, 222.528, SPEAKER_05
223.104, 226.56, SPEAKER_05
227.136, 238.08, SPEAKER_05
239.232, 243.456, SPEAKER_05
244.032, 253.056, SPEAKER_06
253.632, 270.144, SPEAKER_05
275.52, 276.672, SPEAKER_07
279.168, 286.464, SPEAKER_05
287.04, 288.96, SPEAKER_05
```