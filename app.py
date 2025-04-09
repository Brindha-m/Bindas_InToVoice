import streamlit as st
import os
from scipy.io.wavfile import write
import demucs.separate
from pydub import AudioSegment

# Function for Demucs separation
def separate_audio(audio):
    try:
        os.makedirs("out", exist_ok=True)
        write('test.wav', audio[0], audio[1])
        demucs.separate.main(["-n", "htdemucs", "--two-stems=vocals", "test.wav", "-o", "out"])
        return "./out/htdemucs/test/vocals.wav", "./out/htdemucs/test/no_vocals.wav"
    except Exception as e:
        st.error(f"An error occurred during separation: {e}")
        return None, None

# Streamlit app
st.title("Demucs Music Source Separation (v4)")
st.markdown("<p style='text-align: center'><a href='https://arxiv.org/abs/1911.13254' target='_blank'>Music Source Separation in the Waveform Domain</a> | <a href='https://github.com/facebookresearch/demucs' target='_blank'>Github Repo</a> | <a href='https://www.thafx.com' target='_blank'>//THAFX</a></p>", unsafe_allow_html=True)

# Add Hugging Face's logo
st.image("https://huggingface.co/front/assets/huggingface_logo.svg", width=200)

# File uploader
uploaded_file = st.file_uploader("Upload an audio file", type=["wav", "mp3"])

if uploaded_file is not None:
    audio = AudioSegment.from_file(uploaded_file)
    audio_array = audio.get_array_of_samples()
    sample_rate = audio.frame_rate
    
    # Separate audio
    vocals_wav, no_vocals_wav = separate_audio((sample_rate, audio_array))
    
    if vocals_wav and no_vocals_wav:
        st.success("Audio separation completed!")
        st.audio(vocals_wav, format="audio/wav", start_time=0)
        st.audio(no_vocals_wav, format="audio/wav", start_time=0)
    else:
        st.error("Audio separation failed!")
