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
def insert_data_commission_collecte(data):
    conn = connect_db()
    if conn is None:
        return

    cursor = conn.cursor()

    query = """
        INSERT INTO com_collecte 
        (agence, collectes, commissions, date, institution)
        VALUES (%s, %s, %s, %s,  %s)
    """
    
    total_inserted = 0
    for index, row in data.iterrows():
        
        values = (
            row.get('agence'),
            row.get('collectes'),
            row.get('commissions'),
            row.get("date"),
            row.get("institution"),
        )
        
        try:
            cursor.execute(query, values)
            conn.commit()
            total_inserted += 1
        except mariadb.Error as e:
            st.error(f"Erreur lors de l'insertion de la ligne {index} : {e}")
    
    conn.close()
    st.success(f"{total_inserted} ligne(s) insérée(s) dans la base de données avec succès !")
