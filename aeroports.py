# Importation des bibliothèques nécessaires
import streamlit as st
import pandas as pd
from sqlalchemy import create_engine, text
import matplotlib.pyplot as plt

# Informations de connexion PostgreSQL
DB_USER = 'postgres'
DB_PASSWORD = 'respons11'
DB_HOST = 'localhost'
DB_PORT = '5432'  # Utilise le port PostgreSQL par défaut
DB_NAME = 'aeroport'

# Connexion à la base de données PostgreSQL via SQLAlchemy
engine = create_engine(f'postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}')

# Fonction pour compter les aéroports, départs, destinations
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

# Fonction pour les aéroports sans DST et les fuseaux horaires
def count_airports_without_dst_and_timezones():
    query_airports_without_dst = """
    SELECT COUNT(*) AS airports_without_dst
    FROM airports
    WHERE dst = 'N';
    """
    query_time_zones = """
    SELECT COUNT(DISTINCT tz) AS time_zones
    FROM airports;
    """
    with engine.connect() as connection:
        airports_without_dst = connection.execute(text(query_airports_without_dst)).fetchone()[0]
        time_zones = connection.execute(text(query_time_zones)).fetchone()[0]
    return {'airports_without_dst': airports_without_dst, 'time_zones': time_zones}

# Requête pour l'aéroport de départ le plus emprunté
def most_popular_origin():
    query = """
    SELECT origin, COUNT(*) AS flight_count
    FROM flights
    GROUP BY origin
    ORDER BY flight_count DESC
    LIMIT 1;
    """
    with engine.connect() as connection:
        most_popular_origin = connection.execute(text(query)).fetchone()[0]
    return most_popular_origin

# Requête SQL pour compter le nombre de destinations desservies par chaque compagnie
def count_destinations_by_carrier():
    query = """
    SELECT carrier, COUNT(DISTINCT dest) AS destination_count
    FROM flights
    GROUP BY carrier;
    """
    with engine.connect() as connection:
        result = connection.execute(text(query)).fetchall()
    return result

# Requête SQL pour obtenir les vols ayant atterri à Houston (IAH ou HOU)
def flights_to_houston():
    query = """
    SELECT *
    FROM flights
    WHERE dest IN ('IAH', 'HOU');
    """
    with engine.connect() as connection:
        result = connection.execute(text(query)).fetchall()
    return result

# Requête SQL pour compter les vols de NYC (JFK, LGA, EWR) à Seattle (SEA)
def flights_nyc_to_seattle():
    query = """
    SELECT
        COUNT(*) AS flights_from_nyc_to_seattle,
        COUNT(DISTINCT carrier) AS unique_carriers,
        COUNT(DISTINCT tailnum) AS unique_planes
    FROM flights
    WHERE origin IN ('JFK', 'LGA', 'EWR') AND dest = 'SEA';
    """
    with engine.connect() as connection:
        result = connection.execute(text(query)).fetchone()
    return result

# Fonction pour les 10 destinations les plus prisées
def top_10_destinations():
    query = """
    SELECT a.name, f.dest, COUNT(*) AS flight_count
    FROM flights f
    JOIN airports a ON f.dest = a.faa
    GROUP BY a.name, f.dest
    ORDER BY flight_count DESC
    LIMIT 10;
    """
    with engine.connect() as connection:
        result = connection.execute(text(query)).fetchall()
    return result

# Fonction pour les 10 destinations les moins prisées
def bottom_10_destinations():
    query = """
    SELECT a.name, f.dest, COUNT(*) AS flight_count
    FROM flights f
    JOIN airports a ON f.dest = a.faa
    GROUP BY a.name, f.dest
    ORDER BY flight_count ASC
    LIMIT 10;
    """
    with engine.connect() as connection:
        result = connection.execute(text(query)).fetchall()
    return result

# Fonction pour compter les compagnies aériennes et avions annulés
def count_companies_planes_cancelled_flights():
    query = """
    SELECT
        (SELECT COUNT(*) FROM airlines) AS total_airlines,
        (SELECT COUNT(*) FROM planes) AS total_planes,
        (SELECT COUNT(*) FROM flights WHERE arr_delay IS NULL) AS cancelled_flights;
    """
    with engine.connect() as connection:
        result = connection.execute(text(query)).fetchone()
    return {
        'total_airlines': result[0],
        'total_planes': result[1],
        'cancelled_flights': result[2]
    }

# Utilisation du cache pour charger les données afin d'améliorer les performances
@st.cache_data
def load_data():
    
    # appel des fonctions dans des variables
    
    airport_counts = count_airports()
    
    # Récupération des données pour les destinations les plus et moins prisées
    top_dest_data = top_10_destinations()
    bottom_dest_data = bottom_10_destinations()
    
    # Création des DataFrames pour les destinations
    top_destinations_info = pd.DataFrame(top_dest_data, columns=['Destination', 'Code', 'Nombre de vols']).drop(columns='Code')
    bottom_destinations_info = pd.DataFrame(bottom_dest_data, columns=['Destination', 'Code', 'Nombre de vols']).drop(columns='Code')
    
    return airport_counts, top_destinations_info, bottom_destinations_info

# Chargement des données via la fonction cache
airport_counts, top_destinations_info, bottom_destinations_info = load_data()
cancellation_data = count_companies_planes_cancelled_flights()
airports_without_dst = count_airports_without_dst_and_timezones()

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

# Affichage des autres informations
st.markdown("<h3 style='color: #003399;'>🔎 Autres informations :</h3>", unsafe_allow_html=True)
col4, col5 = st.columns(2)
with col4:
    st.metric(label="Aéroports sans DST", value=airports_without_dst['airports_without_dst'])
with col5:
    st.metric(label="Nombre de fuseaux horaires", value=airports_without_dst['time_zones'])

# Affichage des vols annulés
st.markdown("<h3 style='color: #003399;'>ℹ️ Informations utiles :</h3>", unsafe_allow_html=True)
col6, col7 = st.columns(2)
with col6:
    st.metric(label="Total des compagnies aériennes", value=cancellation_data['total_airlines'])
with col7:
    st.metric(label="Total des avions", value=cancellation_data['total_planes'])

st.markdown("<h3 style='color: #003399;'>🚫 Vols annulés :</h3>", unsafe_allow_html=True)
st.metric(label="Vols annulés", value=cancellation_data['cancelled_flights'])

# Affichage des 10 destinations les plus prisées
st.markdown("<h3 style='color: #003399;'>🏆 10 destinations les plus prisées :</h3>", unsafe_allow_html=True)
st.dataframe(top_destinations_info)

# Affichage des 10 destinations les moins prisées
st.markdown("<h3 style='color: #003399;'>🌍 10 destinations les moins prisées :</h3>", unsafe_allow_html=True)
st.dataframe(bottom_destinations_info)

# Graphique des 10 destinations les plus prisées
st.markdown("<h3 style='color: #003399;'>📊 Graphique des 10 destinations les plus prisées :</h3>", unsafe_allow_html=True)
fig, ax = plt.subplots(figsize=(10, 5))
ax.bar(top_destinations_info['Destination'], top_destinations_info['Nombre de vols'], color='#33c3ff')
ax.set_title("10 destinations les plus prisées", fontsize=14, color='#003399')
ax.set_xlabel("Destination", fontsize=12, color='#003399')
ax.set_ylabel("Nombre de vols", fontsize=12, color='#003399')
plt.xticks(rotation=45)
st.pyplot(fig)

# Graphique des 10 destinations les moins prisées
st.markdown("<h3 style='color: #003399;'>📉 Graphique des 10 destinations les moins prisées :</h3>", unsafe_allow_html=True)
fig, ax = plt.subplots(figsize=(10, 5))
ax.bar(bottom_destinations_info['Destination'], bottom_destinations_info['Nombre de vols'], color='#ff6666')
ax.set_title("10 destinations les moins prisées", fontsize=14, color='#003399')
ax.set_xlabel("Destination", fontsize=12, color='#003399')
ax.set_ylabel("Nombre de vols", fontsize=12, color='#003399')
plt.xticks(rotation=45)
st.pyplot(fig)

# Barre latérale avec options supplémentaires
st.sidebar.header("🔧 Options")
st.sidebar.markdown("Utilisez les options ci-dessous pour filtrer les données.")

# Séparateur graphique
st.markdown("<hr style='border-top: 3px solid #33c3ff;'>", unsafe_allow_html=True)
