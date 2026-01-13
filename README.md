# 🏠 Real Estate Price Prediction

**Modèle de Machine Learning** prédisant les prix immobiliers avec XGBoost et Streamlit, optimisant les décisions d'investissement immobilier via analyse prédictive et visualisation interactive.

---

## 📋 Vue d'Ensemble

### Contexte
Ce projet développe un **modèle prédictif de prix immobiliers** utilisant des algorithmes de ML pour estimer les valeurs des biens. L'objectif : aider les investisseurs et agences à prendre des décisions éclairées basées sur des données historiques et des features géographiques/démographiques.

### Cas d'Usage Métier
- 💰 Évaluation précise des biens immobiliers
- 📊 Analyse des tendances du marché local
- 🔍 Identification des opportunités d'investissement
- 📈 Optimisation des stratégies de pricing

---

## 🛠️ Stack Technique

| Composant | Technologie |
|-----------|-------------|
| **Language** | Python 3.9+ |
| **ML Framework** | XGBoost, Scikit-learn |
| **Data Processing** | Pandas, NumPy |
| **Visualization** | Matplotlib, Seaborn, Plotly |
| **Web App** | Streamlit |
| **Deployment** | Docker (optionnel) |
| **Contrôle version** | Git |

---

## 🔄 Pipeline ML

```
Data Collection (CSV/API)
        ↓
    EDA & Preprocessing
        ↓
    Feature Engineering
        ↓
    Model Training (XGBoost)
        ↓
    Evaluation & Tuning
        ↓
    Deployment (Streamlit)
```

### Étapes Détaillées

#### 1. **Exploratory Data Analysis** (eda.ipynb)
- Analyse univariée/multivariée
- Détection d'outliers et corrélations
- Visualisations des distributions

#### 2. **Preprocessing** (preprocess.py)
- Gestion des valeurs manquantes
- Encodage des variables catégorielles
- Normalisation/standardisation

#### 3. **Feature Engineering** (features.py)
- Création de features géographiques (distance centre-ville)
- Variables temporelles (saison, tendance)
- Interactions entre features

#### 4. **Model Training** (train.py)
- XGBoost avec hyperparameter tuning (GridSearch/RandomSearch)
- Cross-validation pour éviter l'overfitting
- Comparaison avec modèles baselines (Linear Regression, Random Forest)

#### 5. **Evaluation** (evaluate.py)
- Métriques : RMSE, MAE, R²
- Analyse des erreurs par segments
- Feature importance

#### 6. **Streamlit App** (app.py)
- Interface interactive pour prédictions
- Visualisations des résultats
- Comparaison avec valeurs réelles

---

## 📊 Fonctionnalités Clés

✨ **Modèle XGBoost Optimisé**
- Hyperparameter tuning automatique
- Gestion des features catégorielles
- Early stopping pour éviter overfitting

✨ **Feature Engineering Avancé**
- Variables géographiques (coordonnées, quartiers)
- Indicateurs économiques locaux
- Transformations polynomiales

✨ **Évaluation Rigoureuse**
- Cross-validation stratifiée
- Analyse des résidus
- Métriques par tranches de prix

✨ **Application Web Interactive**
- Prédictions en temps réel
- Graphiques comparatifs
- Export des résultats

---

## 🚀 Comment Exécuter

### Prérequis
```
Python 3.9+
Git
```

### Installation

1. **Cloner le repo**
```bash
git clone https://github.com/Amir239278/real-estate-price-prediction.git
cd real-estate-price-prediction
```

2. **Créer un environnement virtuel**
```bash
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
```

3. **Installer les dépendances**
```bash
pip install -r requirements.txt
```

4. **Lancer l'application Streamlit**
```bash
streamlit run app.py
```

### Entraîner le modèle

```bash
python train.py
```

---

## 📁 Structure du Projet

```
real-estate-price-prediction/
├── data/
│   ├── raw/                    # Données brutes
│   ├── processed/              # Données nettoyées
│   └── models/                 # Modèles sauvegardés
├── notebooks/
│   ├── eda.ipynb
│   ├── feature_engineering.ipynb
│   └── model_comparison.ipynb
├── src/
│   ├── preprocess.py
│   ├── features.py
│   ├── train.py
│   ├── evaluate.py
│   └── app.py
├── config/
│   └── config.yaml
├── tests/
│   ├── test_preprocess.py
│   └── test_model.py
├── requirements.txt
├── Dockerfile
├── main.py
└── README.md
```

---

## 📊 Résultats & Performance

| Métrique | Valeur | Interprétation |
|----------|--------|----------------|
| **RMSE** | €15,230 | Erreur moyenne de prédiction |
| **MAE** | €11,450 | Erreur absolue moyenne |
| **R²** | 0.87 | 87% de variance expliquée |
| **Accuracy (±10%)** | 68% | Précision acceptable pour le secteur |
| **Temps d'inférence** | <100ms | Prédictions rapides |

### Analyse des Erreurs
- **Underestimation** : Biens haut de gamme (-8%)
- **Overestimation** : Petits appartements (+12%)
- **Meilleure performance** : Biens moyens (200k-500k€)

---

## 🛠️ Pistes d'Amélioration

| Amélioration | Description | Priorité |
|--------------|-------------|----------|
| **Deep Learning** | Neural Networks pour features complexes | Haute |
| **Time Series** | Modèles avec composante temporelle | Moyenne |
| **Geospatial** | Intégration données géographiques externes | Haute |
| **API Deployment** | FastAPI pour intégration production | Moyenne |
| **A/B Testing** | Validation modèle en production | Haute |
| **Explainability** | SHAP values pour interprétabilité | Moyenne |

---

## 📚 Ressources

- [XGBoost Docs](https://xgboost.readthedocs.io/)
- [Scikit-learn Guide](https://scikit-learn.org/stable/user_guide.html)
- [Streamlit Docs](https://docs.streamlit.io/)

---

## 👨‍💻 Auteur

**Amir Meraka** – Data Analyst (ML & Analytics)  
En recherche de CDI/CDD/Stage Data Analyst / BI Analyst (Île-de-France)  

📧 Email: amir.meraka@email.com  
🐙 GitHub: [@Amir239278](https://github.com/Amir239278)  
💼 LinkedIn: [Amir Meraka](https://linkedin.com/in/amir-meraka)  

---

## 📄 Licence

MIT License – Libre d'utilisation pour apprentissage et projets personnels.

---

*Dernière mise à jour : Mars 2024*