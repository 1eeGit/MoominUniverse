import csv
from pathlib import Path
import re
import pandas as pd
from datetime import datetime, timedelta

base_dir = Path(__file__).resolve().parent

def convert_speaker_csv():
    input_dir = base_dir / "speakers_output/compressed"
    output_dir = base_dir / "speakers_csv"
    output_dir.mkdir(exist_ok=True)

    pattern = re.compile(r"start=(\d+\.?\d*)s stop=(\d+\.?\d*)s speaker_(SPEAKER_\d+)")
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

def convert_sub_csv():
    srt_path = base_dir / "subtitles/compressed"
    csv_path = base_dir / "subtitles/csv"
    csv_path.mkdir(exist_ok=True)

    sub_list = list(srt_path.glob("*.srt"))

    for srt_file in sub_list:
        csv_file_path = csv_path / (srt_file.stem + "_sub.csv")

        with open(srt_file, 'r', encoding='utf-8') as f:
            content = f.read()

        entries = content.strip().split('\n\n')
        rows = []

        for entry in entries:
            lines = entry.strip().split('\n')
            if len(lines) >= 3:
                index = lines[0].strip()
                times = lines[1].strip()
                text = ' '.join(lines[2:]).strip()

                match = re.match(r"(\d{2}:\d{2}:\d{2},\d{3}) --> (\d{2}:\d{2}:\d{2},\d{3})", times)
                if match:
                    start, end = match.groups()
                    rows.append([index, start, end, text])

        with open(csv_file_path, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(['Index', 'Start', 'End', 'Text'])
            writer.writerows(rows)

        print(f"Saved CSV to {csv_file_path}")

def to_sec(t_str):
    
    try:
        dt = datetime.strptime(t_str, "%H:%M:%S,%f")
        return dt.hour * 3600 + dt.minute * 60 + dt.second + dt.microsecond / 1e6
    except ValueError as e:
        print(f"Error parsing time string '{t_str}': {e}")
        return 0.0

def to_srt_time(seconds):
    """Convert seconds to SRT time format (HH:MM:SS,mmm)."""
    td = timedelta(seconds=seconds)
    total_seconds = int(td.total_seconds())
    hours, remainder = divmod(total_seconds, 3600)
    minutes, secs = divmod(remainder, 60)
    milliseconds = int((td.total_seconds() - total_seconds) * 1000)
    return f"{hours:02}:{minutes:02}:{secs:02},{milliseconds:03}"

def merge_speaker_and_subtitle(speaker_csv_path, subtitle_csv_path, output_path):
    speaker_df = pd.read_csv(speaker_csv_path)
    subtitle_df = pd.read_csv(subtitle_csv_path)

    merged_rows = []

    for _, s_row in speaker_df.iterrows():
        speaker_start = s_row['start']
        speaker_stop = s_row['stop']

        for _, sub_row in subtitle_df.iterrows():
            sub_start = sub_row['Start']
            sub_end = sub_row['End']

            sub_start_sec = to_sec(sub_start)
            sub_end_sec = to_sec(sub_end)

            if sub_start_sec <= speaker_start <= sub_end_sec:
                merged_rows.append({
                    "Speaker_Start": to_srt_time(speaker_start),
                    "Speaker_Stop": to_srt_time(speaker_stop),
                    "Speaker": s_row['speaker'],
                    "Subtitle_Start": sub_start,
                    "Subtitle_End": sub_end,
                    "Text": sub_row['Text']
                })
                break

    merged_df = pd.DataFrame(merged_rows)
    merged_df.to_csv(output_path, index=False)
    print(f"Merged CSV saved to {output_path}")

if __name__ == "__main__":
    
    # convert_speaker_csv()
    # convert_sub_csv()

    for i in range(1, 4):
        speaker_csv = base_dir / f"speakers_csv/{i}_compressed.csv"
        subtitle_csv = base_dir / f"subtitles/csv/{i}_compressed_sub.csv"
        output_csv = base_dir / f"merged/{i}_merged.csv"

        Path(output_csv.parent).mkdir(parents=True, exist_ok=True)
        merge_speaker_and_subtitle(speaker_csv, subtitle_csv, output_csv)
