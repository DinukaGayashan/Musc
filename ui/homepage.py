import streamlit as st
from generators import melody_generator


def generate_melody():
    audio_file = melody_generator.generate_music()
    st.audio(audio_file)

def homepage():
    st.title("Musc")
    st.write("""
    music from nowhere
    """)

    if st.button("Generate"):
        generate_melody()
