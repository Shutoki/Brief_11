import streamlit as st
import pandas as pd
import numpy as np
import psycopg2
import sqlalchemy
import plotly.express  as  px 
import plotly.figure_factory as ff
import json
import folium
import geopandas as gpd
import requests

from streamlit_folium import folium_static

from utils import load_data, dept_region
from path import data_geojson



st.set_page_config(page_title="Marché du travail Tech",
    page_icon="🧊",
    layout="wide")

conn = st.connection("postgresql", type="sql") # calls for secrets.toml file to access postgresql

df = conn.query('SELECT * FROM france_travail;', ttl="10m") #fetch all data from table "france_travail" / ttl=10m for max cache time = 10 minutes

data = pd.DataFrame(df)

lowercase= lambda x: str(x).lower()
data.rename(lowercase, axis='columns', inplace=True)
print(data.columns)


data["departement"] = data['lieutravail_libelle'].str.slice(0,3)
data['departement'] = data['departement'].str.strip()
data['region'] = data['departement'].astype(str).map(dept_region)

data["latitude"] = pd.to_numeric(data["lieutravail_latitude"],errors = 'coerce')
data["longitude"] = pd.to_numeric(data["lieutravail_longitude"],errors = 'coerce')
valid_locations = data.dropna(subset=["latitude", "longitude"])
print(data['romecode'].value_counts())

st.title("Data : Marché du travail Tech")
# #if st.button("Get data from API"):
#  #   response = requests.post("http://api:5000/api/offers", json={"begin_datetime": max_value})
#     print(response)
#     st.write(response.json())

st.sidebar.title("Filtres")



# appel de la fonction load_data, affichage des données 
old_data = st.dataframe(data)

# Affichage initial des données
#st.dataframe(data)


 # Nom des colonnes
columns = data.columns

# Section de tri
st.sidebar.markdown("# Expérience")
# Filtre pour sélectionner un code rome

if 'romecode' in columns:
    lieux_uniques = sorted(data['romecode'].str.lower().unique())
    lieu_selectionne = st.sidebar.selectbox(
        " ",
        ["Tous"] + lieux_uniques,
        index=0
    )
    if lieu_selectionne != "Tous":
        data = data[data['romecode'].str.lower() == lieu_selectionne]

# Filtre pour sélectionner une expérience spécifique

if 'experienceexige' in columns:
    lieux_uniques = sorted(data['experienceexige'].str.lower().unique())
    lieu_selectionne = st.sidebar.selectbox(
        " ",
        ["Tous"] + lieux_uniques,
        index=0
    )
    if lieu_selectionne != "Tous":
        data = data[data['experienceexige'].str.lower() == lieu_selectionne]

# Filtre pour l'alternance
if 'alternance' in columns:
    alternance_filter = st.sidebar.checkbox("Afficher uniquement les alternances")
    if alternance_filter:
        data = data[data['alternance'] == True]

# Sélection des colonnes à afficher
st.sidebar.markdown("# Affichage")
display_columns = st.sidebar.multiselect(
    "Sélectionner les colonnes à afficher",
    columns,
    default=columns
)

# Sélection des colonnes
df = data[display_columns]

# Affichage du DataFrame
#st.dataframe(data)
############## Répartitition géographique des offres

regions = gpd.read_file(data_geojson)

# # Afficher les premières lignes pour vérifier
#st.write(regions.head())

# # Création de la carte
m = folium.Map(location=[46.603354, 1.888334], zoom_start=6)

# # Ajout des contours des régions
folium.GeoJson(regions).add_to(m)

# # Ajout des marqueurs pour les offres d'emploi
# Définir les codes ROME et leurs couleurs associées
codes_rome_couleurs = {
    'M1805': 'green',  # Couleur pour M1805
    'M1403': 'red'  # Couleur pour M1403
}
for idx, row in valid_locations.iterrows():
    if row['romecode'] in codes_rome_couleurs:
        folium.CircleMarker(
            location=[row['latitude'], row['longitude']],
            radius=5,
            popup=(
                f"Lieu: {row['lieutravail_libelle']}<br>"
                f"Poste: {row['intitule']}<br>"
                f'<a href="{row["origineoffre_urlorigine"]}" target="_blank">Plus d\'infos</a>'
            ),
            color=codes_rome_couleurs[row['romecode']],
        fill=True,
   ).add_to(m)

# # Affichage de la carte dans Streamlit
folium_static(m)

############# Affichage  de la répartition entre dev et data
fig  =  px . pie (data, names='romecode', color='romecode',  color_discrete_map={'M1805': 'green', 'M1403': 'red'},
             title="Proportion des offres entre développeurs et data analystes") 
st.plotly_chart(fig, use_container_width=True)

############# Répartition des offres en France

# Vérifiez que les colonnes 'region' et 'romecode' existent dans le DataFrame
if 'region' in data.columns and 'romecode' in data.columns:
    # Calculer le nombre d'offres pour chaque combinaison région-romecode
    df_count = data.groupby(['region', 'romecode']).size().reset_index(name='count')

    # Créer un sélecteur pour les romecodes
    romecodes = sorted(df_count['romecode'].unique())
    selected_romecodes = st.multiselect('Sélectionnez les codes rome à afficher', romecodes, default=romecodes)

    # Filtrer les données selon la sélection
    df_filtered = df_count[df_count['romecode'].isin(selected_romecodes)]

    # Créer un seul treemap pour les romecodes sélectionnés
    fig = px.treemap(
        df_filtered,
        path=['region', 'romecode'],
        values='count',
        color='count',
        color_continuous_scale='RdBu',
        title='Nombre d\'offres par région et romecode'
    )

    # Personnaliser l'affichage du texte et du survol
    fig.data[0].textinfo = 'label+value'
    fig.data[0].hovertemplate = '%{label}<br>Nombre d\'offres: %{value}'

    # Améliorer la mise en page
    fig.update_layout(
        margin=dict(t=50, l=25, r=25, b=25),
        font=dict(size=12),
    )

    # Afficher le treemap dans Streamlit
    st.plotly_chart(fig, use_container_width=True)
else:
    st.error("Les colonnes 'region' ou 'romecode' ne sont pas présentes dans le DataFrame.")
# # Calculer le nombre d'offres pour chaque combinaison région-romecode
# df_count = data.groupby(['region', 'value']).size().unstack(fill_value=0)

# # Créer un treemap pour M1403
# fig_M1403 = px.treemap(
#     df_count.reset_index(),
#     path=['region'],
#     values='M1403',
#     color='M1403',
#     color_continuous_scale='RdBu',
#     title='Nombre d\'offres {M1403} par région'
# )
# fig_M1403.data[0].textinfo = 'label+value'
# fig_M1403.data[0].hovertemplate = '%{label}<br>Nombre d\'offres: %{value}'

# # # Créer un treemap pour M1805
# fig_M1805 = px.treemap(
#     df_count.reset_index(),
#     path=['region'],
#     values='M1805',
#     color='M1805',
#     color_continuous_scale='RdBu',
#     title='Nombre d\'offres M1805 par région'
# )
# fig_M1805.data[0].textinfo = 'label+value'
# fig_M1805.data[0].hovertemplate = '%{label}<br>Nombre d\'offres: %{value}'

# # Afficher les treemaps dans Streamlit
# st.plotly_chart(fig_romecode, use_container_width=True)
# st.plotly_chart(fig_M1805, use_container_width=True)
