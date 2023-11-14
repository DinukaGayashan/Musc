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
            with st.container():
                st.write(melody.split('.')[0],melodies[melody])
                col_1, col_2 = st.columns([3, 1])
                with col_1.container():
                    wave_file = midi_to_wave(utility.get_melody_name(melody))
                    st.audio(wave_file, format="audio/wav")
                with col_2.container():
                    delete=st.button(f"Delete",key=melody)
                    if delete:
                        utility.delete_melody(melody)
                        st.experimental_rerun()
            st.write('')
