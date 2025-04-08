import streamlit as st
import os
from pydub import AudioSegment
import ffmpeg  # Make sure this is ffmpeg-python
import subprocess

def download_audio_from_youtube(youtube_url, download_path):
    try:
        if not os.path.exists(download_path):
            os.makedirs(download_path)
        # Using a sanitized filename pattern
        command = f'yt-dlp -o "{download_path}/%(title)s.%(ext)s" -x --audio-format mp3 --merge-output-format mp3 "{youtube_url}"'
        result = subprocess.run(command, shell=True, capture_output=True, text=True)
        
        if result.returncode == 0:
            st.success("Download completed!")
            downloaded_files = [f for f in os.listdir(download_path) if f.endswith(".mp3")]
            if downloaded_files:
                original_file = os.path.join(download_path, downloaded_files[0])
                # Replace spaces and special characters
                sanitized_name = "".join(c if c.isalnum() else "_" for c in downloaded_files[0])
                new_file_path = os.path.join(download_path, sanitized_name)
                
                if original_file != new_file_path:
                    os.rename(original_file, new_file_path)
                return new_file_path
            return None
        else:
            st.error(f"Download failed: {result.stderr}")
            return None
    except Exception as e:
        st.error(f"An error occurred during download: {e}")
        return None

def separate_audio(input_file, output_path):
    try:
        if not os.path.exists(output_path):
            os.makedirs(output_path)
        # Ensure the input file path is properly quoted
        command = f'spleeter separate -p spleeter:5stems -o "{output_path}" "{input_file}"'
        result = subprocess.run(command, shell=True, capture_output=True, text=True)
        if result.returncode == 0:
            st.success("Audio separation completed!")
        else:
            st.error(f"Audio separation failed: {result.stderr}")
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
