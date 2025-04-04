# CollecteCommission.py
import streamlit as st
import datetime
from graphiques.nuages import nuages,nua
from Requete.requete_collecte_commission import (
    get_com_collecte as get_com_collecte_data, 
    get_agences_com_collecte, 
    get_filtered_data_collecte
)

def afficher_filtre_collecte_commission():
    st.subheader("📊 Filtrer les collectes et commissions")
    with st.container():
        col1, col2, col3, col4, col5 = st.columns(5)
        
        with col1:
            # Utilisation de l'import aliasé pour éviter le conflit
            institutions = get_com_collecte_data()
            institution = st.selectbox("🏦 Institution", institutions, key="institution_select_collecte")
        
        with col2:
            agences = get_agences_com_collecte(institution)
            agence = st.selectbox("🏢 Agences", agences, key="agence_select_collecte")
        
        with col3:
            date_debut = st.date_input("📆 Date de début", value=datetime.date.today(), key="date_debut_collecte")
        
        with col4:
            date_fin = st.date_input("📆 Date de fin", value=datetime.date.today(), key="date_fin_collecte")
        
        with col5:
            data_type = st.selectbox("📊 Type de Donnée", ["Commission", "Collecte"], key="data_type_select_collecte")
        
        if date_fin < date_debut:
            st.error("⚠️ La date de fin ne peut pas être avant la date de début.")
    
    if st.button("🔍 Filtrer les collectes commissions", key="bouton_collecte"):
        filtered_data = get_filtered_data_collecte(institution, agence, date_debut, date_fin, data_type)
        if data_type == "Commission":
            nuages(filtered_data.Date,filtered_data.Commissions)
            nua(filtered_data)
        elif data_type == "Collecte":
            nuages(filtered_data.Date,filtered_data.Collectes) 
        else:
            nuages(filtered_data.Date,filtered_data.Collectes)
            nuages(filtered_data.Date,filtered_data.Commissions)
                    
        
        st.subheader("📊 Graphiques")
        
        if not filtered_data.empty:
            st.write("### 📋 Résultats filtrés :")
            st.dataframe(filtered_data)
        else:
            st.warning("Aucune donnée ne correspond aux critères sélectionnés.")
