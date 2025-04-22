import csv
from pathlib import Path
import re

# Set base directory
base_dir = Path(__file__).resolve().parent

# Input and output folders
input_dir = base_dir / "speakers_output"
output_dir = base_dir / "speakers_csv"
output_dir.mkdir(exist_ok=True)  # Make sure the output directory exists

# Regular expression pattern to match lines
pattern = re.compile(r"start=(\d+\.?\d*)s stop=(\d+\.?\d*)s speaker_(SPEAKER_\d+)")

# Get all .txt files in the input directory
audio_list = list(input_dir.glob("*.txt"))

for audio_file in audio_list:
    data = []

    with open(audio_file, "r") as file:
        for line in file:
            match = pattern.search(line.strip())
            if match:
                start_time = float(match.group(1))
                stop_time = float(match.group(2))
                speaker = match.group(3)
                data.append([start_time, stop_time, speaker])

    output_file = output_dir / (audio_file.stem + ".csv")

    with open(output_file, "w", newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["start", "stop", "speaker"])
        writer.writerows(data)

    print(f"CSV file saved to {output_file}")
