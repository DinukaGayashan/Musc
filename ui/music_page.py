import streamlit as st
from generators import melody_generator


def generate_melody(duration, temperature):
    audio_file = melody_generator.generate_music(duration, temperature)
    st.success(f'Successfully generated a melody of {duration} seconds with {duration} model temperature of {temperature}.')
    st.audio(audio_file)


def music_page():
    with st.container():
        st.subheader('Options')
        left_col, right_col = st.columns([1, 1])
        with left_col.container():
            st.radio('Model', ['Pop', 'Jazz'],)
        with right_col.container():
            duration = st.number_input(
                'Duration (s)', min_value=0, step=1, value=30)
            temperature = st.slider(
                'Temperature', 0.1, 1.0, 0.5)
    st.write('#')
    with st.container():
        if st.button('Generate'):
            st.divider()
            with st.spinner('Hold on for a new melody'):
                try:
                    generate_melody(duration, temperature)
                except:
                    st.error("Failed to generate a melody.")
