import streamlit as st
import pandas as pd
import datetime
from donnees.connexiondb import connect_db  

# Fonction pour récupérer les institutions disponibles
def get_ace_sfi():
    conn = connect_db()
    if conn is None:
        return ["Toutes"]
    
    cursor = conn.cursor()
    cursor.execute("SELECT DISTINCT institution FROM ace_sfi")
    results = cursor.fetchall()
    cursor.close()
    conn.close()
    return ["Toutes"] + [row[0] for row in results]

# Fonction pour récupérer les utilisateurs disponibles
def get_usernames():
    conn = connect_db()
    if conn is None:
        return ["Tous"]
    
    cursor = conn.cursor()
    cursor.execute("SELECT DISTINCT username FROM ace_sfi")
    results = cursor.fetchall()
    cursor.close()
    conn.close()
    return ["Tous"] + [str(row[0]) for row in results]

# Fonction pour récupérer les valeurs ACE SFI
def get_agence_ace_sfi():
    return ["Tous", "ACE", "SFI"]

# Fonction pour récupérer les données filtrées avec toutes les colonnes
def get_filtered_data_ace_sfi(institution, username, ace_sfi, date_debut, date_fin):
    conn = connect_db()
    if conn is None:
        return pd.DataFrame()
    
    cursor = conn.cursor()
    query = """
        SELECT username, nom_prenom, collecte, commission, date, institution, ace_sfi
        FROM ace_sfi 
        WHERE DATE(date) BETWEEN %s AND %s
    """
    params = [date_debut.strftime('%Y-%m-%d'), date_fin.strftime('%Y-%m-%d')]
    
    if institution != "Toutes":
        query += " AND institution = %s"
        params.append(institution)
    
    if username != "Tous":
        query += " AND username = %s"
        params.append(username)
    
    if ace_sfi != "Tous":
        query += " AND ace_sfi = %s"
        params.append(ace_sfi)
    
    cursor.execute(query, tuple(params))
    results = cursor.fetchall()
    cursor.close()
    conn.close()
    
    return pd.DataFrame(results, columns=["username", "nom_prenom", "collecte", "commission", "date", "institution", "ace_sfi"])

# Fonction principale pour afficher l'interface de filtrage
def afficher_filtre_ace_sfi():
    st.title("📊 Filtrer les données ACE SFI")
    with st.container():
        col1, col2, col3, col4, col5 = st.columns(5)
        
        with col1:
            institution = st.selectbox("🏦 Institution", get_ace_sfi(), key="institution_ace_sfi")
        with col2:
            username = st.selectbox("👤 Utilisateur", get_usernames(), key="username_ace_sfi")
        with col3:
            ace_sfi = st.selectbox("🏢 ACE SFI", get_agence_ace_sfi(), key="ace_sfi_ace_sfi")
        with col4:
            date_debut = st.date_input("📆 Date de début", value=datetime.date.today(), key="date_debut_ace_sfi")
        with col5:
            date_fin = st.date_input("📆 Date de fin", value=datetime.date.today(), key="date_fin_ace_sfi")
        
        if date_fin < date_debut:
            st.error("⚠️ La date de fin ne peut pas être avant la date de début.")
    
    if st.button("🔍 Filtrer les données", key="bouton_filtrer_ace_sfi"):
        filtered_data = get_filtered_data_ace_sfi(
            st.session_state.institution_ace_sfi,
            st.session_state.username_ace_sfi,
            st.session_state.ace_sfi_ace_sfi,
            st.session_state.date_debut_ace_sfi,
            st.session_state.date_fin_ace_sfi
        )
        
        if not filtered_data.empty:
            st.write("### 📋 Résultats filtrés :")
            st.dataframe(filtered_data)
        else:
            st.warning("Aucune donnée ne correspond aux critères sélectionnés.")

# Appel de la fonction pour lancer l'interface
# afficher_filtre_ace_sfi()
