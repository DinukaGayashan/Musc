import streamlit as st
from generators import melody_generator
from models import model

def generate_melody():
    audio_file = melody_generator.generate_music()
    st.audio(audio_file)


def train_models():
    model.train_model()


def homepage():
    st.title("Musc")
    st.write("""
    music from nowhere
    """)

    if st.button("Generate"):
        generate_melody()

    if st.button("Train Models"):
        train_models()
