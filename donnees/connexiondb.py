import mariadb
import streamlit as st

# Fonction pour se connecter à la base de données
def connect_db():
    try:
        conn = mariadb.connect(
            host="localhost",
            user="root",
            password="",
            database="Statistic_projet",
            port=3307
        )
        return conn
    except mariadb.Error as e:
        st.error(f"Erreur de connexion à la base de données : {e}")
        return None
