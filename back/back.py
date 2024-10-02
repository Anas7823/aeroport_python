# Importation des bibliothèques
from sqlalchemy import create_engine, text

# Informations de connexion
DB_USER = 'postgres'
DB_PASSWORD = 'postgres'
DB_HOST = 'localhost'
DB_PORT = '5432'  # Mets bien 5432 si c'est le port PostgreSQL par défaut
DB_NAME = 'aeroport'

# Connexion via SQLAlchemy
engine = create_engine(f'postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}')

# Fonction back-end avec SQLAlchemy pour compter les aéroports
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

 
# Fonction pour compter les aéroports de départ et de destination
def count_airports(cursor):
    query = """
    SELECT
        (SELECT COUNT(*) FROM airports) AS total_airports,
        (SELECT COUNT(DISTINCT origin) FROM flights) AS departure_airports,
        (SELECT COUNT(DISTINCT dest) FROM flights) AS destination_airports;
    """
    cursor.execute(query)
    result = cursor.fetchone()
    
    total_airports = result[0]
    departure_airports = result[1]
    destination_airports = result[2]
    
    print(f"Total des aéroports : {total_airports}")
    print(f"Aéroports de départ : {departure_airports}")
    print(f"Aéroports de destination : {destination_airports}")
 
# Fonction pour compter les aéroports sans heure d'été et les fuseaux horaires
def count_airports_without_dst_and_timezones(cursor):
    query_airports_without_dst = """
    SELECT COUNT(*) AS airports_without_dst
    FROM airports
    WHERE dst = 'N';
    """
    
    query_time_zones = """
    SELECT COUNT(DISTINCT tz) AS time_zones
    FROM airports;
    """
    
    cursor.execute(query_airports_without_dst)
    airports_without_dst = cursor.fetchone()[0]
    
    cursor.execute(query_time_zones)
    time_zones = cursor.fetchone()[0]
    
    print(f"Aéroports sans passage à l'heure d'été : {airports_without_dst}")
    print(f"Nombre de fuseaux horaires : {time_zones}")
 
def count_companies_planes_cancelled_flights(cursor):
    query = """
    SELECT
        (SELECT COUNT(*) FROM airlines) AS total_airlines,
        (SELECT COUNT(*) FROM planes) AS total_planes,
        (SELECT COUNT(*) FROM flights WHERE arr_delay IS NULL) AS cancelled_flights;  -- Vols annulés (pas de temps d'arrivée)
    """
    
    cursor.execute(query)
    result = cursor.fetchone()
    
    total_airlines = result[0]
    total_planes = result[1]
    cancelled_flights = result[2]
    
    # Affichage des résultats
    print(f"Total des compagnies aériennes : {total_airlines}")
    print(f"Total des avions : {total_planes}")
    print(f"Total des vols annulés : {cancelled_flights}")
 
def popular_and_least_popular_airports(cursor):
    # Requête pour l'aéroport de départ le plus emprunté
    query_most_used_origin = """
    SELECT origin, COUNT(*) AS flight_count
    FROM flights
    GROUP BY origin
    ORDER BY flight_count DESC
    LIMIT 1;
    """
 
    # Requête pour les 10 destinations les plus prisées
    query_top_10_destinations = """
    SELECT dest, COUNT(*) AS flight_count
    FROM flights
    GROUP BY dest
    ORDER BY flight_count DESC
    LIMIT 10;
    """
 
    # Requête pour les 10 destinations les moins prisées
    query_bottom_10_destinations = """
    SELECT dest, COUNT(*) AS flight_count
    FROM flights
    GROUP BY dest
    ORDER BY flight_count ASC
    LIMIT 10;
    """
    
    cursor.execute(query_most_used_origin)
    most_used_origin = cursor.fetchone()
    
    cursor.execute(query_top_10_destinations)
    top_10_destinations = cursor.fetchall()
    
    cursor.execute(query_bottom_10_destinations)
    bottom_10_destinations = cursor.fetchall()
    
    print(f"Aéroport de départ le plus emprunté : {most_used_origin[0]} avec {most_used_origin[1]} vols")
 
    print("\n10 destinations les plus prisées :")
    for dest in top_10_destinations:
        print(f"Destination : {dest[0]} avec {dest[1]} vols")
    
    print("\n10 destinations les moins prisées :")
    for dest in bottom_10_destinations:
        print(f"Destination : {dest[0]} avec {dest[1]} vols")
 
def destinations_by_carrier(cursor):
    # Requête SQL pour compter le nombre de destinations desservies par chaque compagnie
    query = """
    SELECT carrier, COUNT(DISTINCT dest) AS destination_count
    FROM flights
    GROUP BY carrier;
    """
    
    cursor.execute(query)
    results = cursor.fetchall()
    
    print("Nombre de destinations desservies par chaque compagnie :")
    for carrier, destination_count in results:
        print(f"Compagnie : {carrier}, Destinations desservies : {destination_count}")
 
def flights_to_houston(cursor):
    # Requête SQL pour obtenir les vols ayant atterri à Houston (IAH ou HOU)
    query = """
    SELECT *
    FROM flights
    WHERE dest IN ('IAH', 'HOU');
    """
    
    cursor.execute(query)
    results = cursor.fetchall()
    
    print("Vols ayant atterri à Houston (IAH ou HOU) :")
    for flight in results:
        print(flight)
 
def flights_nyc_to_seattle(cursor):
    # Requête SQL pour compter les vols de NYC (JFK, LGA, EWR) à Seattle (SEA)
    query = """
    SELECT
        COUNT(*) AS flights_from_nyc_to_seattle,
        COUNT(DISTINCT carrier) AS unique_carriers,
        COUNT(DISTINCT tailnum) AS unique_planes
    FROM flights
    WHERE origin IN ('JFK', 'LGA', 'EWR') AND dest = 'SEA';
    """
    
    cursor.execute(query)
    result = cursor.fetchone()
    
    flights_count = result[0]
    unique_carriers = result[1]
    unique_planes = result[2]
    
    print(f"Nombre de vols de NYC à Seattle : {flights_count}")
    print(f"Nombre de compagnies distinctes : {unique_carriers}")
    print(f"Nombre d'avions distincts : {unique_planes}")
 
def flights_by_destination(cursor):
    # Requête SQL pour obtenir le nombre de vols par destination
    query = """
    SELECT dest, COUNT(*) AS flight_count
    FROM flights
    GROUP BY dest
    ORDER BY flight_count DESC;
    """
    
    cursor.execute(query)
    results = cursor.fetchall()
    
    print("Nombre de vols par destination :")
    for dest, flight_count in results:
        print(f"Destination : {dest}, Nombre de vols : {flight_count}")
 
def airlines_not_operating_on_all_airports(cursor):
    # Requête SQL pour obtenir les compagnies qui n'opèrent pas sur tous les aéroports d'origine
    query = """
    SELECT carrier
    FROM airline_airport_routes
    GROUP BY carrier
    HAVING COUNT(DISTINCT faa) < (SELECT COUNT(*) FROM airports);
    """
    
    cursor.execute(query)
    results = cursor.fetchall()
    
    print("Compagnies qui n'opèrent pas sur tous les aéroports d'origine :")
    for carrier in results:
        print(f"Compagnie : {carrier[0]}")
 
def airlines_serving_all_destinations(cursor):
    # Requête SQL pour obtenir les compagnies qui desservent toutes les destinations
    query = """
    SELECT carrier
    FROM airline_airport_routes
    GROUP BY carrier
    HAVING COUNT(DISTINCT faa) = (SELECT COUNT(DISTINCT faa) FROM airports);
    """
    
    cursor.execute(query)
    results = cursor.fetchall()
    
    print("Compagnies qui desservent l'ensemble des destinations :")
    for carrier in results:
        print(f"Compagnie : {carrier[0]}")
 
def all_origins_destinations_by_airline(cursor):
    # Requête SQL pour obtenir l'ensemble des origines et des destinations pour chaque compagnie
    query = """
    SELECT DISTINCT a.origin, a.dest, l.name AS airline_name
    FROM airline_airport_routes r
    JOIN airlines l ON r.carrier = l.carrier
    JOIN flights a ON r.faa = a.origin;
    """
    
    cursor.execute(query)
    results = cursor.fetchall()
    
    print(f"{'Origine':<10} {'Destination':<15} {'Compagnie Aérienne':<20}")
    print("="*50)
    for origin, dest, airline_name in results:
        print(f"{origin:<10} {dest:<15} {airline_name:<20}")
 
def exclusive_destinations_by_airline(cursor):
    # Requête SQL pour obtenir les destinations exclusives à certaines compagnies
    query = """
    SELECT dest
    FROM flights
    GROUP BY dest
    HAVING COUNT(DISTINCT carrier) = 1;
    """
    
    cursor.execute(query)
    results = cursor.fetchall()
    
    print("Destinations exclusives à certaines compagnies :")
    for dest in results:
        print(f"Destination : {dest[0]}")
 
def flights_by_united_american_delta(cursor):
    # Requête SQL pour obtenir les vols exploités par United, American ou Delta
    query = """
    SELECT *
    FROM flights
    WHERE carrier IN ('UA', 'AA', 'DL');
    """
    
    cursor.execute(query)
    results = cursor.fetchall()
    
    print("Vols exploités par United, American ou Delta :")
    for flight in results:
        print(flight)
 
 
 
 
 
 
 
 
# Main pour exécuter les fonctions avec connexion
if __name__ == "__main__":
    try:
        connection = psycopg2.connect(
            host=host,
            port=port,
            dbname=dbname,
            user=user,
            password=password
        )
 
        # Créer un curseur pour exécuter les requêtes SQL
        cursor = connection.cursor()
 
        #count_airports(cursor)
        count_airports_without_dst_and_timezones(cursor)
        #count_companies_planes_cancelled_flights(cursor)
        #popular_and_least_popular_airports(cursor)
        #destinations_by_carrier(cursor)
        #flights_to_houston(cursor)
        #flights_nyc_to_seattle(cursor)
        #flights_by_destination(cursor)
        #airlines_not_operating_on_all_airports(cursor)
        #airlines_serving_all_destinations(cursor)
        #all_origins_destinations_by_airline(cursor)
        #exclusive_destinations_by_airline(cursor)
        #flights_by_united_american_delta(cursor)
        
        
 
 
 
        # Fermer le curseur et la connexion
        cursor.close()
        connection.close()
 
    except Exception as e:
        print(f"Erreur de connexion à la base de données PostgreSQL : {e}")