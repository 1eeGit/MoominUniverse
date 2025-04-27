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
            if os.path.exists(audio_output):
                continue
        except subprocess.CalledProcessError as e:
            print(f"Error extracting audio: {e}")

### cconcatenate video/ audio
def concatenate_files(extension="wav", output_name="final.wav", path = 'audios'):
    base_dir = Path(__file__).resolve().parent
    input_path = base_dir / path
    output_path = base_dir / output_name
    file_list = sorted(input_path.glob(f"*.{extension}")) 
    list_file = base_dir / f"concat_list.txt"

    with open(list_file, "w") as f:
        for file in file_list:
            f.write(f"file '{file.resolve()}'\n") 

    command = [
        "ffmpeg",
        "-f", "concat",
        "-safe", "0",
        "-i", str(list_file),
        "-c", "copy",
        str(output_path)
    ]

    try:
        subprocess.run(command, check=True)
        print("------------------------final file cooked--------------------")
    except subprocess.CalledProcessError as e:
        print(e)   



if __name__ == "__main__":
    # extract_audio()
    # concatenating()
    



    concatenate_files("mp4", "final.mp4", "videos/all")

    '''
duration=53740.202667
ffmpeg -i final.wav -ss 0 -t 17000 -acodec pcm_s16le -ar 22050 -ac 1 1_compressed.wav
ffmpeg -i final.wav -ss 17000 -t 14000 -acodec pcm_s16le -ar 22050 -ac 1 2_compressed.wav
ffmpeg -i final.wav -ss 34000 -acodec pcm_s16le -ar 22050 -ac 1 3_compressed.wav
'''