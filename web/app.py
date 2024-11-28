import streamlit as st
import pandas as pd
import numpy as np
import psycopg2
import sqlalchemy
# from utils import load_data


st.set_page_config(page_title="Marché du travail Tech",
    page_icon="🧊",
    layout="wide")

conn = st.connection("postgresql", type="sql") # calls for secrets.toml file to access postgresql

df = conn.query('SELECT * FROM france_travail;', ttl="10m") #fetch all data from table "france_travail" / ttl=10m for max cache time = 10 minutes


st.sidebar.title("Filtres")


st.title("Data : Marché du travail Tech")

# appel de la fonction load_data, affichage des données 
# data = load_data()

st.dataframe(df)