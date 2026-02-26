import streamlit 
import pandas 
import streamlit as st
import pandas as pd
import numpy 
import time 
import plotly.express as px

pd.read_csv("cleaned_dataset.csv")
df = pd.read_csv("./cleaned_dataset.csv")
df = df.dropna(subset=["Gare de départ","Gare d'arrivée","year","month"])
st.title("Delay distribution visualization")

year =df['year'].unique()
month = df["month"].unique()

#ajoute une sidebar
with st.sidebar:
    st.title("Delay distribution visualization")
    #with st.expander("Delay distribution visualization"):
    month = st.select_slider(
        "Select month",
        options=month
    )
    st.write("You selected", month)
    years = st.select_slider(
       "Select a year",
       options=year
       )
    st.write("You selected", years)

#Filtre les choix 
df_filtered = df[(df["year"] == years) & (df["month"] == month)]

#Histogram (regroupe les valeurs en intervalles (appelés "bins"))
fig = px.histogram(df_filtered, x = "Retard moyen de tous les trains à l'arrivée",
barmode="overlay",
width=1200,
height=700,
range_x=["-30","90"],
labels={"Retard moyen de tous les trains à l'arrivée":"Retard moyen à l'arrivée (minutes)"},
title="Histogram of Retard moyen de tous les trains à l'arrivée"
)
fig.update_yaxes(title="Nombres de trajets")
st.plotly_chart(fig)


st.title("Descriptive statistics panel")

with st.sidebar:
    st.subheader("Descriptive statistics panel")


average = df_filtered["Retard moyen de tous les trains à l'arrivée"].mean()   


average_delays, total_trip, punctuality_rate = st.columns(3)
with average_delays:
    st.subheader("Average delay")
    st.write("average delay in ",years,month)
    average
    
with total_trip:
    st.subheader("Total trip")
    
with punctuality_rate:
    st.subheader("Punctuality rate")
