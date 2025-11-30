import numpy as np

# estimation.py
import joblib
import pandas as pd
import time
import sys
import pickle
from geopy.geocoders import Nominatim
from geopy.exc import GeocoderTimedOut

# 🌍 Géocodeur
geolocator = Nominatim(user_agent="estimation-immo-app")

# 🔧 Fonction de chargement compatible avec les anciennes versions de pandas
def load_pickle_compatible(filepath):
    """Charge un fichier pickle en gérant les incompatibilités de version pandas"""
    try:
        return joblib.load(filepath)
    except (ModuleNotFoundError, AttributeError, ImportError) as e:
        error_str = str(e)
        if "pandas.core.indexes.numeric" in error_str or "pandas.core" in error_str:
            # Solution: créer des modules de compatibilité pour les anciennes références pandas
            import types
            
            # Créer un module factice pour pandas.core.indexes.numeric
            numeric_module = types.ModuleType('pandas.core.indexes.numeric')
            # Ajouter les classes nécessaires depuis pandas
            numeric_module.Int64Index = pd.Index
            numeric_module.Float64Index = pd.Index
            numeric_module.UInt64Index = pd.Index
            
            # Injecter le module dans sys.modules
            if 'pandas.core.indexes' not in sys.modules:
                sys.modules['pandas.core.indexes'] = types.ModuleType('pandas.core.indexes')
            if 'pandas.core.indexes.numeric' not in sys.modules:
                sys.modules['pandas.core.indexes.numeric'] = numeric_module
            
            # Essayer de charger à nouveau
            try:
                return joblib.load(filepath)
            except Exception:
                # Si ça ne fonctionne toujours pas, utiliser pickle directement
                with open(filepath, 'rb') as f:
                    return pickle.load(f)
        else:
            raise

# 📦 Chargement automatique avec gestion de compatibilité
try:
    modele_dict = load_pickle_compatible("dataset/modele_dict.pkl")
    stats_locales = pd.read_pickle("dataset/stats_locales.pkl")
except Exception as e:
    print(f"⚠️ Erreur lors du chargement des modèles: {e}")
    print("💡 Tentative de chargement avec méthode alternative...")
    # Méthode alternative: charger avec pickle directement
    import warnings
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        try:
            with open("dataset/modele_dict.pkl", 'rb') as f:
                modele_dict = pickle.load(f)
            stats_locales = pd.read_pickle("dataset/stats_locales.pkl")
        except Exception as e2:
            print(f"❌ Impossible de charger les modèles: {e2}")
            print("💡 Veuillez régénérer les modèles avec la commande: python scripts/regenerate_models.py")
            modele_dict = {}
            stats_locales = pd.DataFrame(columns=['code_postal', 'prix_m2_median_code_postal'])

def geocoder_adresse(adresse, tentative=1, max_tentative=3):
    try:
        location = geolocator.geocode(adresse, timeout=10)
        if location:
            return {'latitude': location.latitude, 'longitude': location.longitude}
    except GeocoderTimedOut:
        if tentative <= max_tentative:
            time.sleep(1)
            return geocoder_adresse(adresse, tentative + 1)
    return {'latitude': None, 'longitude': None}

def estimer_bien(bien, modele_dict, stats_locales, alpha=0.7):
    type_local = bien['type_local']
    code_postal = str(bien['code_postal'])
    dep = code_postal[:2]
    key = (type_local, dep)

    if key not in modele_dict:
        return {"erreur": f"❌ Modèle non disponible pour {type_local} - {dep}"}

    model = modele_dict[key]
    surface = bien['surface_reelle_bati']
    pieces = bien['nombre_pieces_principales']
    surface_par_piece = surface / pieces if pieces > 0 else 0

    prix_median_local = stats_locales.loc[
        stats_locales['code_postal'] == code_postal, 'prix_m2_median_code_postal'
    ]
    prix_m2_median = prix_median_local.values[0] if not prix_median_local.empty else None

    if prix_m2_median is not None:
        if prix_m2_median < 2000:
            zone = 'zone_rurale'
        elif prix_m2_median <= 3000:
            zone = 'zone_intermediaire'
        else:
            zone = 'zone_urbaine'
    else:
        zone = 'zone_intermediaire'

    X_input = pd.DataFrame([{
        'surface_reelle_bati': surface,
        'nombre_pieces_principales': pieces,
        'surface_par_piece': surface_par_piece,
        'code_postal': code_postal,
        'prix_m2_median_code_postal': prix_m2_median or 2500,
        'latitude': bien['latitude'],
        'longitude': bien['longitude'],
        'zone_typologique': zone
    }])

    prix_m2_ml = model.predict(X_input)[0]
    prix_m2_final = (
        alpha * prix_m2_ml + (1 - alpha) * prix_m2_median
        if prix_m2_median
        else prix_m2_ml
    )

    valeur_estimee = int(prix_m2_final * surface)
    prix_min = int(valeur_estimee * 0.85)
    prix_max = int(valeur_estimee * 1.15)

    if prix_m2_median:
        ratio = prix_m2_final / prix_m2_median
        if ratio < 0.9:
            commentaire = "🔽 Estimation sous le marché local"
        elif ratio > 1.1:
            commentaire = "🔼 Estimation au-dessus du marché local"
        else:
            commentaire = "✅ Estimation cohérente avec les prix locaux"
    else:
        commentaire = "ℹ️ Pas de référence de prix local disponible"

    return {
        'prix_m2_estime': round(prix_m2_final, 2),
        'valeur_fonciere_estimee': valeur_estimee,
        'fourchette': (prix_min, prix_max),
        'zone': zone,
        'commentaire': commentaire
    }

def estimer_depuis_adresse(adresse_str, type_local, surface, nb_pieces, code_postal,
                           modele_dict=modele_dict, stats_locales=stats_locales, alpha=0.7):
    coords = geocoder_adresse(adresse_str)

    if coords['latitude'] is None or coords['longitude'] is None:
        return {"erreur": f"❌ Adresse introuvable via Nominatim : {adresse_str}"}

    bien = {
        'type_local': type_local,
        'code_postal': str(code_postal),
        'surface_reelle_bati': surface,
        'nombre_pieces_principales': nb_pieces,
        'latitude': coords['latitude'],
        'longitude': coords['longitude']
    }

    return estimer_bien(bien, modele_dict, stats_locales, alpha)
