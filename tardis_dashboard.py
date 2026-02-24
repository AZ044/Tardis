import streamlit 
import pandas 
import streamlit as st
import pandas as pd
import numpy 
import time 

@st.cache_data
def load_data():
    return pd.read_csv("cleaned_dataset.csv")

df = pd.read_csv("./cleaned_dataset.csv")
df

