import streamlit as st
# import mariadb
# import pandas as pd

# # Fonction pour récupérer les données d'une colonne spécifique
# def get_column_values(column_name, table_name):
#     try:
#         # Connexion à la base de données
#         conn = mariadb.connect(
#             host="localhost",
#             user="root",
#             password="",
#             database="Statistic_projet",
#             port=3307
#         )
#         cursor = conn.cursor()

#         # Exécuter la requête pour récupérer une colonne spécifique
#         query = f"SELECT DISTINCT {column_name} FROM {table_name}"
#         cursor.execute(query)
#         results = cursor.fetchall()  # Récupérer toutes les valeurs

#         # Fermer la connexion
#         cursor.close()
#         conn.close()

#         # Transformer les résultats en une liste
#         return [row[0] for row in results]
    
#     except mariadb.Error as e:
#         st.error(f"Erreur de base de données : {e}")
#         return []

# # Interface Streamlit
# st.title("📋 Sélectionner une Institution")

# # Récupérer les valeurs de la colonne "institution"
# institutions = get_column_values("institution", "interventions")

# # Vérifier si des données sont récupérées
# if institutions:
#     selected_institution = st.selectbox("🏦 Choisissez une institution :", institutions)
#     st.success(f"Vous avez sélectionné : {selected_institution}")
# else:
#     st.warning("Aucune institution trouvée dans la base de données.")



# import streamlit as st
# import pandas as pd
# import numpy as np
# import matplotlib.pyplot as plt


# data = np.random.normal(size=10000)
# data = pd.DataFrame(data, columns=["Disk_norm"])
# st.dataframe(data.head())
# # st.write(data)

# fig, ax = plt.subplots(figsize=(10, 5))
# ax.plot(data.Disk_norm, color='blue', linestyle='-', marker='o', label="Utilisation Disque Normalisée")
# ax.set_title("Évolution de l'utilisation du disque")
# ax.set_xlabel("Index")
# ax.set_ylabel("Disk_norm")
# ax.legend()
# # ax.grid(True)
# # ax.hist(data.Disk_norm)
# plt.show()


# st.pyplot(fig)



# import numpy as np

# images = np.empty( shape = (2048, 2048, 50) )
# for index, im in enumerate("images/logo.png"):
#     images[:,:,index] = im

# avg = np.average(images, axis = 2)