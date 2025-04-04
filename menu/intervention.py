# Intervention.py
import streamlit as st
import datetime
from Requete.requete_intervention import get_institutions, get_filtered_data, get_agences

def get_intervention():
    st.subheader("📌 Filtrer les interventions")
    with st.container():
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            institutions = get_institutions()
            institution = st.selectbox("🏦 Institution", ["Toutes"] + institutions if institutions else ["Toutes"], key="institution_select_intervention")
        with col2:
            agences = get_agences(institution)
            agence = st.selectbox("🏢 Agence", ["Toutes"] + agences if agences else ["Toutes"], key="agence_intervention")
        with col3:
            date_debut = st.date_input("📆 Date de début", value=datetime.date.today(), key="date_debut_intervention")
        with col4:
            date_fin = st.date_input("📆 Date de fin", value=date_debut, key="date_fin_intervention")
    
    if date_fin < date_debut:
        st.error("⚠️ La date de fin ne peut pas être avant la date de début.")

    if st.button("🔍 Filtrer les interventions", key="bouton_intervention"):
        filtered_data = get_filtered_data(institution, agence, date_debut, date_fin)
        if not filtered_data.empty:
            st.write("### 📋 Résultats filtrés :")
            st.dataframe(filtered_data)
        else:
            st.warning("Aucune donnée ne correspond aux critères sélectionnés.")
