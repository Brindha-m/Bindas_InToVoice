import os
import streamlit as st
from scipy.io.wavfile import write
import tempfile
import torchaudio
from demucs import separate

st.title("🎵 Demucs Music Source Separation (v4)")
st.markdown(
    """
    <p style='text-align: center'>
        <a href='https://arxiv.org/abs/1911.13254' target='_blank'>Music Source Separation in the Waveform Domain</a> |
        <a href='https://github.com/facebookresearch/demucs' target='_blank'>GitHub Repo</a> |
        <a href='https://www.thafx.com' target='_blank'>//THAFX</a>
    </p>
    """,
    unsafe_allow_html=True
)

uploaded_audio = st.file_uploader("Upload audio file (WAV, MP3, etc.)", type=["wav", "mp3", "flac"])

if uploaded_audio is not None:
    with tempfile.TemporaryDirectory() as tmpdir:
        input_path = os.path.join(tmpdir, "input_audio.wav")
        output_path = os.path.join(tmpdir, "out")

        # Save uploaded audio to file
        with open(input_path, "wb") as f:
            f.write(uploaded_audio.read())

        st.info("Separating audio, please wait...")

        # Call Demucs via command line or internal API
        separate.main([
            "-n", "htdemucs", 
            "--two-stems=vocals", 
            input_path,
            "-o", output_path
        ])

        vocals_path = os.path.join(output_path, "htdemucs", "input_audio", "vocals.wav")
        no_vocals_path = os.path.join(output_path, "htdemucs", "input_audio", "no_vocals.wav")

        st.success("Separation complete!")

        st.audio(vocals_path, format="audio/wav", start_time=0)
        st.audio(no_vocals_path, format="audio/wav", start_time=0)

        st.download_button("Download Vocals", open(vocals_path, "rb"), file_name="vocals.wav")
        st.download_button("Download No Vocals", open(no_vocals_path, "rb"), file_name="no_vocals.wav")
