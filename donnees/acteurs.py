
import streamlit as st
import pandas as pd
import mariadb
import re  # Pour traiter les heures

# Fonction de connexion à la base de données
def connect_db():
    try:
        conn = mariadb.connect(
            host="localhost",
            user="root",
            password="",
            database="Statistic_projet",
            port=3307,
            connect_timeout=5
        )
        conn.autocommit = True
        return conn
    except mariadb.Error as e:
        st.error(f"Erreur de connexion à la base de données : {e}")
        return None

# Fonction pour formater l'heure en HH:MM:SS
def format_time(value):
    if pd.isna(value) or value in [None, "", "0"]:
        return None  # On renvoie NULL si la valeur est vide ou incorrecte
    
    # Essayer d'extraire une heure correcte (ex: 12h00 -> 12:00:00)
    match = re.match(r"(\d{1,2})[hH:](\d{1,2})", str(value))
    if match:
        hours, minutes = match.groups()
        return f"{int(hours):02}:{int(minutes):02}:00"
    
    return None  # Retourne NULL si le format est incorrect

# Fonction d'insertion des données dans la BDD
def insert_data_acteur(data):
    conn = connect_db()
    if conn is None:
        return

    cursor = conn.cursor()

    query = """
        INSERT INTO interventions 
        (pays, institution, intervention_date, intervention_time, etat_intervention, agence, 
         problemes, solutions_proposees, solutions_finales, date_solution, heure_solution, observations_qu_bureau)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    """
    
    total_inserted = 0
    for index, row in data.iterrows():
        obs_bool = 1 if row.get('Observations') in [1, '1', True, 'True'] else 0
        
        values = (
            row.get('pays'),
            row.get('institution'),
            row.get('intervention_date'),
            format_time(row.get('intervention_time')),
            row.get("etat_intervention"),
            row.get('agence'),
            row.get('problèmes'),
            row.get('solutions_proposees'),
            row.get('solutions_finales'),
            row.get('date_solution'),
            format_time(row.get('heure_solution')),
            obs_bool
        )
        
        try:
            cursor.execute(query, values)
            conn.commit()
            total_inserted += 1
        except mariadb.Error as e:
            st.error(f"Erreur lors de l'insertion de la ligne {index} : {e}")
    
    conn.close()
    st.success(f"{total_inserted} ligne(s) insérée(s) dans la base de données avec succès !")
