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

year = sorted(df["year"].dropna().astype(int).unique())
month = df["month"].unique()
month_names = {
1: "January", 2: "February", 3: "March", 4: "April",
5: "May", 6: "June", 7: "July", 8: "August",
9: "September", 10: "October", 11: "November", 12: "December"
}
month_disponibles = sorted(df["month"].unique())
month_labels = [month_names[m] for m in month_disponibles]

#ajoute une sidebar
with st.sidebar:
    st.title("Delay distribution visualization")
    #with st.expander("Delay distribution visualization"):
    month = st.select_slider(
        "Select month",
        options=month_labels
    )
    
    st.write("You selected", month)
    years = st.select_slider(
       "Select a year",
       options=year
       )
    
    st.write("You selected", years)

month = [k for k, v in month_names.items() if v == month][0]

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
# Charger le modele lineaire
with open("linear.pkl","rb") as f:
    reg = pickle.load(f)
with open("mapping_depart.pkl", "rb") as f:
    mapping_depart = pickle.load(f) 
with open("mapping_arrivee.pkl", "rb") as f:
    mapping_arrivee = pickle.load(f)
    

# Charge le modele Descision Tree
#with open("DecisionTreeRegressor.pkl", "rb") as f:
    #DescisonTree = pickle.load(f)
#with open("service.pkl", "rb") as f:
    #service = pickle.load(f)
#with open("departure.pkl", "rb") as f:
    #departure = pickle.load(f)
#with open("arrival.pkl", "rb") as f:
    #arrival = pickle.load(f)



# Modele lineaire
with st.sidebar:
    st.subheader("Prediction interface")
    st.subheader("Linear Model")
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
            month_labels
        )

    Year= st.selectbox(
            "year",
            year
        )

Month_num = [k for k, v in month_names.items() if v == Month][0]
print(list(mapping_depart.keys())[:10])
 
    
if st.button("Predict Linear Model", type="primary"):
    input_data = pd.DataFrame([[
    mapping_depart[Departure],
    mapping_arrivee[Arrival],
    Average_delays,
    Month_num,
    Year
    ]], columns=["Gare de départ", "Gare d'arrivée", "Durée moyenne du trajet", "month", "year"])
    prediction = reg.predict(input_data)
    st.metric("Predict late", f"{prediction[0]:.1f} minutes")


# Descision Tree modele

# with st.sidebar:
#     with st.expander(" Descision Tree Model"):
#         DT_service = st.selectbox(
#             "Service",
#             df["Service"].unique()
#         )
#         
#         
#         DT_Departure = st.selectbox(
#             "Departure station",
#             df["Gare de départ"].unique(),
#             key="DT_departure"
#         )
# 
#         DT_Arrival = st.selectbox(
#             "Arrival station",
#             df["Gare d'arrivée"].unique(),
#             key="DT_arrival"
#         )
# 
#         DT_Month = st.selectbox(
#             "Month",
#             month_labels,
#             key="DT_month"
#         )
# 
#         DT_Year = st.selectbox(
#             "Year",
#             year,
#             key="DT_year"
#         )
# 
# DT_Month_num = [k for k, v in month_names.items() if v == DT_Month][0]
# 
# if st.button("Predisct escision Tree Model"):
#     input_data = pd.DataFrame([[
#    service.transform([DT_service])[0],
#     departure.transform([DT_Departure])[0],
#     arrival.transform([DT_Arrival])[0],
#     DT_Year,
#     DT_Month_num
#     ]], columns=["Service","Gare de départ", "Gare d'arrivée", "year", "month"])
#     prediction = DescisonTree.predict(input_data)
#     st.metric("Predict late", f"{prediction[0]:.1f} minutes")