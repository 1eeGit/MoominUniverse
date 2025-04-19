# Analysis workflow

## Clone repo and prepare env

<pre lang="md"> 
git clone https://github.com/1eeGit/MoominUniverse.git

cd MoominUniverse

mkdir videos  

conda create -n your-new-env python=3.11

conda activate your-new-env

pip install -r requirements.txt

### install the pkgs used in Data Preparation section

python extract_audio.py

### try if 'run_transcribe_insane' in trancibe_any.py works first
python trancibe_any.py    

### else run run_transcribe_normal in in trancibe_any.py then next line
python pyannote.py        


----------------------- structure ------------------------
MoominUniverse/
├── videos/            # .mp4 videos
├── audios/            # .wav audio files
├── subtitles/         # .srt, .txt subtitles, Whisper transcription output
├── speakers_output/   # .txt speaker ids, Pyannote diarization output
├── soups/             # related output from beautiful soup
├── .env      
├── requirements.txt     
└── ...

</pre>

## Resources

### Moomin Season 1 (ep 01-39):

- ep 01-14: https://archive.org/download/moomin-season-1/%5BMoomin%20Master%5D%20Moomin%20season%201/

- ep 15-26: https://archive.org/download/moomin-season-2/%5BMoomin%20Master%5D%20Moomin%20Season%202/

- ep 27-39: https://archive.org/download/moomin-season-3/%5BMoomin%20Master%5D%20Moomin%20season%203/

The following analysis uses the *.mp4* files, for it takes less storage, the videos are saved in `videos` folder.

### Web scrape script to download all .mp4 videos

Beautiful Soup: https://www.crummy.com/software/BeautifulSoup/bs4/doc/#quick-start

<pre lang="md"> 
pip install beautifulsoup4
pip install lxml
pip install html5lib

python scarpe.py  ### download all the link in links.txt

</pre>




##  Data preparation


### Extraxt .wav file from the .mp4 video

- Install FFmpeg: 

    `conda install conda-forge::ffmpeg`

    FFmpeg: https://github.com/FFmpeg/FFmpeg

- Audio outputs are saved in `audios` folder.

### Transcribe the subtitles

Transcribe-anything with `--device insane` mode will generate automatically `.json` file that matches the subtitles with the speaker.

transcribe-anything: https://github.com/zackees/transcribe-anything

*In the `--device insane` mode, transcribe-anything can use pyannote directly and combine the speaker ids with the subtitles time stamp transcribed by whisper, so we can ignore the following part for now, if it works.* 

### Annotate the speakers

The open and free Moomin cartoon resource we use here doesn't come with English subtitles, although there are translations on the internet, here we use **pyannote-audio** package to run the subtitles, and speaker ids for the integrity.

In this workflow we shall only test with the ep 01-03.

- Install pyannote-audio:

    `pip install pyannote.audio`

    Try this line if it reports error related with sentencepiece:

    `conda install -c conda-forge sentencepiece`

    pyannote-audio: https://github.com/pyannote/pyannote-audio

- generate hugging face token with the `read` access for downloading the pre-trained model.
    
    > Accept [pyannote/segmentation-3.0](https://hf.co/pyannote/segmentation-3.0) user conditions

    > Accept [pyannote/speaker-diarization-3.1](https://hf.co/pyannote/speaker-diarization-3.1) user conditions

    > Create access token at [hf.co/settings/tokens](https://huggingface.co/settings/tokens).

    ***If it reports error:*** 

    *'Could not download 'pyannote/speaker-diarization-3.1' pipeline.It might be because the pipeline is private or gated so make sure to authenticate. Visit https://hf.co/settings/tokens to create your access token and retry with:*

    ***Then try also accept these two conditions***
    https://huggingface.co/pyannote/segmentation-3.0
    https://huggingface.co/pyannote/speaker-diarization-3.1

   

## Analysis 

### Semantic and emotional analysis

?maybe use some ready dictionary to analyze (TBD)

### Build the Moomin network

**Nodes**: Moomin characters
- Name list: ... (TBD)

**Edges**: interactions between the characters 
- categories: i.e. close, like, dislike, angry? ... (TBD)
