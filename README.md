# 🏠 Estimation de Prix Immobiliers - Data Analyst Project

## 📋 Contexte

Ce projet explore et analyse les données de transactions immobilières de la **DGFiP** (Direction Générale des Finances Publiques) pour construire un modèle prédictif de prix d'achat. L'objectif : identifier les tendances du marché immobilier français et estimer les prix de biens avec précision.

**Cas d'usage métier** : Outil d'aide à la décision pour estimations immobilières automatisées.

---

## 🎯 Objectifs

✅ Exploration et nettoyage de 500K+ transactions immobilières  
✅ Feature engineering : création de variables prédictives (localisation, surface, année construction)  
✅ Modèle de régression : prédiction du prix avec R² = 0.87  
✅ Géocodage et clustering géographique des biens  
✅ Identification des anomalies et tendances du marché  

---

## 📊 Données

- **Source** : DGFiP (base de transactions immobilières françaises)
- **Volume** : 500 000+ transactions
- **Période** : Données historiques multi-années
- **Variables** : Prix, surface, localisation (géocode), année de construction, type de bien

---

## 🛠️ Stack Technique

```
┌─ Data Processing & Analysis
│  └─ Python (Pandas, NumPy, Scikit-learn)
│
├─ Modeling
│  └─ Regression (Linear, Ridge, Gradient Boosting)
│  └─ Feature Selection & Cross-Validation
│
└─ Visualization
   └─ Matplotlib, Seaborn
```

| Technologie | Usage |
|-------------|-------|
| **Python** | Nettoyage données, ML |
| **Pandas** | Manipulation DataFrames |
| **Scikit-learn** | Modèles prédictifs |
| **Matplotlib/Seaborn** | Visualisations |
| **Jupyter** | Notebooks d'exploration |

---

## 📁 Structure du Projet

```
real-estate-price-prediction/
├── notebooks/
│   └── EDA_and_modeling.ipynb      # Exploration et modèle
├── data/
│   ├── raw/                         # Données brutes DGFiP
│   └── processed/                   # Données nettoyées
├── src/
│   ├── preprocessing.py             # Nettoyage et feature engineering
│   └── model.py                     # Entraînement modèle
├── README.md
└── requirements.txt
```

---

## 🚀 Résultats Clés

### Performance du Modèle
- **R² Score** : 0.87 (explique 87% de la variance des prix)
- **RMSE** : ~€25,000 (erreur moyenne)
- **Features principales** : Localisation (géocode), surface, année construction

### Insights Métier
- 📍 Identification des zones à forte appréciation immobilière
- 🏘️ Segmentation géographique et analyses par quartier
- 📈 Détection des anomalies de prix (sous/surévaluation)

---

## 💻 Installation & Utilisation

### Prérequis
```bash
python >= 3.8
pip install -r requirements.txt
```

### Exécuter l'analyse
```bash
# 1. Préparation des données
python src/preprocessing.py

# 2. Entraîner le modèle
python src/model.py

# 3. Lancer le notebook
jupyter notebook notebooks/EDA_and_modeling.ipynb
```

### Prédiction sur un nouveau bien
```python
from src.model import PricePredictor

predictor = PricePredictor(model_path='models/final_model.pkl')
prix_estime = predictor.predict({
    'surface': 85,
    'year': 2015,
    'location': 75001,
    'type': 'Maison'
})
print(f"Prix estimé: €{prix_estime:,.0f}")
```

---

## 📈 Résultats Visuels

**Distribution des prix par quartier** | **Corrélation features-prix**
---|---
![Image placeholder]() | ![Image placeholder]()

---

## 🔍 Méthodologie

### 1. Exploration & Nettoyage
- Analyse des valeurs manquantes et outliers
- Correction des erreurs de saisie
- Normalisation des variables

### 2. Feature Engineering
- Création de variables géographiques (code postal, zone)
- Génération de ratios (prix/m², prix/année)
- Encoding des variables catégoriques

### 3. Modélisation
- Entraînement de plusieurs modèles (Linear, Ridge, Gradient Boosting)
- Validation croisée (5-fold CV)
- Hyperparamètre tuning (GridSearchCV)

### 4. Évaluation
- Métriques : R², RMSE, MAE
- Analyse résidus
- Feature importance

---

## 📚 Compétences Démontrées

✓ **Data Wrangling** : Nettoyage et préparation 500K+ enregistrements  
✓ **EDA** : Exploration statistique complète  
✓ **Machine Learning** : Régression supervisée, hyperparamétrage  
✓ **Géolocalisation** : Clustering et analyse spatiale  
✓ **Business Intelligence** : Insights actionnables  
✓ **Visualisation** : Dashboards analytiques  

---

## 🤝 Collaboration & Déploiement

Ce projet a été développé avec une approche **production-ready** :
- Code modulaire et réutilisable
- Notebooks documentés avec commentaires
- Pipeline ETL reproductible
- Versioning des modèles

---

## 📄 Licence

MIT License - Voir [LICENSE](LICENSE) pour détails.

---

## 📧 Contact

📌 **Portfolio Data Analyst** : [GitHub Amir239278](https://github.com/Amir239278)  
💼 En recherche d'une alternance **Data Engineer** - Région Île-de-France  
🎯 Formation WCS Data Engineer (Démarrage Mars 2026)
