FROM python:3.10-slim

# Variables d'environnement pour optimiser Python et encoding
ENV PYTHONIOENCODING=utf-8 \
    PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1

# Dossiers et dépendances système
WORKDIR /app
RUN mkdir -p /app/dataset /app/logs \
 && apt-get update \
 && apt-get install -y --no-install-recommends \
      cron \
      gcc \
      g++ \
      python3-dev \
      build-essential \
      curl \
      procps \
      libgdal-dev \
      libproj-dev \
      libgeos-dev \
      gdal-bin \
 && rm -rf /var/lib/apt/lists/* \
 && apt-get clean

# Copie et installation des dépendances Python
COPY docker.requirements.txt .
RUN pip install --no-cache-dir --timeout=120 --upgrade pip \
 && pip install --no-cache-dir --timeout=120 -r docker.requirements.txt

# Copier le code source
COPY . .

# Créer les dossiers nécessaires pour les modèles
RUN mkdir -p /app/dataset

# Régénérer les modèles (si les vrais modèles ne sont pas disponibles)
# Note: Pour la production, copiez vos vrais modèles dans dataset/ avant le build
RUN python scripts/regenerate_models.py || echo "⚠️ Modèles factices créés - Remplacez par les vrais modèles pour la production"

# Ports exposés
EXPOSE 8501

# Commande par défaut - Lance Streamlit uniquement
# Pour utiliser Mage AI, décommentez la ligne suivante et commentez celle-ci
CMD ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]

# Alternative avec Mage AI (décommentez si nécessaire):
# CMD bash -c "mage start project & streamlit run app.py --server.port=8501 --server.address=0.0.0.0"