import pandas as pd
from pathlib import Path


base_dir = Path(__file__).resolve().parent
merged_dir = base_dir / "merged"
global_id_path = base_dir / "Global_speaker_ids/global_speaker_ids_0.8.csv"
tuned_assignments_path = base_dir / "matches/matches_0.7.csv"

def match_global_ID(global_id_path, merged_dir):
    global_df = pd.read_csv(global_id_path)

    speaker_to_global = {}
    for _, row in global_df.iterrows():
        global_id = row['Global_ID']
        speaker_ids = [s.strip() for s in row['Speaker_IDs'].split(',')]
        for speaker_id in speaker_ids:
            speaker_to_global[speaker_id] = global_id

    csv_files = list(merged_dir.glob("*.csv"))

    for csv_file in csv_files:
        print(f"Processing file: {csv_file}")
        df = pd.read_csv(csv_file)


        file_index = csv_file.stem.split("_")[0]
        df['Full_Speaker_ID'] = df['Speaker'].apply(lambda x: f"audios/{file_index}_compressed.wav-{x}")

        df['Global_ID'] = df['Full_Speaker_ID'].map(speaker_to_global)

        df.drop(columns=['Full_Speaker_ID'], inplace=True)
        df.to_csv(csv_file, index=False)
        print(f"Updated file saved to {csv_file}")

def match_tuned_assignments():
    tuned_df = pd.read_csv(tuned_assignments_path)

    for _, row in tuned_df.iterrows():
        global_id = row['Global_ID']
        speaker_ids = [s.strip() for s in row['Speaker_IDs'].split(',')]
        for speaker_id in speaker_ids:
            speaker_to_global[speaker_id] = global_id

    return speaker_to_global
