import streamlit as st
from estimation import estimer_depuis_adresse  # importe la fonction qui contient déjà les modèles
from streamlit_folium import st_folium
import re
import requests
import json
from datetime import datetime

# Configuration Mage API
MAGE_API_URL = "http://localhost:6789/api/v1"

# Fonction pour communiquer avec Mage
def call_mage_api(endpoint, method="GET", data=None):
    """Fonction utilitaire pour appeler l'API Mage"""
    try:
        url = f"{MAGE_API_URL}/{endpoint}"
        if method == "GET":
            response = requests.get(url, timeout=10)
        elif method == "POST":
            response = requests.post(url, json=data, timeout=30)
        
        if response.status_code == 200:
            return {"success": True, "data": response.json()}
        else:
            return {"success": False, "error": f"Erreur API: {response.status_code}"}
    except requests.exceptions.RequestException as e:
        return {"success": False, "error": f"Erreur de connexion: {str(e)}"}

def trigger_mage_pipeline(pipeline_name, variables=None):
    """Déclenche un pipeline Mage avec des variables"""
    data = {
        "pipeline_run": {
            "variables": variables or {}
        }
    }
    return call_mage_api(f"pipelines/{pipeline_name}/pipeline_runs", "POST", data)

def get_mage_pipeline_status(pipeline_name):
    """Récupère le statut des dernières exécutions d'un pipeline"""
    return call_mage_api(f"pipelines/{pipeline_name}/pipeline_runs")

# Initialisation de la session pour stocker l'historique
if "historique_estimations" not in st.session_state:
    st.session_state.historique_estimations = []

if "mage_status" not in st.session_state:
    st.session_state.mage_status = None

st.set_page_config(page_title="Estimation immobilière", page_icon="🏡")
departements = [
    "01 - Ain",
    "26 - Drôme",
    "31 - Haute-Garonne",
    "33 - Gironde",
    "35 - Ille-et-Vilaine",
    "38 - Isère",
    "44 - Loire-Atlantique",
    "45 - Loiret",
    "63 - Puy-de-Dôme",
    "69 - Rhône"
]

# Sidebar avec informations + statut Mage
with st.sidebar:
    st.markdown("### 📊 Informations")
    st.markdown("""
    - **Modèle** : IA hybride  
    - **Sources** : Données DVF (data.gouv) & Observatoire des territoires  
    - **Mise à jour** : Semestrielle 
    - **Précision** : ±15%  
    """)

    st.markdown("### 🛠️ Fonctionnalités")
    st.markdown("""
    - Estimation par adresse  
    - Analyse géographique  
    - Comparaison de prix  
    - Tendances du marché  
    """)
    
    # Section Mage AI
    st.markdown("### 🚀 Mage AI")
    if st.button("🔄 Vérifier statut Mage"):
        with st.spinner("Vérification..."):
            status = call_mage_api("pipelines")
            if status["success"]:
                st.success("🟢 Mage AI connecté")
                st.session_state.mage_status = "connected"
            else:
                st.error("🔴 Mage AI déconnecté")
                st.session_state.mage_status = "disconnected"
    
    if st.session_state.mage_status:
        if st.session_state.mage_status == "connected":
            st.success("🟢 Mage AI opérationnel")
        else:
            st.error("🔴 Mage AI non disponible")

st.title("🏘️ Où acheter et à quel prix ?")

# Création des onglets (ajout onglet Mage)
onglet_carte, onglet_estimation, onglet_mage = st.tabs([
    "🗺️ Analyse des départements", 
    "📊 Estimation d'une adresse",
    "🚀 Pipelines Mage"
])

with onglet_estimation:
    st.markdown("Entrez les infos de votre bien immobilier pour obtenir une estimation par modèle hybride :")

    departement_selectionne = st.selectbox("🗺️​ Départements disponibles", departements)
    code_departement = departement_selectionne.split(" - ")[0]

    adresse = st.text_input("📍 Adresse complète (adresse, code postal et ville)", placeholder="Ex : 15 rue Félix Thomas, 44000 Nantes")
    match = re.search(r'\b\d{5}\b', adresse)
    code_postal = match.group() if match else None
    
    col1, col2 = st.columns(2)
    with col1:
        type_local = st.selectbox("🏠 Type de bien", ["Appartement", "Maison"])
    with col2:
        nb_pieces = st.number_input("🔢 Nombre de pièces", 1, 12, 3)

    surface = st.number_input("📐 Surface habitable (m²)", 10, 500, 60)

    # Options d'estimation
    col_est1, col_est2 = st.columns(2)
    
    with col_est1:
        if st.button("🔮 Estimation classique"):
            if not adresse:
                st.warning("Merci de renseigner à la fois l'adresse complète.")
            elif not code_postal.startswith(code_departement):
                st.error(f"Le code postal doit commencer par {code_departement} (département sélectionné).")
            else:
                with st.spinner("Estimation en cours..."):
                    resultat = estimer_depuis_adresse(
                        adresse_str=adresse,
                        type_local=type_local,
                        surface=surface,
                        nb_pieces=nb_pieces,
                        code_postal=code_postal
                    )

                if "erreur" in resultat:
                    st.error(resultat["erreur"])
                else:
                    st.success("✅ Estimation réussie !")
                    st.markdown(f"**📏 Prix/m² estimé** : `{format(resultat['prix_m2_estime'], ',.2f').replace(',', ' ').replace('.', ',')} €`")
                    st.markdown(f"**💶 Valeur foncière estimée** : `{resultat['valeur_fonciere_estimee']:,}`".replace(",", " ") + " €")
                    st.markdown(f"**📎 Fourchette de confiance** : `{resultat['fourchette'][0]:,}`".replace(",", " ") + " € – " + f"`{resultat['fourchette'][1]:,}`".replace(",", " ") + " €")
                    st.markdown(f"**🗺️ Zone typologique** : `{resultat['zone'].capitalize()}`".replace("_"," "))
                    st.markdown(f"**💬 Commentaire** : {resultat['commentaire']}")

                    # Enregistrement dans l'historique
                    st.session_state.historique_estimations.append({
                        "Adresse": adresse,
                        "Code postal": code_postal,
                        "Type": type_local,
                        "Surface": surface,
                        "Pièces": nb_pieces,
                        "Prix/m² estimé (€)": round(resultat["prix_m2_estime"], 2),
                        "Valeur foncière (€)": resultat["valeur_fonciere_estimee"],
                        "Zone": resultat["zone"].capitalize().replace("_", " "),
                        "Méthode": "Classique",
                        "Timestamp": datetime.now().strftime("%Y-%m-%d %H:%M")
                    })

    with col_est2:
        if st.button("🚀 Estimation via Mage"):
            if not adresse:
                st.warning("Merci de renseigner l'adresse complète.")
            elif not code_postal.startswith(code_departement):
                st.error(f"Le code postal doit commencer par {code_departement}.")
            else:
                with st.spinner("Lancement du pipeline Mage..."):
                    # Variables à passer au pipeline Mage
                    variables = {
                        "adresse": adresse,
                        "code_postal": code_postal,
                        "type_local": type_local,
                        "surface": surface,
                        "nb_pieces": nb_pieces,
                        "departement": code_departement
                    }
                    
                    # Déclencher le pipeline (remplacez 'estimation_pipeline' par le nom de votre pipeline)
                    result = trigger_mage_pipeline("estimation_pipeline", variables)
                    
                    if result["success"]:
                        st.success("🚀 Pipeline Mage lancé avec succès !")
                        st.info("Consultez l'onglet 'Pipelines Mage' pour suivre l'exécution.")
                        
                        # Enregistrement dans l'historique
                        st.session_state.historique_estimations.append({
                            "Adresse": adresse,
                            "Code postal": code_postal,
                            "Type": type_local,
                            "Surface": surface,
                            "Pièces": nb_pieces,
                            "Prix/m² estimé (€)": "En cours...",
                            "Valeur foncière (€)": "En cours...",
                            "Zone": "En cours...",
                            "Méthode": "Mage AI",
                            "Timestamp": datetime.now().strftime("%Y-%m-%d %H:%M")
                        })
                    else:
                        st.error(f"❌ Erreur lors du lancement: {result['error']}")

    # Affichage de l'historique
    if st.session_state.historique_estimations:
        st.markdown("### 📜 Historique des estimations réalisées")
        st.dataframe(st.session_state.historique_estimations, use_container_width=True)

with onglet_mage:
    st.markdown("### 🚀 Gestion des pipelines Mage AI")
    
    # Statut des pipelines
    col_m1, col_m2 = st.columns(2)
    
    with col_m1:
        if st.button("📋 Lister les pipelines"):
            with st.spinner("Récupération des pipelines..."):
                result = call_mage_api("pipelines")
                if result["success"]:
                    pipelines = result["data"]
                    st.success(f"✅ {len(pipelines)} pipeline(s) trouvé(s)")
                    for pipeline in pipelines:
                        st.write(f"- **{pipeline.get('uuid', 'N/A')}** - {pipeline.get('name', 'Sans nom')}")
                else:
                    st.error(f"❌ {result['error']}")
    
    with col_m2:
        pipeline_name = st.text_input("📝 Nom du pipeline", placeholder="estimation_pipeline")
        if st.button("🔍 Statut du pipeline"):
            if pipeline_name:
                with st.spinner("Vérification..."):
                    result = get_mage_pipeline_status(pipeline_name)
                    if result["success"]:
                        runs = result["data"]
                        st.success(f"✅ Pipeline '{pipeline_name}' trouvé")
                        if runs:
                            latest_run = runs[0]
                            st.write(f"**Dernière exécution**: {latest_run.get('status', 'N/A')}")
                            st.write(f"**ID**: {latest_run.get('id', 'N/A')}")
                        else:
                            st.info("Aucune exécution trouvée")
                    else:
                        st.error(f"❌ {result['error']}")
            else:
                st.warning("Veuillez saisir un nom de pipeline")
    
    # Section de test manuel
    st.markdown("### 🧪 Test manuel de pipeline")
    with st.expander("Paramètres avancés"):
        test_pipeline = st.text_input("Pipeline à tester", value="estimation_pipeline")
        test_variables = st.text_area(
            "Variables JSON", 
            value='{"test": true, "adresse": "Test address"}',
            help="Format JSON pour les variables du pipeline"
        )
        
        if st.button("🚀 Lancer le test"):
            try:
                variables = json.loads(test_variables)
                with st.spinner("Lancement du test..."):
                    result = trigger_mage_pipeline(test_pipeline, variables)
                    if result["success"]:
                        st.success("✅ Test lancé avec succès !")
                        st.json(result["data"])
                    else:
                        st.error(f"❌ {result['error']}")
            except json.JSONDecodeError:
                st.error("❌ Format JSON invalide")

with onglet_carte:
    st.markdown("### 🗺️ Cartes d'attractivité par type de bien")

    with st.expander("🌍 Afficher la carte d'attractivité globale", expanded=True):
        with open("carte_attract_globale.html", "r", encoding="utf-8") as f:
            st.components.v1.html(f.read(), height=650, scrolling=False)

    with st.expander("🏢 Afficher la carte pour les appartements", expanded=True):
        with open("carte_attract_app.html", "r", encoding="utf-8") as f:
            st.components.v1.html(f.read(), height=650, scrolling=False)

    with st.expander("🏡 Afficher la carte pour les maisons", expanded=True):
        with open("carte_attract_maison.html", "r", encoding="utf-8") as f:
            st.components.v1.html(f.read(), height=650, scrolling=False)

    # Explication du score en bas
    st.markdown("### ℹ️ Méthodologie du rang d'attractivité")
    st.write("""
    Le **rang d'attractivité** est un indicateur calculé à partir de plusieurs critères socio-économiques et immobiliers à l'échelle départementale :

    - L'évolution de la population d'ici 2070
    - Les revenus médians
    - Et le prix moyen au m² des logements

    Les critères ne sont pas pondérés, le score est donc une moyenne simple de ces trois indicateurs.
    Ces cartes permettent ainsi d'identifier les zones les plus dynamiques ou à potentiel en France.
    """)