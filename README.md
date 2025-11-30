# 🏘️ Wild Data Hub - Estimation Immobilière

> Application web d'estimation immobilière basée sur l'IA et l'analyse de données DVF (Demandes de Valeurs Foncières)

[![Python](https://img.shields.io/badge/Python-3.10+-blue.svg)](https://www.python.org/)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.45+-red.svg)](https://streamlit.io/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

## 📋 Description

Wild Data Hub est une application web interactive permettant d'estimer la valeur immobilière d'un bien en France. Le projet combine :

- **Machine Learning** : Modèles XGBoost entraînés sur les données DVF
- **Géocodage** : Intégration avec Nominatim pour la localisation
- **Visualisation** : Cartes interactives d'attractivité par département
- **Analyse de données** : Fusion de données INSEE, DVF et statistiques locales

## ✨ Fonctionnalités

### 🎯 Estimation de prix
- Estimation par adresse complète
- Support pour **Appartements** et **Maisons**
- Prise en compte de la surface, nombre de pièces, et localisation
- Fourchette de confiance (±15%)
- Classification par zone typologique (rurale, intermédiaire, urbaine)

### 🗺️ Cartes d'attractivité
- Carte globale d'attractivité des départements
- Cartes spécifiques par type de bien (appartements/maisons)
- Analyse basée sur :
  - Évolution démographique projetée (2070)
  - Revenus médians
  - Prix moyen au m²

### 🚀 Intégration Mage AI
- Pipelines de traitement de données
- API pour déclencher des estimations via Mage
- Suivi des exécutions de pipelines

## 🛠️ Technologies

- **Backend** : Python 3.10+
- **Framework Web** : Streamlit
- **Machine Learning** : 
  - XGBoost
  - scikit-learn
  - category-encoders
- **Géospatial** : 
  - GeoPy (géocodage)
  - Folium (cartes)
  - GeoPandas
- **Data Processing** : Pandas, NumPy
- **Orchestration** : Mage AI (optionnel)

## 📦 Installation

### Prérequis
- Python 3.10 ou supérieur
- pip

### Étapes

1. **Cloner le dépôt**
```bash
git clone https://github.com/Amir239278/wild-data-hub.git
cd wild-data-hub
```

2. **Installer les dépendances**
```bash
pip install -r requirements.txt
```

3. **Préparer les données**
   - Les modèles pré-entraînés doivent être disponibles dans `dataset/`
   - Si nécessaire, régénérer les modèles :
   ```bash
   python scripts/regenerate_models.py
   ```

4. **Lancer l'application**
```bash
streamlit run app.py
```

L'application sera accessible sur `http://localhost:8501`

## 📁 Structure du projet

```
wild-data-hub/
├── app.py                 # Application Streamlit principale
├── estimation.py          # Module d'estimation immobilière
├── collecte_dvf.py        # Script de collecte des données DVF
├── scripts/
│   └── regenerate_models.py  # Régénération des modèles ML
├── dataset/              # Données et modèles (non versionné)
├── project/              # Configuration Mage AI
├── requirements.txt      # Dépendances Python
└── README.md            # Ce fichier
```

## 🎓 Utilisation

### Estimation classique

1. Sélectionnez un département
2. Entrez l'adresse complète (adresse, code postal, ville)
3. Spécifiez le type de bien (Appartement/Maison)
4. Indiquez la surface et le nombre de pièces
5. Cliquez sur "🔮 Estimation classique"

### Estimation via Mage AI

1. Remplissez les mêmes informations
2. Cliquez sur "🚀 Estimation via Mage"
3. Consultez l'onglet "Pipelines Mage" pour suivre l'exécution

## 📊 Données utilisées

- **DVF** : Données de transactions immobilières (data.gouv.fr)
- **INSEE** : Données socio-économiques et démographiques
- **Observatoire des territoires** : Statistiques locales

## 🔧 Configuration

### Variables d'environnement (optionnel)

Pour utiliser Mage AI, configurez :
```bash
MAGE_API_URL=http://localhost:6789/api/v1
```

## 🐳 Docker

### Option 1 : Docker Compose (recommandé)

Le moyen le plus simple de lancer l'application avec Docker :

```bash
docker-compose up -d
```

L'application sera accessible sur `http://localhost:8501`

Pour arrêter :
```bash
docker-compose down
```

### Option 2 : Docker classique

```bash
# Construire l'image
docker build -t wild-data-hub .

# Lancer le conteneur
docker run -p 8501:8501 wild-data-hub
```

### Note importante sur les modèles

⚠️ **Pour la production**, vous devez copier vos vrais modèles ML dans le conteneur :

```bash
# Option 1 : Via volume Docker
docker run -p 8501:8501 -v ./dataset:/app/dataset wild-data-hub

# Option 2 : Via docker-compose (décommentez la ligne volume dans docker-compose.yml)
```

Par défaut, le Dockerfile crée des modèles factices pour permettre le démarrage de l'application.

## 📝 Notes

- Les modèles sont entraînés sur les données de 2024
- La précision estimée est de ±15%
- Les données sont mises à jour semestriellement
- Les départements supportés sont limités (voir liste dans l'application)

## 🤝 Contribution

Les contributions sont les bienvenues ! N'hésitez pas à :
- Ouvrir une issue pour signaler un bug
- Proposer une amélioration via une pull request
- Partager vos retours d'expérience

## 📄 Licence

Ce projet est sous licence MIT. Voir le fichier [LICENSE](LICENSE) pour plus de détails.

## 👤 Auteur

**Amir** - [@Amir239278](https://github.com/Amir239278)

## 🙏 Remerciements

- Data.gouv.fr pour les données DVF
- INSEE pour les données statistiques
- La communauté open source Python

---

⭐ Si ce projet vous a été utile, n'hésitez pas à lui donner une étoile !
