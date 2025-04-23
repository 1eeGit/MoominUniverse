'''
Code changed from: 
https://medium.com/@sapkotabinit2002/speaker-identification-and-clustering-using-pyannote-dbscan-and-cosine-similarity-dfa08b5b2a24
'''


import os
import torch
import torchaudio
import numpy as np
from pyannote.audio import Pipeline, Model, Inference
from sklearn.cluster import DBSCAN
from sklearn.metrics.pairwise import cosine_distances
import warnings
from dotenv import load_dotenv
import csv

warnings.filterwarnings("ignore")



device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
print(f"The device that you are using is {device}")

# diarization and embedding models
print("Initializing diarization pipeline...")

load_dotenv()
HUGGINGFACE_TOKEN = os.getenv('hugging_face_token')
diarization_pipeline = Pipeline.from_pretrained(
    "pyannote/speaker-diarization-3.1",
    use_auth_token=HUGGINGFACE_TOKEN).to(device)

print("Initializing embedding model...")
embedding_model = Inference(
    Model.from_pretrained("pyannote/embedding", use_auth_token=HUGGINGFACE_TOKEN).to(device),
    window="whole"
)

print("Diarization and embedding models initialized")

def extract_speaker_embeddings(audio_files, save_path="embeddings.npz"):
    all_embeddings = []
    speaker_info = []

    for audio_file in audio_files:
        print(f"Processing file: {audio_file}")
        waveform, sample_rate = torchaudio.load(audio_file)
        waveform = waveform.to(device)
        print(f"Loaded waveform with shape: {waveform.shape}, sample_rate: {sample_rate}")

        diarization = diarization_pipeline({"waveform": waveform, "sample_rate": sample_rate})
        print("Speaker diarization completed.")

        for turn, _, speaker_label in diarization.itertracks(yield_label=True):

            start_time = turn.start
            end_time = turn.end
            duration = end_time - start_time

            # Skip segments shorter than 1 second
            if duration < 1.0:
               continue

            start_idx = int(start_time * sample_rate)
            end_idx = int(end_time * sample_rate)
            segment = waveform[:, start_idx:end_idx]

            # Move segment to CPU if necessary
            segment = segment.cpu()

            # Extract embedding
            embedding = embedding_model({"waveform": segment, "sample_rate": sample_rate})
            if not isinstance(embedding, np.ndarray):
                embedding = embedding.numpy()

            # Normalize the embedding
            embedding = embedding / np.linalg.norm(embedding)

            all_embeddings.append(embedding)
            speaker_info.append({
                "audio_file": audio_file,
                "local_speaker_label": speaker_label,
                "embedding": embedding
            })

            print(f"Extracted embedding for speaker {speaker_label} from {start_time:.2f}s to {end_time:.2f}s.")

    np.savez_compressed(save_path, embeddings=all_embeddings, speaker_info=speaker_info)
    print(f"Saved embeddings and speaker info to {save_path}")

    return all_embeddings, speaker_info


def load_embeddings(save_path="embeddings.npz"):
    data = np.load(save_path, allow_pickle=True)
    all_embeddings = data['embeddings']
    speaker_info = data['speaker_info']
    print(f"Loaded embeddings and speaker info from {save_path}")
    return all_embeddings, speaker_info


def compute_similarity_matrix(embeddings):
    embeddings_array = np.vstack(embeddings)
    cosine_sim_matrix = 1 - cosine_distances(embeddings_array)
    print("Computed cosine similarity matrix.")
    return cosine_sim_matrix

def cluster_speaker(embeddings):
    embeddings_array = np.vstack(embeddings)
    cosine_sim_matrix = 1 - cosine_distances(embeddings_array)
    distance_matrix = 1 - cosine_sim_matrix

    clustering = DBSCAN(eps=0.8, min_samples=2, metric="precomputed")
    clustering.fit(distance_matrix)
    labels = clustering.labels_

    print(f"Clustering completed. Number of clusters found: {len(set(labels)) - (1 if -1 in labels else 0)}")

    return labels


def assign_global_speaker_ids(labels, speaker_info):
    speaker_mapping = {}
    for idx, info in enumerate(speaker_info):
        key = (info["audio_file"], info["local_speaker_label"])
        cluster_label = labels[idx]
        if cluster_label == -1:
            continue
        if key not in speaker_mapping:
            speaker_mapping[key] = cluster_label
    return speaker_mapping

def find_top_similar_embeddings(cosine_sim_matrix, top_n=10):
    top_similar_indices = []

    for idx, row in enumerate(cosine_sim_matrix):
        row_copy = row.copy()
        row_copy[idx] = -1  # Exclude self-similarity
        top_n_indices = np.argsort(row_copy)[-top_n:]  # Get indices of top_n most similar
        top_similar_indices.append(top_n_indices)

    return top_similar_indices


def process_multiple_audio_files_with_similarity(audio_files, save_path="embeddings.npz"):
    all_embeddings, speaker_info = extract_speaker_embeddings(audio_files, save_path=save_path)
    cosine_sim_matrix = compute_similarity_matrix(all_embeddings)
    top_similar_indices = find_top_similar_embeddings(cosine_sim_matrix, top_n=10)

    matches = []
    for idx, top_n_indices in enumerate(top_similar_indices):
        source = speaker_info[idx]
        print(f"Top 10 similar embeddings for speaker {source['local_speaker_label']} in {os.path.basename(source['audio_file'])}")
        for i in top_n_indices:
            sim_score = cosine_sim_matrix[idx][i]
            target = speaker_info[i]
            print(f"   --> Similar to {target['local_speaker_label']} in {os.path.basename(target['audio_file'])}, Similarity: {sim_score:.4f}")
            matches.append([
                os.path.basename(source['audio_file']),
                source['local_speaker_label'],
                os.path.basename(target['audio_file']),
                target['local_speaker_label'],
                f"{sim_score:.4f}"
            ])

    labels = cluster_speaker(all_embeddings)
    speaker_mapping = assign_global_speaker_ids(labels, speaker_info)

    with open("clustered_speakers.csv", "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["File", "Speaker", "Matched_File", "Matched_Speaker", "Similarity"])
        for row in matches:
            writer.writerow(row)

    print("Processing complete.")


if __name__ == "__main__":
    test_audio = ["audios/test/MOOMIN_01_Spring_in_Moomin_Valley.wav"]
    audio_files = [
        "audios/1_compressed.wav",
        "audios/2_compressed.wav",
        "audios/3_compressed.wav"
    ]

    save_path = "embeddings.npz"

    # process_multiple_audio_files_with_similarity(test_audio, save_path)
    # -> test_clustered_speakers.csv, test_embeddings.npz
    process_multiple_audio_files_with_similarity(audio_files, save_path)
