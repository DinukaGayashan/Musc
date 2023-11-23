import streamlit as st

from models import create_model
from ui import utility


def train_models(model_name, model, from_scratch):
    create_model.create_model(model_name, model, from_scratch)
    st.success(
        f"Successfully created a model named {model_name}.")


def model_page():
    with st.container():
        st.title("Models")
        st.caption(
            "Generate of finetune models with custom datasets and manage them.")
        st.divider()
    model_names = utility.get_model_names()
    if len(model_names) > 0:
        with st.container():
            st.subheader("Available Models")
            for model in model_names:
                col_1, col_2, col_3 = st.columns([2, 2, 1])
                with col_1.container():
                    st.write(f"**{model}**")
                with col_2.container():
                    st.write(model_names[model])
                with col_3.container():
                    delete = st.button('Delete', key=model)
                    if delete:
                        utility.delete_model(model)
                        st.experimental_rerun()
            st.divider()
    with st.container():
        st.subheader("Create Model")
        if len(model_names) > 0:
            left_col, right_col = st.columns([1, 5])
            with left_col.container():
                finetune = st.checkbox("Finetune")
            with right_col.container():
                model_names = utility.get_model_names()
                model = st.radio(
                    "Model", model_names, label_visibility="hidden", disabled=not finetune)
            st.write("#")
        left_col, right_col = st.columns([2, 3], gap="large")
        with left_col.container():
            model_name = st.text_input("Enter model name")
        with right_col.container():
            uploaded_files = st.file_uploader(
                "Choose midi files", accept_multiple_files=True, type=["mid", "midi"])
        st.write("#")

    with st.container():
        generate = st.button("Create")
        st.divider()
        if generate:
            if model_name and uploaded_files:
                if not utility.is_model_available(model_name):
                    utility.save_dataset(model_name, uploaded_files)
                    with st.spinner("Hold on for a new model. This may take a while."):
                        try:
                            train_models(model_name, model,
                                         from_scratch=not finetune)
                            utility.delete_dataset(model_name)
                        except:
                            utility.delete_model(model_name)
                            st.error("Failed to generate model.")
                else:
                    st.warning("Model with same name already exists.")
            else:
                st.warning("Enter a model name and a dataset.")
