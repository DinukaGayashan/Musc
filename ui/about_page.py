import streamlit as st


def about_page():
    with st.container():
        st.title("About")
        st.caption(
            "Get to know about Musc.")
        st.divider()
    with st.container():
        st.write("Musc lets you to generate customized musical melodies. There are four sections to be discovered.")
        with st.expander("Melody"):
            st.caption("Generate musical melodies with custom requirements.")
            st.caption("- Model - Select the model you want to generate music with; select one from the default or "
                       "finetuned ones.")
            st.caption("- Duration - Duration of the melody; how long the melody should be.")
            st.caption("- Tempo - Tempo of the melody; how speedy the melody should be.")
            st.caption("- Temperature - Temperature of the melody; how varied the notes of the melody should be.")
            st.write("")
        with st.expander("Finetune"):
            st.caption("Finetune models with custom datasets and manage them.")
            st.caption("- Finetuned Models - Currently available finetuned models are listed here with the name and "
                       "the created date, unwanted ones can be deleted.")
            st.caption("- Finetune Models - New finetuned model can be created. Enter a name for the model and "
                       "choose midi files and finetune a model.")
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
