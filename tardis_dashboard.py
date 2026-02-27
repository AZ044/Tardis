import streamlit 
import pandas 
import streamlit as st
import pandas as pd
import numpy 
import time 
import plotly.express as px
import pickle

pd.read_csv("cleaned_dataset.csv")
df = pd.read_csv("./cleaned_dataset.csv")
df = df.dropna(subset=["Gare de départ","Gare d'arrivée","year","month"])
st.title("Delay distribution visualization")

df["Date"] = pd.to_datetime(df["Date"])

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
df_filtered = df[(df["year"] == years) & (df["month"] == month) ]

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
    st.write("Date :",month,years)

# Moyenne du retard moyen de tout les trains à l'arrivé
average = round(df_filtered["Retard moyen de tous les trains à l'arrivée"].mean(),2) 

# Colonnes
average_delays, total_trip, punctuality_rate = st.columns(3)
with average_delays:
    average_delays.metric("Average delay",average,"Minutes","yellow", border=True)
    
with total_trip:
    total_trip.metric("Total trip" ,len(df_filtered), "Trips" , "violet", border=True)

#initalisation du seuil en minutes
line  = 5 
punctuality_trips = (df_filtered["Retard moyen de tous les trains à l'arrivée"]< line).sum()
total_trips = len(df_filtered)
# Calcul du %
rate = round((punctuality_trips/total_trips) * 100,2)

with punctuality_rate:
    punctuality_rate.metric("Punctuality rate",rate,"punctuality rate < 5 Minutes","orange",border=True)


# Interface de prediction

st.title("Prediction interface")
# Charger les modele
with open("linear.pkl","rb") as f:
    reg = pickle.load(f)

with open("mapping_depart.pkl", "rb") as f:
    mapping_depart = pickle.load(f)
    
with open("mapping_arrivee.pkl", "rb") as f:
    mapping_arrivee = pickle.load(f)

#with open("DecisionTreeRegressor.pkl") as d:
    #DescisonTree = pickle.load(d)


#with open("RandomForest.pkl") as r:
    #RandomForest = pickle.load(r)



with st.sidebar:
    st.subheader("Prediction interface")
    Departure = st.selectbox(
        "Departure station",
        list(mapping_depart.keys())
    )

    Arrival = st.selectbox(
        "Arrival station",
        list(mapping_arrivee.keys())
    )

    Average_delays = st.number_input(
        "Average trip duration",
    )

    Month = st.selectbox(
        "Month",
        df["month"].unique()
    )

    Year= st.selectbox(
        "year",
        df["year"].unique()
    )

    
print(list(mapping_depart.keys())[:10])
 
    
if st.button("Predict", type="primary"):
    input_data = pd.DataFrame([[
    mapping_depart[Departure],
    mapping_arrivee[Arrival],
    Average_delays,
    Month,
    Year
    ]], columns=["Gare de départ", "Gare d'arrivée", "Durée moyenne du trajet", "month", "year"])
    prediction = reg.predict(input_data)
    st.metric("Retard prédit", f"{prediction[0]:.1f} minutes")
    
