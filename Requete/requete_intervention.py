import streamlit as st
import mariadb
import pandas as pd
import datetime
from donnees.connexiondb import connect_db  

# Fonction pour récupérer les institutions disponibles
def get_institutions():
    conn = connect_db()
    if conn is None:
        return ["Toutes"]
    
    cursor = conn.cursor()
    cursor.execute("SELECT DISTINCT institution FROM interventions")
    results = cursor.fetchall()
    cursor.close()
    conn.close()

    return [row[0] for row in results]
# Fonction pour récupérer les institutions disponibles
def get_type_intervention(institution,agence):
    conn = connect_db()
    if conn is None:
        return ["Toutes"]
    
    cursor = conn.cursor()
    
    if agence == "Toutes":
        cursor.execute("SELECT DISTINCT problemes FROM interventions")
    else:
        cursor.execute("SELECT DISTINCT problemes FROM interventions WHERE institution = %s AND agence = %s", (institution,agence,))
    
    results = cursor.fetchall()
    cursor.close()
    conn.close()

    return  [row[0] for row in results]

def get_etat_intervention(institution,agence,intervention):
    conn = connect_db()
    if conn is None:
        return ["Toutes"]
    
    cursor = conn.cursor()
    
    if agence == "Toutes":
        cursor.execute("SELECT DISTINCT etat_intervention FROM interventions")
    else:
        cursor.execute("SELECT DISTINCT etat_intervention FROM interventions WHERE institution = %s AND agence = %s AND etat_intervention = %s", (institution,agence,intervention,))
    
    results = cursor.fetchall()
    cursor.close()
    conn.close()

    return  [row[0] for row in results]

# Fonction pour récupérer les agences selon l'institution sélectionnée
def get_agences(institution):
    conn = connect_db()
    if conn is None:
        return ["Toutes"]
    
    cursor = conn.cursor()
    
    if institution == "Toutes":
        cursor.execute("SELECT DISTINCT agence FROM interventions")
    else:
        cursor.execute("SELECT DISTINCT agence FROM interventions WHERE institution = %s", (institution,))
    
    results = cursor.fetchall()
    cursor.close()
    conn.close()

    return  [row[0] for row in results]

# Fonction pour récupérer les données filtrées
def get_filtered_data(institution, agence, intervention, etat, date_debut, date_fin):
    conn = connect_db()
    if conn is None:
        return pd.DataFrame()
    
    cursor = conn.cursor()
    
    query = """
        SELECT institution, agence, intervention_date, etat_intervention, problemes 
        FROM interventions 
        WHERE DATE(intervention_date) BETWEEN %s AND %s 
    """
    params = [date_debut.strftime('%Y-%m-%d'), date_fin.strftime('%Y-%m-%d')]  # Conversion des dates

    if institution != "Toutes":
        query += " AND institution = %s"
        params.append(institution)
    
    if agence != "Toutes":
        query += " AND agence = %s"
        params.append(agence)
        
    if intervention != "Tous":
        query += " AND problemes = %s"
        params.append(intervention)
        
    if etat != "Toutes":
        query += " AND etat_intervention = %s"
        params.append(etat)    
    
    cursor.execute(query, tuple(params))
    results = cursor.fetchall()
    cursor.close()
    conn.close()

    return pd.DataFrame(results, columns=["Institution", "Agence", "Date", "État", "Interventions"])
