import streamlit as st

st.set_page_config(page_title="Picture Completion")

project_name = 'picompletion'
experiment_URL = "https://picturecompletion.web.app/?user="

# Title of the app
st.title('Experiment')

# Input for participant ID
username = st.text_input('Enter participant id', max_chars=8)

# Button to trigger the redirect in a new tab
if st.button("Submit"):
    if username:
        redirect_url = experiment_URL + username
        st.markdown(f"""
            <script>
                window.open("{redirect_url}", "_blank");
            </script>
            <p>Opening experiment in a new tab: <a href="{redirect_url}" target="_blank">{redirect_url}</a></p>
        """, unsafe_allow_html=True)
    else:
        st.warning("Please enter a participant ID.")
