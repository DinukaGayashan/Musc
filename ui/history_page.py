import streamlit as st
from ui import utility
from models.melody_formatter import midi_to_wave

def history_page():
    with st.container():
        st.title("History")
        st.caption(
            "Previously generated musical melodies.")
        st.divider()

    with st.container():
        melodies = utility.get_melody_names()
        for melody in melodies:
            delete_button = st.button(f"{melody}")
            st.write(melodies[melody]) 
            wave_file = midi_to_wave(f"generated_melodies/{melody}")
            st.audio(wave_file, format="audio/wav")
            st.write('')
