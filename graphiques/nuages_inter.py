import streamlit as st
import matplotlib.pyplot as plt
import plotly.express as px
import numpy as np

# Exemple de données


# Fonction pour afficher le graphique
def nuages_inter(x, y):
    plt.figure(figsize=(10,5))
    plt.plot(x, y, marker='o', color='red', linestyle='-', label="Interventions")
    
    # Ajouter des labels
    plt.xticks(rotation=45)
    plt.ylabel("Nombre d'Intervention")
    plt.xlabel("Période")
    plt.title("Évolution des Interventions")
    plt.legend()
    
    # Annotation pour le premier point
    plt.annotate(f"{y[0]:,}".replace(",", " "), (x[0], y[0]), textcoords="offset points", xytext=(0,10), ha='center', fontsize=10, fontweight='bold')
    
    plt.grid(True)
    
    # Affichage avec Streamlit
    st.pyplot(plt)

def nua_inter(df):
     # Création du graphique interactif
     fig = px.line(df, x="Date", y="Nb_interventions", markers=True, text=df["Nb_interventions"],
               title="Évolution des Interventions", labels={"Interventions": "Date"})
     fig.update_traces(marker=dict(color="red", size=8), line=dict(color="red"))

     # Format du tooltip
     fig.update_traces(hovertemplate="<b>%{x}</b><br>Commissions : <b>%{y:,.0f}</b>")

     fig.show()
          
