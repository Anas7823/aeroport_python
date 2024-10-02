# Importation des bibliothèques nécessaires
import streamlit as st
import pandas as pd
from sqlalchemy import create_engine, text

# Informations de connexion PostgreSQL
DB_USER = 'postgres'
DB_PASSWORD = 'respons11'
DB_HOST = 'localhost'
DB_PORT = '5432'  # Utilise le port PostgreSQL par défaut
DB_NAME = 'aeroport'

# Connexion à la base de données PostgreSQL via SQLAlchemy
engine = create_engine(f'postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}')

# Fonction pour compter les aéroports et les destinations
def count_airports():
    query = """
    SELECT
        (SELECT COUNT(*) FROM airports) AS total_airports,
        (SELECT COUNT(DISTINCT origin) FROM flights) AS departure_airports,
        (SELECT COUNT(DISTINCT dest) FROM flights) AS destination_airports;
    """
    with engine.connect() as connection:
        result = connection.execute(text(query)).fetchone()
    return {
        'total_airports': result[0],
        'departure_airports': result[1],
        'destination_airports': result[2]
    }

# Fonction pour obtenir les 10 destinations les plus prisées
def top_10_destinations():
    query = """
    SELECT dest, COUNT(*) AS flight_count
    FROM flights
    GROUP BY dest
    ORDER BY flight_count DESC
    LIMIT 10;
    """
    with engine.connect() as connection:
        result = connection.execute(text(query)).fetchall()
    return result

# Fonction pour obtenir les noms des aéroports pour les destinations les plus prisées
def get_airport_names(destinations):
    query = """
    SELECT name
    FROM airports
    WHERE faa IN :destinations;
    """
    with engine.connect() as connection:
        result = connection.execute(text(query), {'destinations': tuple(destinations)}).fetchall()
    return [row[0] for row in result]

# Utilisation du cache pour charger les données afin d'améliorer les performances
@st.cache_data
def load_data():
    airport_counts = count_airports()
    top_dest_data = top_10_destinations()
    top_destinations = [row[0] for row in top_dest_data]
    top_dest_counts = [row[1] for row in top_dest_data]
    top_dest_names = get_airport_names(top_destinations)
    
    # Création d'un DataFrame pour les informations des destinations les plus prisées
    destinations_info = pd.DataFrame({
        'Destination': top_dest_names,
        'Count': top_dest_counts
    })
    
    return airport_counts, destinations_info

# Chargement des données via la fonction cache
airport_counts, destinations_info = load_data()

# Interface Streamlit
st.markdown("<h1 style='text-align: center; color: #003399;'>Analyse du Trafic Aérien ✈️</h1>", unsafe_allow_html=True)
st.markdown("<hr style='border-top: 3px solid #003399;'>", unsafe_allow_html=True)

# Affichage des métriques avec du style
col1, col2, col3 = st.columns(3)
with col1:
    st.metric(label="Total d'aéroports", value=airport_counts['total_airports'])
with col2:
    st.metric(label="Aéroports de départ", value=airport_counts['departure_airports'])
with col3:
    st.metric(label="Aéroports de destination", value=airport_counts['destination_airports'])

# 10 destinations les plus prisées
st.markdown("<h3 style='color: #003399;'>🏆 10 destinations les plus prisées :</h3>", unsafe_allow_html=True)

# Affichage du tableau des destinations
st.dataframe(destinations_info)

# Graphique des 10 destinations les plus prisées
st.markdown("<h3 style='color: #003399;'>📊 Graphique des 10 destinations les plus prisées :</h3>", unsafe_allow_html=True)
import matplotlib.pyplot as plt

fig, ax = plt.subplots(figsize=(10, 5))
ax.bar(destinations_info['Destination'], destinations_info['Count'], color='#33c3ff')
ax.set_title("10 destinations les plus prisées", fontsize=14, color='#003399')
ax.set_xlabel("Destination", fontsize=12, color='#003399')
ax.set_ylabel("Nombre de vols", fontsize=12, color='#003399')
plt.xticks(rotation=45)
st.pyplot(fig)

# Barre latérale avec options supplémentaires
st.sidebar.header("🔧 Options")
st.sidebar.markdown("Utilisez les options ci-dessous pour filtrer les données.")

# Séparateur graphique
st.markdown("<hr style='border-top: 3px solid #33c3ff;'>", unsafe_allow_html=True)
