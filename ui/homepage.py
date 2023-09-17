import streamlit as st
from streamlit_option_menu import option_menu
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

    with st.sidebar:
        selected=option_menu(
            menu_title=None,
            options=["Music", "Models"],
            icons=["music-note-beamed","cpu"]
        )

    if selected=="Music":
        if st.button("Generate"):
            with st.spinner('Hold on for a new melody'):
                generate_melody()

    if selected=="Models":
        if st.button("Train Models"):
            with st.spinner('Hold on for a new model'):
                train_models()
