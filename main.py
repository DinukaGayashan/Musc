import streamlit as st
from generators import melody_generator


def function():
    data = melody_generator.generate_music()
    st.audio(data)


if __name__ == "__main__":
    st.title("Musc")
    st.write("""
    music from nowhere
    """)

    if st.button("Generate"):
        function()
