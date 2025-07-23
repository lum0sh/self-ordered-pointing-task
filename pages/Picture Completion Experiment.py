import streamlit as st

st.set_page_config(page_title="Picture Completion")

project_name = 'picompletion'
experiment_URL = "https://picturecompletion.web.app/?user="

# Title of the app
st.title('Experiment')

# Input for participant ID
username = st.text_input('Enter participant id', max_chars=8)

# Button to submit the ID
if st.button("Generate Link"):
    if username:
        st.link_button("Go to experiment", experiment_URL + username)
    else:
        st.warning("Please enter a participant ID.")
