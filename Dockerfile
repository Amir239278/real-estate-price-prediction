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

# Régénérer les modèles
RUN python scripts/regenerate_models.py

# Ports exposés
EXPOSE 8501 6789

# Commande par défaut - Lance à la fois Streamlit et Mage
CMD bash -c "mage start project & streamlit run app.py --server.port=8501 --server.address=0.0.0.0"