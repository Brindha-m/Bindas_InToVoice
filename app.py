import streamlit as st
import os
from pydub import AudioSegment

# Function to download audio from YouTube
def download_audio_from_youtube(youtube_url, download_path):
    try:
        if not os.path.exists(download_path):
            os.makedirs(download_path)
        command = f'yt-dlp -o "{download_path}/%(title)s.%(ext)s" -x --audio-format mp3 "{youtube_url}"'
        result = os.system(command)
        if result == 0:
            st.success("Download completed!")
            # Find the downloaded file
            for file in os.listdir(download_path):
                if file.endswith(".mp3"):
                    return os.path.join(download_path, file)
        else:
            st.error("Download failed!")
            return None
    except Exception as e:
        st.error(f"An error occurred during download: {e}")
        return None

# Function to separate audio using spleeter
def separate_audio(input_file, output_path):
    try:
        if not os.path.exists(output_path):
            os.makedirs(output_path)
        command = f'spleeter separate -p spleeter:5stems -o {output_path} "{input_file}"'
        result = os.system(command)
        if result == 0:
            st.success("Audio separation completed!")
        else:
            st.error("Audio separation failed!")
    except Exception as e:
        st.error(f"An error occurred during separation: {e}")

# Function to convert WAV to MP3
def convert_wav_to_mp3(wav_path, mp3_path):
    try:
        sound = AudioSegment.from_wav(wav_path)
        sound.export(mp3_path, format="mp3")
        st.success("Conversion to MP3 completed!")
        return mp3_path
    except Exception as e:
        st.error(f"An error occurred during conversion: {e}")
        return None

# Streamlit UI
st.title("YouTube Audio Separator")
st.write("Enter a YouTube URL to download, separate, and play the audio stems.")

# Input field for YouTube URL
youtube_url = st.text_input("YouTube URL", "https://music.youtube.com/watch?v=BNkIvh6qExw")
download_path = "content"
output_path = "output"

# Button to start processing
if st.button("Process Audio"):
    # Step 1: Download the audio
    downloaded_file = download_audio_from_youtube(youtube_url, download_path)
    
    if downloaded_file:
        # Step 2: Separate the audio
        separate_audio(downloaded_file, output_path)
        
        # Step 3: Convert vocals to MP3 and make it playable
        song_name = os.path.splitext(os.path.basename(downloaded_file))[0]
        vocals_wav = os.path.join(output_path, song_name, "vocals.wav")
        vocals_mp3 = os.path.join(output_path, song_name, "vocals.mp3")
        
        if os.path.exists(vocals_wav):
            mp3_file = convert_wav_to_mp3(vocals_wav, vocals_mp3)
            if mp3_file and os.path.exists(mp3_file):
                # Display playable audio
                st.write("### Vocals Audio")
                audio_file = open(mp3_file, "rb")
                st.audio(audio_file.read(), format="audio/mp3")
        else:
            st.error("Vocals WAV file not found!")

# Display instructions
st.write("Note: The app downloads the audio, separates it into 5 stems, converts the vocals to MP3, and plays it.")
