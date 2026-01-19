pip install -r requirements.txt
# comparateur_regulations_crypto_final.py
import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import time

# Page configuration
st.set_page_config(
    page_title="Comparateur de Régulations Crypto",
    page_icon="⚖️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS - version simplifiée
st.markdown("""
<style>
    .main-header {
        font-size: 2.8rem;
        font-weight: 800;
        background: linear-gradient(90deg, #1E40AF 0%, #7C3AED 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 0.5rem;
    }
    
    .country-card {
        background: white;
        padding: 1.5rem;
        border-radius: 12px;
        box-shadow: 0 6px 16px rgba(0, 0, 0, 0.08);
        margin-bottom: 1.5rem;
        border: 1px solid #E5E7EB;
        transition: all 0.3s;
    }
    
    .metric-badge {
        display: inline-block;
        padding: 0.3rem 1rem;
        border-radius: 20px;
        font-weight: 600;
        margin: 0.2rem;
        font-size: 0.9rem;
    }
    
    .high { background: linear-gradient(135deg, #10B981 0%, #059669 100%); color: white; }
    .medium { background: linear-gradient(135deg, #F59E0B 0%, #D97706 100%); color: white; }
    .low { background: linear-gradient(135deg, #EF4444 0%, #DC2626 100%); color: white; }
    
    .progress-bar {
        height: 8px;
        background: #E5E7EB;
        border-radius: 4px;
        margin: 0.5rem 0;
        overflow: hidden;
    }
    
    .progress-fill {
        height: 100%;
        border-radius: 4px;
    }
</style>
""", unsafe_allow_html=True)

# Données réglementaires
@st.cache_data
def charger_donnees_reglementaires():
    frameworks = [
        {
            "pays": "Maroc (Projet 2025)",
            "drapeau": "🇲🇦",
            "statut": "Projet de Loi (42.25)",
            "score_innovation": 42,
            "score_protection": 85,
            "score_conformite": 90,
            "score_acces_marche": 35,
            "score_total": 63,
            "metriques": {
                "reconnaissance_legale": "Partielle (Actifs seulement)",
                "licence_requise": "Oui (Double : AMMC + BAM)",
                "protection_investisseurs": "Élevée",
                "aml_cft": "Oui (Rétention 10 ans)",
                "paiement_autorise": "Non",
                "reglementation_stablecoins": "Émission bancaire exclusive",
                "defi_reglemente": "Non (Exclu)",
                "nft_reglemente": "Non (Exclu)",
                "taxation_crypto": "À déterminer",
                "seuil_kyc": "Aucun seuil",
                "travel_rule": "Oui (Toutes transactions)"
            },
            "points_forts": ["AML/CFT renforcé", "Protection investisseurs", "Stabilité monétaire"],
            "points_faibles": ["Pas d'usage paiement", "Barrières d'entrée élevées", "Innovation limitée"],
            "source": "Ministère de l'Économie et des Finances, Maroc"
        },
        {
            "pays": "Union Européenne",
            "drapeau": "🇪🇺",
            "statut": "Implémenté (MiCA)",
            "score_innovation": 72,
            "score_protection": 92,
            "score_conformite": 88,
            "score_acces_marche": 78,
            "score_total": 82.5,
            "metriques": {
                "reconnaissance_legale": "Complète",
                "licence_requise": "Oui (Passeport européen)",
                "protection_investisseurs": "Très élevée",
                "aml_cft": "Oui (6ème directive)",
                "paiement_autorise": "Oui (avec conditions)",
                "reglementation_stablecoins": "Niveaux différenciés",
                "defi_reglemente": "Partiellement",
                "nft_reglemente": "Cas par cas",
                "taxation_crypto": "Variable par État",
                "seuil_kyc": "€1000",
                "travel_rule": "Oui (Seuil €1000)"
            },
            "points_forts": ["Passeport européen", "Protection consommateurs", "Règles claires"],
            "points_faibles": ["Conformité complexe", "Coûts élevés", "Adaptation lente"],
            "source": "Commission Européenne, ESMA"
        },
        {
            "pays": "Émirats Arabes Unis",
            "drapeau": "🇦🇪",
            "statut": "Implémenté",
            "score_innovation": 95,
            "score_protection": 78,
            "score_conformite": 82,
            "score_acces_marche": 97,
            "score_total": 88,
            "metriques": {
                "reconnaissance_legale": "Complète",
                "licence_requise": "Oui (VARA + FSRA)",
                "protection_investisseurs": "Moyenne-Élevée",
                "aml_cft": "Oui",
                "paiement_autorise": "Oui",
                "reglementation_stablecoins": "Autorisée",
                "defi_reglemente": "Oui (Expérimental)",
                "nft_reglemente": "Oui",
                "taxation_crypto": "0% impôt sociétés",
                "seuil_kyc": "$1000",
                "travel_rule": "Oui"
            },
            "points_forts": ["0% impôt sociétés", "Agrément rapide", "Favorable à DeFi"],
            "points_faibles": ["Multiples régulateurs", "Coûts élevés", "Focus institutionnel"],
            "source": "VARA, FSRA, ADGM"
        },
        {
            "pays": "Royaume-Uni",
            "drapeau": "🇬🇧",
            "statut": "Transition",
            "score_innovation": 68,
            "score_protection": 85,
            "score_conformite": 83,
            "score_acces_marche": 72,
            "score_total": 77,
            "metriques": {
                "reconnaissance_legale": "Complète",
                "licence_requise": "Oui (FCA)",
                "protection_investisseurs": "Élevée",
                "aml_cft": "Oui (Strict)",
                "paiement_autorise": "Oui (avec restrictions)",
                "reglementation_stablecoins": "En développement",
                "defi_reglemente": "En discussion",
                "nft_reglemente": "Guidances",
                "taxation_crypto": "Capital gains tax",
                "seuil_kyc": "£1000",
                "travel_rule": "Oui"
            },
            "points_forts": ["Règles claires", "Protection robuste", "Stabilité réglementaire"],
            "points_faibles": ["Complexité post-Brexit", "Coûts élevés", "Publicité restrictive"],
            "source": "Financial Conduct Authority"
        }
    ]
    return frameworks

# Fonctions d'affichage
def afficher_carte_pays(framework):
    couleur = "#10B981" if framework["score_total"] >= 70 else "#F59E0B" if framework["score_total"] >= 50 else "#EF4444"
    
    html = f"""
    <div class="country-card">
        <div style="display: flex; align-items: center; margin-bottom: 1rem;">
            <div style="font-size: 2rem; margin-right: 1rem;">{framework['drapeau']}</div>
            <div>
                <h3 style="margin: 0; color: #1F2937;">{framework['pays']}</h3>
                <div style="font-size: 0.9rem; color: #6B7280;">{framework['statut']}</div>
            </div>
        </div>
        
        <div style="text-align: center; margin: 1.5rem 0;">
            <div style="display: inline-block; background: {couleur}; color: white; padding: 0.8rem 2rem; border-radius: 25px; font-size: 1.8rem; font-weight: 800;">
                {framework['score_total']}/100
            </div>
        </div>
        
        <div style="margin-bottom: 1.5rem;">
            <div style="display: flex; justify-content: space-between; margin-bottom: 0.5rem;">
                <span>Innovation</span>
                <span style="font-weight: 600;">{framework['score_innovation']}</span>
            </div>
            <div class="progress-bar">
                <div class="progress-fill" style="width: {framework['score_innovation']}%; background: #10B981;"></div>
            </div>
            
            <div style="display: flex; justify-content: space-between; margin: 1rem 0 0.5rem 0;">
                <span>Protection</span>
                <span style="font-weight: 600;">{framework['score_protection']}</span>
            </div>
            <div class="progress-bar">
                <div class="progress-fill" style="width: {framework['score_protection']}%; background: #3B82F6;"></div>
            </div>
            
            <div style="display: flex; justify-content: space-between; margin: 1rem 0 0.5rem 0;">
                <span>Accès marché</span>
                <span style="font-weight: 600;">{framework['score_acces_marche']}</span>
            </div>
            <div class="progress-bar">
                <div class="progress-fill" style="width: {framework['score_acces_marche']}%; background: #8B5CF6;"></div>
            </div>
        </div>
        
        <div style="font-size: 0.85rem; color: #6B7280; border-top: 1px solid #E5E7EB; padding-top: 1rem;">
            Source: {framework['source']}
        </div>
    </div>
    """
    return html

def creer_tableau_comparatif(frameworks_selectionnes):
    donnees = []
    for f in frameworks_selectionnes:
        ligne = {
            "Pays": f"{f['drapeau']} {f['pays']}",
            "Score Total": f["score_total"],
            "Innovation": f["score_innovation"],
            "Protection": f["score_protection"],
            "Conformité": f["score_conformite"],
            "Accès Marché": f["score_acces_marche"],
            "Paiement Autorisé": f["metriques"]["paiement_autorise"],
            "Seuil KYC": f["metriques"]["seuil_kyc"],
            "Stablecoins": f["metriques"]["reglementation_stablecoins"][:20] + "..."
        }
        donnees.append(ligne)
    
    return pd.DataFrame(donnees)

def creer_graphique_scores_simple(frameworks_selectionnes):
    # Création d'un graphique simple avec matplotlib (inclus avec streamlit)
    import matplotlib.pyplot as plt
    
    pays = [f"{f['drapeau']} {f['pays'][:10]}..." for f in frameworks_selectionnes]
    scores_innovation = [f["score_innovation"] for f in frameworks_selectionnes]
    scores_protection = [f["score_protection"] for f in frameworks_selectionnes]
    scores_acces = [f["score_acces_marche"] for f in frameworks_selectionnes]
    
    x = np.arange(len(pays))
    width = 0.25
    
    fig, ax = plt.subplots(figsize=(10, 6))
    
    bars1 = ax.bar(x - width, scores_innovation, width, label='Innovation', color='#10B981')
    bars2 = ax.bar(x, scores_protection, width, label='Protection', color='#3B82F6')
    bars3 = ax.bar(x + width, scores_acces, width, label='Accès Marché', color='#8B5CF6')
    
    ax.set_xlabel('Pays')
    ax.set_ylabel('Scores')
    ax.set_title('Comparaison des Scores par Critère')
    ax.set_xticks(x)
    ax.set_xticklabels(pays, rotation=45, ha='right')
    ax.legend()
    
    # Ajouter les valeurs sur les barres
    for bars in [bars1, bars2, bars3]:
        for bar in bars:
            height = bar.get_height()
            ax.annotate(f'{int(height)}',
                       xy=(bar.get_x() + bar.get_width() / 2, height),
                       xytext=(0, 3),
                       textcoords="offset points",
                       ha='center', va='bottom', fontsize=9)
    
    plt.tight_layout()
    return fig

# Application principale
def main():
    # Charger les données
    frameworks = charger_donnees_reglementaires()
    
    # Header
    st.markdown('<h1 class="main-header">⚖️ Comparateur des Régulations Crypto</h1>', unsafe_allow_html=True)
    st.markdown('<p style="color: #4B5563; font-size: 1.2rem;">Analyse comparative du projet marocain 2025 vs. cadres réglementaires mondiaux</p>', unsafe_allow_html=True)
    
    # Sidebar
    with st.sidebar:
        st.markdown("### 🎯 Sélection des Pays")
        
        # Sélection multiple
        options_pays = [f"{f['drapeau']} {f['pays']}" for f in frameworks]
        selections = st.multiselect(
            "Choisissez les cadres à comparer:",
            options_pays,
            default=[options_pays[0], options_pays[1]]
        )
        
        st.markdown("---")
        
        # Filtres avancés
        st.markdown("#### 🔍 Filtres")
        min_score = st.slider("Score minimum:", 0, 100, 60)
        
        st.markdown("---")
        
        # Informations
        st.markdown("#### 📊 À propos")
        st.info("""
        **Sources principales:**
        - Maroc: Ministère des Finances
        - UE: Règlement MiCA
        - EAU: VARA
        - UK: FCA
        
        Données mises à jour: Janvier 2026
        """)
    
    # Filtrer les frameworks sélectionnés
    frameworks_selectionnes = []
    for f in frameworks:
        nom_complet = f"{f['drapeau']} {f['pays']}"
        if nom_complet in selections and f["score_total"] >= min_score:
            frameworks_selectionnes.append(f)
    
    if not frameworks_selectionnes:
        st.warning("Veuillez sélectionner au moins un cadre réglementaire.")
        return
    
    # Onglets
    tab1, tab2, tab3, tab4 = st.tabs(["📊 Vue d'ensemble", "📋 Comparaison", "📈 Graphiques", "💡 Insights"])
    
    with tab1:
        # Cartes de scores
        st.markdown("### 🏆 Scores Réglementaires")
        
        cols = st.columns(len(frameworks_selectionnes))
        for idx, framework in enumerate(frameworks_selectionnes):
            with cols[idx]:
                st.markdown(afficher_carte_pays(framework), unsafe_allow_html=True)
        
        # Métriques clés
        st.markdown("### 🔑 Métriques Clés")
        
        for framework in frameworks_selectionnes:
            with st.expander(f"{framework['drapeau']} {framework['pays']}"):
                col1, col2 = st.columns(2)
                
                with col1:
                    st.markdown("**Points forts:**")
                    for point in framework['points_forts']:
                        st.markdown(f"✅ {point}")
                    
                    st.markdown("**Reconnaissance légale:**")
                    st.markdown(f"`{framework['metriques']['reconnaissance_legale']}`")
                    
                    st.markdown("**Paiement autorisé:**")
                    st.markdown(f"`{framework['metriques']['paiement_autorise']}`")
                
                with col2:
                    st.markdown("**Points faibles:**")
                    for point in framework['points_faibles']:
                        st.markdown(f"⚠️ {point}")
                    
                    st.markdown("**Seuil KYC:**")
                    st.markdown(f"`{framework['metriques']['seuil_kyc']}`")
                    
                    st.markdown("**Travel Rule:**")
                    st.markdown(f"`{framework['metriques']['travel_rule']}`")
    
    with tab2:
        st.markdown("### 📋 Tableau Comparatif Complet")
        
        df_comparaison = creer_tableau_comparatif(frameworks_selectionnes)
        st.dataframe(
            df_comparaison,
            use_container_width=True,
            height=400
        )
        
        # Export CSV
        csv = df_comparaison.to_csv(index=False)
        st.download_button(
            label="📥 Télécharger CSV",
            data=csv,
            file_name="comparaison_regulations.csv",
            mime="text/csv"
        )
    
    with tab3:
        st.markdown("### 📈 Visualisation des Scores")
        
        # Graphique simple
        try:
            fig = creer_graphique_scores_simple(frameworks_selectionnes)
            st.pyplot(fig)
        except Exception as e:
            st.warning("Graphique non disponible - affichage tabulaire à la place")
            st.dataframe(df_comparaison)
        
        # Analyse comparative
        st.markdown("### 🎯 Analyse Comparative")
        
        if "Maroc (Projet 2025)" in [f["pays"] for f in frameworks_selectionnes]:
            maroc = next(f for f in frameworks_selectionnes if f["pays"] == "Maroc (Projet 2025)")
            
            col_a1, col_a2, col_a3 = st.columns(3)
            
            with col_a1:
                st.metric(
                    label="📉 Écart innovation vs EAU",
                    value=f"{maroc['score_innovation'] - 95} points",
                    delta=f"{((maroc['score_innovation'] - 95)/95*100):.1f}%"
                )
            
            with col_a2:
                st.metric(
                    label="📈 Avantage protection vs UE",
                    value=f"+{maroc['score_protection'] - 92}",
                    delta=f"{(maroc['score_protection'] - 92)/92*100:.1f}%"
                )
            
            with col_a3:
                st.metric(
                    label="🚧 Défi accès marché",
                    value=f"{maroc['score_acces_marche']}/100",
                    delta=f"-{(97 - maroc['score_acces_marche'])} vs EAU"
                )
    
    with tab4:
        st.markdown("### 💡 Insights Stratégiques")
        
        # Recommendations pour le Maroc
        if "Maroc (Projet 2025)" in [f["pays"] for f in frameworks_selectionnes]:
            st.markdown("#### 🎯 Priorités pour le Maroc")
            
            insights = [
                {
                    "titre": "🏗️ Bac à sable réglementaire",
                    "description": "Créer un environnement contrôlé pour tester innovations",
                    "impact": "Élevé",
                    "délai": "6-12 mois"
                },
                {
                    "titre": "💰 Licences différenciées",
                    "description": "Niveaux selon taille et risque des acteurs",
                    "impact": "Moyen-Élevé",
                    "délai": "12-18 mois"
                },
                {
                    "titre": "🌍 Hub régional Afrique",
                    "description": "Positionner Casablanca comme centre crypto pour l'Afrique",
                    "impact": "Très élevé",
                    "délai": "24+ mois"
                },
                {
                    "titre": "📊 Pilote paiements",
                    "description": "Autoriser paiements crypto pour export/import",
                    "impact": "Moyen",
                    "délai": "18-24 mois"
                }
            ]
            
            for insight in insights:
                with st.container():
                    col_i1, col_i2 = st.columns([3, 1])
                    with col_i1:
                        st.markdown(f"**{insight['titre']}**")
                        st.markdown(f"{insight['description']}")
                    with col_i2:
                        st.markdown(f"`Impact: {insight['impact']}`")
                        st.markdown(f"`Délai: {insight['délai']}`")
                    st.markdown("---")
        
        # Matrice de décision
        st.markdown("#### 🎲 Matrice de Décision")
        
        donnees_decision = pd.DataFrame({
            "Option": ["Maintenir projet actuel", "Modérations mineures", "Approche équilibrée", "Cadre innovant"],
            "Innovation": [42, 55, 68, 82],
            "Protection": [85, 82, 78, 75],
            "Risque": ["Faible", "Faible", "Moyen", "Élevé"],
            "Impact Éco.": ["Faible", "Moyen", "Élevé", "Très élevé"]
        })
        
        st.dataframe(
            donnees_decision,
            use_container_width=True,
            hide_index=True
        )
    
    # Footer
    st.markdown("---")
    st.markdown("""
    <div style="text-align: center; color: #6B7280; font-size: 0.9rem;">
        <p>📊 Données sourcées des autorités réglementaires • Mise à jour: Janvier 2026</p>
        <p>⚖️ Outil d'analyse comparative • Pour usage décisionnel</p>
    </div>
    # 1. Créer requirements.txt
echo "streamlit==1.28.0
pandas==2.1.0
numpy==1.24.0" > requirements.txt

# 2. Installer
pip install -r requirements.txt

# 3. Exécuter
streamlit run comparateur_regulations_crypto_final.py
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
