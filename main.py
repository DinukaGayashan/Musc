import streamlit as st
from generators import generator
import numpy as np


def function():
    data = generator.generate_music()
    st.audio(data, sample_rate=44100)

    sample_rate = 44100  # 44100 samples per second
    seconds = 2  # Note duration of 2 seconds

    frequency_la = 440  # Our played note will be 440 Hz

    # Generate array with seconds*sample_rate steps, ranging between 0 and seconds
    t = np.linspace(0, seconds, seconds * sample_rate, False)

    # Generate a 440 Hz sine wave
    note_la = np.sin(frequency_la * t * 2 * np.pi)
    print(type(note_la))
    print(note_la)
    st.audio(note_la, sample_rate=sample_rate)

    st.write("""
    hellow
    """)


if __name__ == "__main__":
    st.title("Musc")
    st.write("""
    music from nowhere
    """)

    if st.button("Generate"):
        function()
