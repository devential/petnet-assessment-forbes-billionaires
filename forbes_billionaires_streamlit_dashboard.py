import streamlit as st
import pandas as pd
import numpy as np
import altair as alt
import pickle

st.title('Billionaire Education')

@st.cache_data
def load_data(filename):
    data = pd.read_pickle(filename)
    return data

@st.cache_data
def load_plotting_data(filename):
    with open(filename, 'rb') as handle:
        data = pickle.load(handle)
    return data

forbes_billionaires = load_data("./forbes_billionaires_preprocessed.pkl")
PlottingDFs = load_plotting_data("./PlottingDFs.pkl")

billionaire_names = forbes_billionaires.Name.unique().tolist()
if st.checkbox('Search Billionaires'):
    selected_name = st.selectbox("Name:", options=billionaire_names, key=1)
    entry = forbes_billionaires[forbes_billionaires["Name"] == selected_name]
    st.write(entry[["NetWorth", "Education"]])

st.subheader('How did billionaires do in school?')
"""
**1408** members of the Forbes Billionaires dataset have known educational information. From this data, we know that:
- **43** only finished or dropped out of High School;
- **1007** completed a Bachelor's degree, while **63** dropped out of their Bachelor's programs;
- **295** remaining billionaires pursued graduate education, such as an MBA, Master's, PhD, MD.
"""


st.subheader('Educational institutes attended by billionaires')
MainEducationDF = pd.concat([PlottingDFs["BachelorSelfmade"], PlottingDFs["BachelorDOSelfmade"], PlottingDFs["BachelorInherited"], PlottingDFs["BachelorDOInherited"]])
all_types = MainEducationDF.label.unique().tolist()
if st.checkbox('Filter by Education and Source of Wealth'):
    selected_types = st.multiselect("Select education and source of wealth:", options=all_types, default=all_types)
    MainEducation_color = 'label'
else:
    selected_types = all_types
    MainEducation_color = alt.value('gray')
selection = alt.selection_single(fields=['values'])
MainEducation = alt.Chart(MainEducationDF[MainEducationDF.label.isin(selected_types)]).mark_bar(clip=True).encode(
    alt.X('values', title='Number of Billionaire Attendees'), 
    alt.Y('index', sort='-x', title='Schools'), 
    color=MainEducation_color).configure_axisX(orient = "top").configure_axisY(orient = "left")
st.altair_chart(MainEducation, use_container_width=True)

