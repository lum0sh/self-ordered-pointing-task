import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import json
import base64
from datetime import datetime

from utils.data_utils import get_participant_data

from io import BytesIO
 
#7bP5jDHC3xoch8HK04WDVUGTffQQ

st.set_page_config(page_title="Picture Completion Dashboard")
project_name = 'picompletion'


# Title of the app
st.title('Dashboard')
 

# Sidebar for user selection
selected_user = st.text_input("Enter completion code below:")

ts = datetime.now().strftime("%Y%m%d_%H%M%S")

@st.cache_data
def download_data_from_db(trial,subject,frame,state):
    output = BytesIO()
    with pd.ExcelWriter(output, engine='openpyxl') as writer:
        trial.to_excel(writer, "trial")
        subject.to_excel(writer, "subject")
        frame.to_excel(writer, "frame")
        state.to_excel(writer, "state")
    output.seek(0)  # Reset pointer to the start of the stream
    return output   

@st.cache_data
def process_trials(df):
    # df['prev_selected'] = df['prev_selected'].fillna(0).astype(int)
    # df['error'] = df.duplicated(subset=['numTiles','blockTrial','selectedImage'],keep='first')
 
    return df


if selected_user:
    try:
        trial, subject, frame, state = get_participant_data(project_name,selected_user)
    except AssertionError:
        st.write("Participant data not found!!!")
    if trial.shape[0]>0:
        audio_blob_str = subject.loc[0,'audioBlob']
        audio_blob = json.loads(audio_blob_str)
        # Step 1: Decode base64 data
        audio_bytes = base64.b64decode(audio_blob["data"])

        # Step 2: Wrap in BytesIO for Streamlit
        audio_file = BytesIO(audio_bytes)

        # Step 3: Play in Streamlit
        st.audio(audio_file, format=audio_blob["mimetype"])
        processed_trials = process_trials(trial)

        processed_trials = processed_trials[['trialNumber','tileBlockIndex',
                                            'responseTime','goCueTime','pageNumber']]
        processed_trials['responseTime_s'] = processed_trials['responseTime'] / 1000.
        processed_trials['goCueTime_s'] = processed_trials['goCueTime'] / 1000.

        processed_trials['timeStamps'] = processed_trials['goCueTime_s'].diff().cumsum()
        
        st.table(processed_trials[['trialNumber','responseTime_s','timeStamps','goCueTime_s']])
        
    else:
        st.write("Empty Dataframe")

