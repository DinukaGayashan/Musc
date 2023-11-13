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


    model_names = utility.get_finetuned_models()
    if len(model_names)>0:
        with st.container():
            st.subheader("Finetuned Models")
            for model in model_names:
                col_1,col_2,col_3 = st.columns([2, 2, 1])
                with col_1.container():
                        st.write(f"**{model}**")
                with col_2.container():
                    st.write(model_names[model])
                with col_3.container():
                    delete=st.button('Delete',key=model)
                    if delete:
                        utility.delete_model(model)
                        st.experimental_rerun()
            st.divider()

    with st.container():
        st.subheader("Finetine Model")
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
                        try:
                            train_models(model_name)
                        except:
                            st.error("Failed to generate model.")
                else:
                    st.warning("Model with same name already exists.")
            else:
                st.warning("Enter a model name and a dataset.")
