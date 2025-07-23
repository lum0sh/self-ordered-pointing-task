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
# experiment_URL = "http://selforderedpointingtask.firebaseapp.com/?ver="
# Simulating data for the behavioral task
# participant_ids = get_participant_ids(project_name)

# Title of the app
st.title('Dashboard')
 

# Sidebar for user selection
# selected_user = st.sidebar.selectbox('Select a Participant', participant_ids)
# st.markdown(f"### Subject ID:  \n **{selected_user}**")
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
        st.download_button(
            label="Download data",
            data=download_data_from_db(processed_trials, subject, frame, state),
            file_name=f"{selected_user}_{ts}.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )

        processed_trials = processed_trials[['trialNumber','tileBlockIndex',
                                            'responseTime','numTiles','pageNumber']]
        processed_trials.loc[:,'responseTime_s'] = processed_trials['responseTime']/1000.

        total_time, total_trials = st.columns(2)

        with total_time:
            st.metric("Total Time",str(round(float(processed_trials['responseTime_s'].sum()),2))+' s')

        with total_trials:
            st.metric("Total Trials",processed_trials.shape[0])

        # st.table(processed_trials)

        
        # Create the figure and axis
    #     fig, ax = plt.subplots(figsize=(10, 5))  # Adjust size if needed

    #     # Generate the bar plot
 
    #     error_data = processed_trials.groupby(['numTiles', 'blockTrial'])['error'].sum().reset_index()


    #     # Get unique hue values
    #     unique_tiles = sorted(error_data['numTiles'].unique())
    #     n_colors = len(unique_tiles)

    #     # Choose a colormap
    #     cmap = plt.get_cmap('viridis', n_colors)  # or 'viridis', 'plasma', etc.

    #     # Map each hue level to a color
    #     palette = {tile: cmap(i) for i, tile in enumerate(unique_tiles)}

    #     # Plot with custom palette
    #     sns.barplot(data=error_data, x='blockTrial', y='error', hue='numTiles', palette=palette, ax=ax)

 
            

    #     # Set title and labels
    #     ax.set_title("Number of Errors Across Trials", fontsize=14)
    #     ax.set_xlabel("Trial Block", fontsize=12)
    #     ax.set_ylabel("Error Count", fontsize=12)
        
        
    #     # Set x-tick labels as blockTrial values
    #     # ax.set_xticklabels([f"{idx[1]}" for idx in error_data.index], rotation=0, ha="right")

    #     st.markdown("## Performance Report")
    #     # Display the plot in Streamlit
    #     st.pyplot(fig)

    #     fig, ax = plt.subplots(figsize=(10, 5))  # Adjust size if needed

    #     sns.scatterplot(processed_trials,x='trialNumber',y='responseTime',hue='numTiles',palette=palette, ax=ax)
    #     ax.set_xlabel("Trial Number")
    #     ax.set_ylabel("Reaction time (ms)")
    #     ax.set_title("Reaction Time across trials")
    #     st.pyplot(fig)

        
    else:
        st.write("Empty Dataframe")

    # # ids :
    #     # JKqowBchDRXfPI59CWjfJN46Hz02
    #     # 10V6r5kdjTTwtBDacmjqtYsw3512
    #     # ujYMAO8B8KhUdB6ZHmY333nQSIu1
    #     # 35USuHJIWAojvzNvYCegnQQvQKCO
        
