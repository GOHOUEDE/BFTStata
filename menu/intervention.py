# Intervention.py
import streamlit as st
import datetime
import pandas as pd
from Requete.requete_intervention import (
    get_institutions, get_filtered_data, get_agences,
    get_type_intervention, get_etat_intervention
)
from graphiques.nuages_inter import nuages_inter, nua_inter

def get_intervention():
    st.subheader("📌 Filtrer les interventions")
    with st.container():
        col1, col2, col3, col4, col5, col6 = st.columns(6)
        
        with col1:
            institutions = get_institutions()
            institution = st.selectbox("🏦 Institution", ["Toutes"] + institutions if institutions else ["Toutes"], key="institution_select_intervention")
        with col2:
            agences = get_agences(institution)
            agence = st.selectbox("🏢 Agence", ["Toutes"] + agences if agences else ["Toutes"], key="agence_intervention")
        with col3:
            interventions = get_type_intervention(institution, agence)
            intervention = st.selectbox("🛠 Intervention", ["Tous"] + interventions if interventions else [""], key="type_intervention")   
        with col4:
            etats = get_etat_intervention(institution, agence, intervention)
            etat = st.selectbox("📋 État", ["Toutes"] + etats if etats else [""], key="etat_intervention")       
        with col5:
            date_debut = st.date_input("📆 Date de début", value=datetime.date.today(), key="date_debut_intervention")
        with col6:
            date_fin = st.date_input("📆 Date de fin", value=datetime.date.today(), key="date_fin_intervention")
    
    if date_fin < date_debut:
        st.error("⚠️ La date de fin ne peut pas être avant la date de début.")
        return

    if st.button("🔍 Filtrer les interventions", key="bouton_intervention"):
        filtered_data = get_filtered_data(institution, agence, intervention, etat, date_debut, date_fin)

        if filtered_data.empty:
            st.warning("Aucune donnée ne correspond aux critères sélectionnés.")
            return
        
        st.write("### 📋 Résultats filtrés :")
        st.dataframe(filtered_data)

        # Vérification colonne Date
        if "Date" not in filtered_data.columns:
            st.error("⚠️ La colonne 'Date' est manquante dans les données récupérées.")
            return
        
        # Convertir en datetime
        filtered_data["Date"] = pd.to_datetime(filtered_data["Date"], errors='coerce')
        filtered_data.dropna(subset=["Date"], inplace=True)

        # Grouper par mois
        grouped_data = (
            filtered_data.groupby(filtered_data["Date"].dt.to_period("M"))
            .size()
            .reset_index(name="Nb_interventions")
        )
        grouped_data["Date"] = grouped_data["Date"].dt.to_timestamp()

        # Affichage des graphiques
        x = grouped_data["Date"]
        y = grouped_data["Nb_interventions"]

        st.subheader("📈 Évolution mensuelle des interventions")
        nuages_inter(x, y)
        nua_inter(grouped_data)
