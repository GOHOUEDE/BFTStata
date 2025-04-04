import streamlit as st
import datetime
from Requete.requete_ace_sfi import get_ace_sfi, get_usernames, get_agence_ace_sfi, get_filtered_data_ace_sfi

def get_suivi_ace_sfi():
    st.subheader("📊 Filtrer les données ACE SFI")
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
    
    if st.button("🔍 Filtrer les ACE & SFI", key="bouton_ace_sfi"):
        filtered_data = get_filtered_data_ace_sfi(institution, username, ace_sfi, date_debut, date_fin)
        if not filtered_data.empty:
            st.write("### 📋 Résultats filtrés :")
            st.dataframe(filtered_data)
        else:
            st.warning("Aucune donnée ne correspond aux critères sélectionnés.")
