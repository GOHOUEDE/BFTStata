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

    return ["Toutes"] + [row[0] for row in results]

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

    return ["Toutes"] + [row[0] for row in results]

# Fonction pour récupérer les données filtrées
def get_filtered_data(institution, agence, date_debut, date_fin):
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
    
    cursor.execute(query, tuple(params))
    results = cursor.fetchall()
    cursor.close()
    conn.close()

    return pd.DataFrame(results, columns=["Institution", "Agence", "Date Intervention", "État", "Problèmes"])

# Interface Streamlit
st.title("📊 Filtrer les interventions")

# Conteneur pour le filtre
with st.container():
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        institutions = get_institutions()
        institution = st.selectbox("🏦 Institution", institutions, key="institution_select")

    with col2:
        agences = get_agences(institution)
        agence = st.selectbox("🏢 Agences", agences, key="agence_select")

    with col3:
        date_debut = st.date_input("📆 Date de début", value=datetime.date.today(), key="date_debut")

    with col4:
        date_fin = st.date_input("📆 Date de fin", value=datetime.date.today(), key="date_fin")

    # Vérification de la cohérence des dates
    if date_fin < date_debut:
        st.error("⚠️ La date de fin ne peut pas être avant la date de début.")

# Bouton pour lancer la recherche
if st.button("🔍 Filtrer les données"):
    filtered_data = get_filtered_data(institution, agence, date_debut, date_fin)
    
    if not filtered_data.empty:
        st.write("### 📋 Résultats filtrés :")
        st.dataframe(filtered_data)
    else:
        st.warning("Aucune donnée ne correspond aux critères sélectionnés.")
