from pyannote.audio import Pipeline
import torch
import os
from dotenv import load_dotenv
from pathlib import Path
import subprocess

### fetch all the .wav audios in the audio folder
### perform speaker diarization and return the speaker id with time stamps in .txt files

def run_pyannote(audio_path = 'audios'):

    # load token: add your huggingface token to .env file
    dotenv_path=os.path.abspath('.env')
    load_dotenv(dotenv_path)
    hugging_face_token = os.getenv('hugging_face_token')
    pipeline = Pipeline.from_pretrained(
        "pyannote/speaker-diarization-3.1",
        use_auth_token=hugging_face_token)

    # send pipeline to GPU (when available)
    print(torch.cuda.is_available())
    pipeline.to(torch.device("cuda"))
    print(torch.device("cuda" if torch.cuda.is_available() else "cpu"))

    base_dir = Path(__file__).resolve().parent
    audio_path = base_dir / audio_path

    audio_list = list(Path(audio_path).glob("*.wav"))

    for audio in audio_list:

        # apply pretrained pipeline
        diarization = pipeline(audio)

        '''
        # print the result
        for turn, _, speaker in diarization.itertracks(yield_label=True):
            print(f"start={turn.start:.1f}s stop={turn.end:.1f}s speaker_{speaker}")
        # start=0.2s stop=1.5s speaker_0
        # start=1.8s stop=3.9s speaker_1
        # start=4.2s stop=5.7s speaker_0
        # ...
        '''
        speaker_output_path = base_dir / "speakers_output"
        output_file = speaker_output_path / (audio.stem + ".txt")

        with open(output_file, "w") as f:
            for turn, _, speaker in diarization.itertracks(yield_label=True):
                f.write(f"start={turn.start:.1f}s stop={turn.end:.1f}s speaker_{speaker}\n")
        print(f"Speaker diarization saved to {output_file}")

if __name__ == "__main__":
    run_pyannote()
