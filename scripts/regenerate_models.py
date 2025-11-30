import pandas as pd
import joblib
import os

# Créer le dossier dataset s'il n'existe pas
os.makedirs("dataset", exist_ok=True)

# Simuler de nouveaux modèles (remplacez par votre vrai code de création de modèles)
modele_dict = {"dummy": "model"}

# Créer des données de statistiques locales de test
stats_locales = pd.DataFrame({
    "code_postal": ["75001", "75002"],
    "prix_m2_median_code_postal": [9500, 8700]
})

# Sauvegarder les modèles et les statistiques
joblib.dump(modele_dict, "dataset/modele_dict.pkl")
stats_locales.to_pickle("dataset/stats_locales.pkl")

print("✅ Modèles et statistiques régénérés avec succès")
