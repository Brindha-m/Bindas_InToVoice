import streamlit as st
import os
from pydub import AudioSegment
import subprocess

def download_audio_from_youtube(youtube_url, download_path):
    try:
        if not os.path.exists(download_path):
            os.makedirs(download_path)
        command = f'yt-dlp -4 -o "{download_path}/%(title)s.%(ext)s" -x --audio-format mp3 "{youtube_url}"'
        result = subprocess.run(command, shell=True)
        if result.returncode == 0:
            st.success("Download completed!")
            for file in os.listdir(download_path):
                if file.endswith(".mp3"):
                    return os.path.join(download_path, file)
        else:
            st.error(f"Download failed with return code {result.returncode}!")
            return None
    except Exception as e:
        st.error(f"An error occurred during download: {e}")
        return None

def separate_audio(input_file, output_path):
    try:
        if not os.path.exists(output_path):
            os.makedirs(output_path)
        command = f'spleeter separate -p spleeter:5stems -o {output_path} "{input_file}"'
        result = subprocess.run(command, shell=True)
        if result.returncode == 0:
            st.success("Audio separation completed!")
        else:
            st.error(f"Audio separation failed with return code {result.returncode}!")
    except Exception as e:
        st.error(f"An error occurred during separation: {e}")

def convert_wav_to_mp3(wav_path, mp3_path):
    try:
        sound = AudioSegment.from_wav(wav_path)
        sound.export(mp3_path, format="mp3")
        st.success("Conversion to MP3 completed!")
        return mp3_path
    except Exception as e:
        st.error(f"An error occurred during conversion: {e}")
        return None

st.title("YouTube Audio Separator")
st.write("Enter a YouTube URL to download, separate, and play the audio stems.")

# Input field from app
youtube_url = st.text_input("YouTube URL", "https://music.youtube.com/watch?v=BNkIvh6qExw")
download_path = "content"
output_path = "output"

if st.button("Process Audio"):
    downloaded_file = download_audio_from_youtube(youtube_url, download_path)
    
    if downloaded_file:
        separate_audio(downloaded_file, output_path)
        
        song_name = os.path.splitext(os.path.basename(downloaded_file))[0]
        vocals_wav = os.path.join(output_path, song_name, "vocals.wav")
        vocals_mp3 = os.path.join(output_path, song_name, "vocals.mp3")
        
        if os.path.exists(vocals_wav):
            mp3_file = convert_wav_to_mp3(vocals_wav, vocals_mp3)
            if mp3_file and os.path.exists(mp3_file):
                st.write("### Vocals Audio")
                audio_file = open(mp3_file, "rb")
                st.audio(audio_file.read(), format="audio/mp3")
        else:
            st.error("Vocals WAV file not found!")
