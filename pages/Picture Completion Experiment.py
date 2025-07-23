import streamlit as st

st.set_page_config(page_title="Picture Completion")

project_name = 'picompletion'
experiment_URL = "https://picturecompletion.web.app/?user="

# Title of the app
st.title('Experiment')

# Input for participant ID
username = st.text_input('Enter participant id', max_chars=8)

# Button to submit and redirect
if st.button("Submit"):
    if username:
        redirect_url = experiment_URL + username
        # Inject JavaScript to redirect
        st.markdown(f"""
            <meta http-equiv="refresh" content="0; url={redirect_url}">
            <p>Redirecting to <a href="{redirect_url}">{redirect_url}</a>...</p>
        """, unsafe_allow_html=True)
    else:
        st.warning("Please enter a participant ID.")
