import streamlit as st
from generators import melody_generator


def generate_melody():
    audio_file = melody_generator.generate_music()
    st.audio(audio_file)


def music_page():
    if st.button("Generate"):
        with st.spinner('Hold on for a new melody'):
            generate_melody()
