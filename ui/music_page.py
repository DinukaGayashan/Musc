import streamlit as st

from models import melody_generator
from ui import utility


def generate_melody(model, duration, tempo, temperature):
    audio_file = melody_generator.generate_music(
        model, duration, tempo, temperature)
    st.audio(audio_file)
    st.success(
        f"Successfully generated a melody of {duration} seconds with {model} model with tempo of {tempo}x and "
        f"temperature of {temperature}.")


def music_page():
    with st.container():
        st.title("Melody")
        st.caption(
            "Generate musical melodies with custom requirements. Customize the options and generate melody.")
        st.divider()
    with st.container():
        st.subheader("Options")
        left_col, right_col = st.columns([1, 1])
        with left_col.container():
            model_names = utility.get_model_names()
            model = st.radio("Model", model_names)
        with right_col.container():
            duration = st.number_input(
                "Duration (s)", min_value=0, step=1, value=30)
            tempo = st.slider(
                "Tempo", 0.5, 2.0, value=1.0)
            temperature = st.slider(
                "Temperature", 1.0, 2.0, value=1.2)
        st.write("#")
    with st.container():
        generate = st.button("Generate")
        st.divider()
        if generate:
            with st.spinner("Hold on for a new melody."):
                try:
                    generate_melody(model, duration, tempo, temperature)
                except:
                    st.error("Failed to generate a melody.")
