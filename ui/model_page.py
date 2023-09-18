import streamlit as st
from models import model
from ui import utility


def train_models(model_name):
    model.train_model(model_name)


def model_page():
    with st.container():
        st.title("Models")
        st.caption(
            "Generate music generating models with custom datasets. Provide a dataset and Train the models and manage them.")
        st.divider()

    with st.container():
        # left_col, right_col = st.columns([1, 1])
        with st.container():
            model_names = utility.get_model_names()
            model = st.radio('Model', model_names,)
        st.write('#')

    with st.container():
        left_col, right_col = st.columns([2, 3], gap="large")
        with left_col.container():
            model_name = st.text_input("Enter model name")
        with right_col.container():
            uploaded_files = st.file_uploader(
                "Choose midi files", accept_multiple_files=True, type="mid")

    with st.container():
        if st.button("Generate"):
            if model_name:
                utility.save_dataset(model_name, uploaded_files)
                with st.spinner('Hold on for a new model'):
                    train_models(model_name)
            else:
                st.warning("Enter a model name")
