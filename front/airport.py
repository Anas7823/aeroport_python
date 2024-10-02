import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from sqlalchemy import create_engine

# Remplacez ces variables par les informations de votre base de données
DB_USER = 'postgres'
DB_HOST = 'localhost'
DB_PORT = '8501'
DB_PASSWORD = ''
DB_NAME = 'aeroport'

# Créez une connexion à la base de données
engine = create_engine(f'postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}')

# Chargement des données depuis la base de données
@st.cache_data
def load_data():
    flights = pd.read_sql('SELECT * FROM flights', engine)  # Remplacez par votre table
    airports = pd.read_sql('SELECT * FROM airports', engine)
    airlines = pd.read_sql('SELECT * FROM airlines', engine)
    planes = pd.read_sql('SELECT * FROM planes', engine)
    weather = pd.read_sql('SELECT * FROM weather', engine)
    return flights, airports, airlines, planes, weather

flights, airports, airlines, planes, weather = load_data()

# Interface Streamlit avec style
st.markdown("<h1 style='text-align: center; color: #003399;'>Analyse du Trafic Aérien ✈️</h1>", unsafe_allow_html=True)
st.markdown("<hr style='border-top: 3px solid #003399;'>", unsafe_allow_html=True)

# Affichage des métriques avec du style
col1, col2 = st.columns(2)
with col1:
    total_airports = airports['faa'].nunique()
    st.metric(label="Total d'aéroports", value=total_airports)

with col2:
    total_companies = airlines['Carrier'].nunique()
    st.metric(label="Total de compagnies aériennes", value=total_companies)

# Aéroport de départ le plus emprunté
st.markdown("<h3 style='color: #003399;'>🛫 Aéroport de départ le plus emprunté :</h3>", unsafe_allow_html=True)
most_frequent_origin = flights['origin'].value_counts().idxmax()
st.markdown(f"<b style='color: #ff5733;'>{most_frequent_origin}</b>", unsafe_allow_html=True)

# 10 destinations les plus prisées
st.markdown("<h3 style='color: #003399;'>🏆 10 destinations les plus prisées :</h3>", unsafe_allow_html=True)
top_destinations = flights['dest'].value_counts().head(10).index.tolist()
top_dest_counts = flights['dest'].value_counts().head(10).values

# Ajouter le nom complet des destinations
top_dest_names = airports[airports['faa'].isin(top_destinations)]['name'].tolist()
destinations_info = pd.DataFrame({
    'Destination': top_dest_names,
    'Count': top_dest_counts
})

st.dataframe(destinations_info)

# Graphique des destinations
st.markdown("<h3 style='color: #003399;'>📊 Graphique des 10 destinations les plus prisées :</h3>", unsafe_allow_html=True)
fig, ax = plt.subplots(figsize=(10, 5))
ax.bar(destinations_info['Destination'], destinations_info['Count'], color='#33c3ff')
ax.set_title("10 destinations les plus prises", fontsize=14, color='#003399')
ax.set_xlabel("Destination", fontsize=12, color='#003399')
ax.set_ylabel("Nombre de vols", fontsize=12, color='#003399')
plt.xticks(rotation=45)
st.pyplot(fig)

# Graphique de retards
st.markdown("<h3 style='color: #003399;'>⏱️ Analyse des retards :</h3>", unsafe_allow_html=True)
delay_counts = flights['dep_delay'].value_counts().head(10)

fig, ax = plt.subplots(figsize=(10, 5))
ax.bar(delay_counts.index, delay_counts.values, color='#ff5733')
ax.set_title("Top 10 des retards de départ", fontsize=14, color='#003399')
ax.set_xlabel("Retard (minutes)", fontsize=12, color='#003399')
ax.set_ylabel("Nombre de vols", fontsize=12, color='#003399')
st.pyplot(fig)

st.sidebar.header("🔧 Options")
st.sidebar.markdown("Utilisez les options ci-dessous pour filtrer les données.")

st.markdown("<hr style='border-top: 3px solid #33c3ff;'>", unsafe_allow_html=True)
