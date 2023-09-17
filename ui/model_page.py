import streamlit as st
from models import model


def train_models():
    model.train_model()


def model_page():
    if st.button("Train Models"):
        with st.spinner('Hold on for a new model'):
            train_models()
