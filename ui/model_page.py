import streamlit as st
from models import finetune_model
from ui import utility


def train_models(model_name):
    finetune_model.finetune_model(model_name)
    st.success(
        f"Successfully finetuned a model named {model_name}.")


def model_page():
    with st.container():
        st.title("Finetune")
        st.caption(
            "Finetune models with custom datasets. Provide a dataset and finetune a model.")
        st.divider()

    # with st.container():
    #     with st.container():
    #         model_names = utility.get_model_names()
    #         model = st.radio("Model", model_names,)
    #     st.divider()

    with st.container():
        left_col, right_col = st.columns([2, 3], gap="large")
        with left_col.container():
            model_name = st.text_input("Enter model name")
        with right_col.container():
            uploaded_files = st.file_uploader(
                "Choose midi files", accept_multiple_files=True, type=["mid", "midi"])
        st.write("#")
    with st.container():
        generate = st.button("Finetune")
        st.divider()
        if generate:
            if model_name and uploaded_files:
                if not utility.is_model_available(model_name):
                    utility.save_dataset(model_name, uploaded_files)
                    with st.spinner("Hold on for a finetuned model."):
                        # try:
                        train_models(model_name)
                        # except:
                        # st.error("Failed to generate model.")
                else:
                    st.warning("Model with same name already exists.")
            else:
                st.warning("Enter a model name and a dataset.")
