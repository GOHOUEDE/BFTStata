import streamlit as st
import datetime
from Requete.requete_ace_sfi import get_ace_sfi, get_usernames, get_agence_ace_sfi, get_filtered_data_ace_sfi
from graphiques.nuages_suivi_ace import nuages, nua

def get_suivi_ace_sfi():
    st.subheader("📊 Filtrer les données ACE SFI")
    with st.container():
        col1, col2, col3, col4, col5 = st.columns(5)
        with col1:
            # Utiliser une clé unique pour cette section
            institution = st.selectbox("🏦 Institution", get_ace_sfi(), key="ace_sfi_suivi")
        with col2:
            username = st.selectbox("👤 Utilisateur", get_usernames(), key="username_ace_sfi_suivi")
        with col3:
            ace_sfi = st.selectbox("🏢 Type", get_agence_ace_sfi(), key="ace_sfi_ace_sfi_suivi")
        with col4:
            date_debut = st.date_input("📆 Date de début", value=datetime.date.today(), key="date_debut_ace_sfi_suivi")
        with col5:
            date_fin = st.date_input("📆 Date de fin", value=datetime.date.today(), key="date_fin_ace_sfi_suivi")
        
        if date_fin < date_debut:
            st.error("⚠️ La date de fin ne peut pas être avant la date de début.")
    
    if st.button("🔍 Filtrer les ACE & SFI", key="bouton_ace_sfi_suivi"):
        filtered_data = get_filtered_data_ace_sfi(institution, username, ace_sfi, date_debut, date_fin)
        
        # Afficher pour déboguer
        # st.write("Colonnes du DataFrame:", filtered_data.columns.tolist())
        
        if not filtered_data.empty:
            st.write("### 📋 Résultats filtrés :")
            st.dataframe(filtered_data)
            
            # Filtrer le DataFrame pour ne garder que les lignes où la colonne 'ace_sfi' correspond à la sélection
            if "ace_sfi" in filtered_data.columns:
                filtered_data = filtered_data[filtered_data["ace_sfi"] == ace_sfi]
                
                if not filtered_data.empty:
                    # Supposons que la colonne "commission" est bien nommée ainsi et "Date" pour la date
                    if "commission" in filtered_data.columns and "date" in filtered_data.columns:
                        nuages(filtered_data["date"], filtered_data["commission"])
                        nua(filtered_data)
                    else:
                        st.error("Les colonnes 'commission' ou 'Date' sont introuvables dans les résultats.")
                else:
                    st.warning("Aucune donnée ne correspond à la valeur sélectionnée dans 'ace_sfi'.")
            else:
                st.error("La colonne 'ace_sfi' n'existe pas dans les résultats.")
        else:
            st.warning("Aucune donnée ne correspond aux critères sélectionnés.")

# Appel de la fonction dans le script principal
# get_suivi_ace_sfi()
