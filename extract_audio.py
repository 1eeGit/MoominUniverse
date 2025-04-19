import os
from pathlib import Path
import subprocess

### fetch all the .mp4 videos in the video folder
### extract the audios from the videos to audio folder
def extract_audio(video_path = 'videos', audio_path = 'audios'):

    base_dir = Path(__file__).resolve().parent
    video_path = base_dir / video_path
    audio_path = base_dir / audio_path
    audio_path.mkdir(parents=True, exist_ok=True)

    video_list = list(Path(video_path).glob("*.mp4"))

    for video in video_list:
        audio_output = audio_path / (video.stem + ".wav")
        command = [
            "ffmpeg",
            "-i", str(video),
            "-vn",  
            "-acodec", 
            "pcm_s16le", # wav
            audio_output
        ]
        try:
            subprocess.run(command, check=True)
            audio_list = list(Path(audio_path).glob("*.wav"))
            print(f"Audio extracted to {audio_path},n {audio_list} \n")
        except subprocess.CalledProcessError as e:
            print(f"Error extracting audio: {e}")


    


if __name__ == "__main__":
    extract_audio()