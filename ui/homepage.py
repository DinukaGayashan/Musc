import streamlit as st
from streamlit_option_menu import option_menu
from ui import music_page, model_page


def homepage():
    with st.sidebar:
        st.title("Musc")
        st.caption("music from nowhere")
        st.divider()
        selected = option_menu(
            menu_title=None,
            options=["Music", "Models"],
            icons=["music-note-beamed", "robot"]
        )

    if selected == "Music":
        music_page.music_page()

    if selected == "Models":
        model_page.model_page()
