import streamlit as st


def about_page():
    with st.container():
        st.title("About")
        st.caption(
            "Get to know about Musc.")
        st.divider()
    with st.container():
        st.write(
            "Generate customized musical melodies with **Musc**. Discover in four sections.")
        with st.expander("Melody"):
            st.caption("Generate musical melodies with custom requirements.")
            st.caption(
                "- Model - Select the model you want to generate music with; select which genre or type of music is required.")
            st.caption(
                "- Duration - Duration of the melody; how long the melody should be.")
            st.caption(
                "- Tempo - Tempo of the melody; how speedy the melody should be.")
            st.caption(
                "- Temperature - Temperature of the melody; how varied the notes of the melody should be.")
            st.write("")
        with st.expander("Models"):
            st.caption(
                "Generate of finetune models with custom datasets and manage them.")
            st.caption("- Available Models - Currently available generated and finetuned models are listed here with the name and "
                       "the created date, unwanted ones can be deleted.")
            st.caption("- Create Model - New model can be created. Default option is to generate model from scratch. "
                       "Select finetune if finetuning is required and select the model for finetuning. "
                       "Enter a name for the model and choose midi files and create a model.")
            st.write("")
        with st.expander("History"):
            st.caption("Previously generated musical melodies.")
            st.caption("All the melodies generated previously are listed with the name and the generated time, "
                       "unwanted ones can be deleted.")
            st.write("")
        with st.expander("About"):
            st.caption("Get to know about the application.")
            st.write("")
        st.divider()
        st.markdown(
            "<div style='text-align: center;'>"
            "<a href='https://dinukagayashan.github.io/DinukaGayashan/' target='_blank' style='color: white; "
            "text-decoration: none; font-family:Reenie Beanie; font-size:1.75rem'>Dinuka Gayashan</a>"
            "</div>",
            unsafe_allow_html=True
        )
