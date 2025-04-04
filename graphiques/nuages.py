import streamlit as st
import matplotlib.pyplot as plt
import plotly.express as px
import numpy as np

# Exemple de données


# Fonction pour afficher le graphique
def nuages(x, y):
    plt.figure(figsize=(10,5))
    plt.plot(x, y, marker='o', color='red', linestyle='-', label="Commissions")
    
    # Ajouter des labels
    plt.xticks(rotation=45)
    plt.ylabel("Montant")
    plt.xlabel("Période")
    plt.title("Évolution des Commissions")
    plt.legend()
    
    # Annotation pour le premier point
    plt.annotate(f"{y[0]:,}".replace(",", " "), (x[0], y[0]), textcoords="offset points", xytext=(0,10), ha='center', fontsize=10, fontweight='bold')
    
    plt.grid(True)
    
    # Affichage avec Streamlit
    st.pyplot(plt)

def nua(df):
     # Création du graphique interactif
     fig = px.line(df, x="Date", y="Commissions", markers=True, text=df["Commissions"],
               title="Évolution des Commissions", labels={"Commissions": "Date"})
     fig.update_traces(marker=dict(color="red", size=8), line=dict(color="red"))

     # Format du tooltip
     fig.update_traces(hovertemplate="<b>%{x}</b><br>Commissions : <b>%{y:,.0f}</b>")

     fig.show()
          
