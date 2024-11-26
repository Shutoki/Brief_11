import streamlit as st
import pandas as pd
import numpy as np
from utils import load_data



st.set_page_config(page_title="Marché du travail Tech",
    page_icon="🧊",
    layout="wide")

st.sidebar.title("Filtres")


st.title("Data : Marché du travail Tech")

# appel de la fonction load_data, affichage des données 
data = load_data()