import streamlit as st
 
st.set_page_config(page_title="Picture Completion")
project_name = 'picompletion'
experiment_URL = "https://picturecompletion.web.app/?user="
# Simulating data for the behavioral task
# participant_ids = get_participant_ids(project_name)

# Title of the app
st.title('Experiment')
username = st.text_input('Enter participant id',max_chars=8)
st.link_button("Go to experiment",experiment_URL+username)
    
