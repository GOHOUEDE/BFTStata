import streamlit as st
import pandas as pd
import datetime
from streamlit_option_menu import option_menu
import os
from donnees.interventions import insert_data_to_db
from donnees.commission_collecte import insert_data_commission_collecte
from donnees.ace_sfi import insert_data_ace_sfi
from donnees.acteurs import insert_data_acteur
from menu.intervention import get_intervention
from menu.com_collecte import afficher_filtre_collecte_commission
from menu.suivi_ace_sfi import get_suivi_ace_sfi
from graphiques.nuages import nuages


# Sidebar - Image et menu de navigation
with st.sidebar:
    image_path = "images/logo.png"
    if os.path.exists(image_path):
        st.image(image_path, width=150)
    else:
        st.error("⚠️ L'image n'existe pas ! Vérifiez le chemin.")
    
    st.markdown(
    """
    <style>
        .css-1d391kg {
            font-size: 14px !important;
            font-weight: bold !important;
            color: #4CAF50 !important;
        }
        .css-1d391kg:hover {
            color: #FF5722 !important;
        }
    </style>
    """, unsafe_allow_html=True)

    selected = option_menu(
        "",
        ["Home", "Collectes & Commissions", "Suivi et analyse des acteurs",  
         "Suivi des ACE & SFI", "Intervention", "Charger les données", "Settings"],
        icons=['house', 'bar-chart', 'pie-chart', 'database', 'wrench', 'database', 'gear'],
        menu_icon="cast",
        default_index=1,
        styles={
            "container": {"padding": "5!important", "background-color": "#f5f5f5"},
            "icon": {"color": "#4CAF50", "font-size": "18px"},
            "nav-link": {
                "font-size": "12px",
                "text-align": "left",
                "margin": "0px",
                "color": "black",
                "--hover-color": "#eee",
            },
            "nav-link-selected": {"background-color": "rgb(129 196 92)", "color": "white"},
        }
    )

# --- Charger les données ---
if selected == "Charger les données":
    # Interface utilisateur pour charger les données
    uploaded_file = st.file_uploader("Téléchargez les données d'interventions", type=["xlsx", "xls"])
    if uploaded_file is not None:
        try:
            data = pd.read_excel(uploaded_file)
            with st.expander("🔍 Voir les données importées"):
                st.dataframe(data, height=300)
            if st.button("Enregistrer dans la base de données"):
                insert_data_to_db(data)
        except Exception as e:
            st.error(f"Erreur lors du chargement du fichier : {e}")

    # Même procédure pour les autres types de données (commissions, ACE SFI, acteurs)
    for file_type, insert_function in [
        ("commissions et collectes", insert_data_commission_collecte),
        ("ACE & SFI", insert_data_ace_sfi),
        ("acteurs", insert_data_acteur),
    ]:
        st.sidebar.markdown("---")
        uploaded_file = st.file_uploader(f"Téléchargez les données des {file_type}", type=["xlsx", "xls"])
        if uploaded_file is not None:
            try:
                data = pd.read_excel(uploaded_file)
                with st.expander(f"🔍 Voir les données importées"):
                    st.dataframe(data, height=300)
                if st.button(f"Enregistrer dans la base de données"):
                    insert_function(data)
            except Exception as e:
                st.error(f"Erreur lors du chargement du fichier : {e}")

if selected == "Intervention":
    get_intervention()
elif selected == "Collectes & Commissions":
    afficher_filtre_collecte_commission()
elif selected == "Suivi des ACE & SFI":
    get_suivi_ace_sfi()