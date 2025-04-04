import streamlit as st
import mariadb
import pandas as pd

# Fonction pour récupérer les données d'une colonne spécifique
def get_column_values(column_name, table_name):
    try:
        # Connexion à la base de données
        conn = mariadb.connect(
            host="localhost",
            user="root",
            password="",
            database="Statistic_projet",
            port=3307
        )
        cursor = conn.cursor()

        # Exécuter la requête pour récupérer une colonne spécifique
        query = f"SELECT DISTINCT {column_name} FROM {table_name}"
        cursor.execute(query)
        results = cursor.fetchall()  # Récupérer toutes les valeurs

        # Fermer la connexion
        cursor.close()
        conn.close()

        # Transformer les résultats en une liste
        return [row[0] for row in results]
    
    except mariadb.Error as e:
        st.error(f"Erreur de base de données : {e}")
        return []

# Interface Streamlit
st.title("📋 Sélectionner une Institution")

# Récupérer les valeurs de la colonne "institution"
institutions = get_column_values("institution", "interventions")

# Vérifier si des données sont récupérées
if institutions:
    selected_institution = st.selectbox("🏦 Choisissez une institution :", institutions)
    st.success(f"Vous avez sélectionné : {selected_institution}")
else:
    st.warning("Aucune institution trouvée dans la base de données.")
