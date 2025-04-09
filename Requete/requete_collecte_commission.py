import streamlit as st
import pandas as pd
import datetime
from donnees.connexiondb import connect_db  

# Fonction pour récupérer les institutions disponibles
def get_com_collecte():
    conn = connect_db()
    if conn is None:
        return ["Toutes"]
    
    cursor = conn.cursor()
    cursor.execute("SELECT DISTINCT institution FROM com_collecte")
    results = cursor.fetchall()
    cursor.close()
    conn.close()

    return ["Toutes"] + [row[0] for row in results]

# Fonction pour récupérer les agences selon l'institution sélectionnée
def get_agences_com_collecte(institution):
    conn = connect_db()
    if conn is None:
        return ["Toutes"]
    
    cursor = conn.cursor()
    
    if institution == "Toutes":
        cursor.execute("SELECT DISTINCT agence FROM com_collecte")
    else:
        cursor.execute("SELECT DISTINCT agence FROM com_collecte WHERE institution = %s", (institution,))
    
    results = cursor.fetchall()
    cursor.close()
    conn.close()

    return ["Toutes"] + [row[0] for row in results]

# Fonction pour récupérer les données filtrées
def get_filtered_data_collecte(institution, agence, date_debut, date_fin, data_type):
    conn = connect_db()
    if conn is None:
        return pd.DataFrame()
    
    cursor = conn.cursor()

    query = """
        SELECT institution, agence, collectes, commissions, date 
        FROM com_collecte 
        WHERE DATE(date) BETWEEN %s AND %s
    """
    params = [date_debut.strftime('%Y-%m-%d'), date_fin.strftime('%Y-%m-%d')]  # Conversion des dates

    if institution != "Toutes":
        query += " AND institution = %s"
        params.append(institution)
    
    if agence != "Toutes":
        query += " AND agence = %s"
        params.append(agence)
    
    if data_type == "Commission":
        query += " AND commissions IS NOT NULL"  
    elif data_type == "Collecte":
        query += " AND collectes IS NOT NULL"
    
    cursor.execute(query, tuple(params))
    results = cursor.fetchall()
    cursor.close()
    conn.close()

    return pd.DataFrame(results, columns=["Institution", "Agence", "Collectes", "Commissions", "Date"])

