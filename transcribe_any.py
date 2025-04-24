
from transcribe_anything import transcribe_anything
import os
from dotenv import load_dotenv
from pathlib import Path
import subprocess
import torch

### transcribe all the audio files as .json with speaker and subtitles
### for me the env has error....
def run_transcribe_insane(audio_path = 'audios'):
    dotenv_path=os.path.abspath('.env')
    load_dotenv(dotenv_path)
    hugging_face_token = os.getenv('hugging_face_token')
    
    base_dir = Path(__file__).resolve().parent
    audio_path = base_dir / audio_path
    audio_list = list(Path(audio_path).glob("*.wav"))
    output_dir = base_dir / "subtitlesinsane"
    output_dir.mkdir(parents=True, exist_ok=True)

    for audio in audio_list:
        
        transcribe_anything(
            url_or_file= str(audio),
            output_dir=output_dir,
            task="transcribe",
            language="en",
            model="base",
            device="insane",
            hugging_face_token=hugging_face_token
        )
        
        for ext in ['json', 'srt', 'tsv', 'txt', 'vtt']:
            original = output_dir / f"out.{ext}"
            new = output_dir / f"{audio.stem}.{ext}"
            if original.exists():
                original.rename(new)
'''
# Full function signiture:
def transcribe(
    url_or_file: str,
    output_dir: Optional[str] = None,
    model: Optional[str] = None,              # tiny,small,medium,large
    task: Optional[str] = None,               # transcribe or translate
    language: Optional[str] = None,           # auto detected if none, "en" for english...
    device: Optional[str] = None,             # cuda,cpu,insane,mps
    embed: bool = False,                      # Produces a video.mp4 with the subtitles burned in.
    hugging_face_token: Optional[str] = None, # If you want a speaker.json
    other_args: Optional[list[str]] = None,   # Other args to be passed to to the whisper backend
) -> str:
        pass

'''


def run_transcribe_normal(audio_path = 'audios'):
    dotenv_path=os.path.abspath('.env')
    load_dotenv(dotenv_path)
    
    base_dir = Path(__file__).resolve().parent
    audio_path = base_dir / audio_path
    audio_list = list(Path(audio_path).glob("*.wav"))
    output_dir = base_dir / "subtitles"

    for audio in audio_list:
        
        transcribe_anything(
            url_or_file= str(audio),
            output_dir=str(output_dir),
            task="transcribe",
            language="en",
            model="base",  # tiny model error: AssertionError: No srt file found.
            device="cpu",
        )
        

        ### rename the subtitles or will be overwritten
        for ext in ['json', 'srt', 'tsv', 'txt', 'vtt']:
            original = output_dir / f"out.{ext}"
            new = output_dir / f"{audio.stem}.{ext}"
            if original.exists():
                original.rename(new)



if __name__ == "__main__":
    run_transcribe_insane()
    #run_transcribe_normal()