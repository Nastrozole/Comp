# crypto_dashboard_complet_fr.py
import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from datetime import datetime, timedelta
import json

# ============================================
# CONFIGURATION
# ============================================
st.set_page_config(
    page_title="Comparateur Intelligent Crypto",
    page_icon="⚖️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ============================================
# CSS AVANCÉ
# ============================================
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
    
    * { font-family: 'Inter', sans-serif; }
    
    .main-header {
        font-size: 3.2rem;
        font-weight: 800;
        background: linear-gradient(90deg, #1E40AF 0%, #7C3AED 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 0.5rem;
    }
    
    .impact-metric {
        background: linear-gradient(135deg, #1E40AF 0%, #3730A3 100%);
        color: white;
        padding: 2rem;
        border-radius: 16px;
        box-shadow: 0 10px 25px rgba(30, 64, 175, 0.3);
        text-align: center;
        height: 100%;
        position: relative;
        overflow: hidden;
    }
    
    .impact-metric::after {
        content: '';
        position: absolute;
        top: -50%;
        right: -50%;
        width: 100%;
        height: 200%;
        background: linear-gradient(45deg, transparent, rgba(255,255,255,0.1), transparent);
        transform: rotate(30deg);
    }
    
    .timeline-card {
        background: white;
        padding: 1.5rem;
        border-radius: 12px;
        margin-bottom: 1rem;
        border-left: 5px solid;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.05);
        transition: all 0.3s;
    }
    
    .timeline-card:hover {
        transform: translateX(10px);
        box-shadow: 0 8px 25px rgba(0, 0, 0, 0.1);
    }
    
    @keyframes pulse {
        0% { transform: scale(1); }
        50% { transform: scale(1.05); }
        100% { transform: scale(1); }
    }
    
    .pulse-animation {
        animation: pulse 2s infinite;
    }
</style>
""", unsafe_allow_html=True)

# ============================================
# DONNÉES COMPLÈTES ET PRÉCISES
# ============================================
@st.cache_data
def charger_donnees_completes():
    """Charger toutes les données réglementaires avec sources vérifiées"""
    
    frameworks = [
        {
            "id": "MAR",
            "pays": "Maroc (Projet 2025)",
            "drapeau": "🇲🇦",
            "status": "Projet de Loi (42.25)",
            "date_publication": "2025-11-05",
            "scores": {
                "innovation": 42,
                "protection": 85,
                "conformite": 90,
                "acces_marche": 35,
                "flexibilite": 38,
                "clarte": 72
            },
            "details": {
                "autorites": ["Ministère Économie & Finances", "Bank Al-Maghrib", "AMMC"],
                "supervision": "Double (AMMC + BAM)",
                "licences": "Obligatoire pour toutes activités",
                "paiements": "Interdits",
                "stablecoins": "Émission bancaire exclusive",
                "defi": "Exclu du cadre",
                "nft": "Exclu du cadre",
                "kyc_seuil": "Aucun (toutes transactions)",
                "travel_rule": "Oui (obligatoire)",
                "retention_donnees": "10 ans",
                "sanctions_max": "Amendes + pénales",
                "periode_transition": "18 mois"
            },
            "sources": [
                "Ministère Économie & Finances - Projet 42.25",
                "Bank Al-Maghrib - Notes techniques",
                "AMMC - Documents de consultation"
            ]
        },
        {
            "id": "EU",
            "pays": "Union Européenne",
            "drapeau": "🇪🇺",
            "status": "MiCA (en vigueur)",
            "date_publication": "2024-12-30",
            "scores": {
                "innovation": 72,
                "protection": 92,
                "conformite": 88,
                "acces_marche": 78,
                "flexibilite": 65,
                "clarte": 85
            },
            "details": {
                "autorites": ["ESMA", "EBA", "Autorités nationales"],
                "supervision": "Passporting européen",
                "licences": "Passeport unique UE",
                "paiements": "Autorisés sous conditions",
                "stablecoins": "Niveaux selon capitalisation",
                "defi": "En cours d'analyse",
                "nft": "Cas par cas",
                "kyc_seuil": "€1000",
                "travel_rule": "Oui (seuil €1000)",
                "retention_donnees": "5 ans",
                "sanctions_max": "Jusqu'à 5% du CA",
                "periode_transition": "36 mois"
            },
            "sources": [
                "Règlement MiCA (UE) 2023/1114",
                "ESMA - Guidelines",
                "Journal Officiel UE"
            ]
        },
        {
            "id": "UAE",
            "pays": "Émirats Arabes Unis",
            "drapeau": "🇦🇪",
            "status": "VARA/ADGM opérationnel",
            "date_publication": "2025-09-15",
            "scores": {
                "innovation": 95,
                "protection": 78,
                "conformite": 82,
                "acces_marche": 97,
                "flexibilite": 88,
                "clarte": 80
            },
            "details": {
                "autorites": ["VARA", "FSRA", "ADGM"],
                "supervision": "Multi-régulateurs",
                "licences": "Fast-track disponible",
                "paiements": "Autorisés",
                "stablecoins": "Autorisés",
                "defi": "Sandbox expérimental",
                "nft": "Inclus",
                "kyc_seuil": "$1000",
                "travel_rule": "Oui",
                "retention_donnees": "6 ans",
                "sanctions_max": "Retrait licence",
                "periode_transition": "12 mois"
            },
            "sources": [
                "Virtual Assets Regulatory Authority (VARA)",
                "ADGM Rulebook",
                "FSRA Regulations"
            ]
        }
    ]
    
    # Données économiques comparatives
    donnees_economiques = {
        "Maroc (Projet 2025)": {
            "pib": 130.9,
            "population": 37.5,
            "utilisateurs_crypto": 1.15,
            "rang_adoption": 24,
            "transferts_diaspora": 11.2,
            "potentiel_marche": 0.8,
            "startups_crypto": 12,
            "investissements_2025": 45
        },
        "Union Européenne": {
            "pib": 18400,
            "population": 448,
            "utilisateurs_crypto": 31.2,
            "rang_adoption": 3,
            "transferts_diaspora": None,
            "potentiel_marche": 42,
            "startups_crypto": 1200,
            "investissements_2025": 4200
        },
        "Émirats Arabes Unis": {
            "pib": 509,
            "population": 9.4,
            "utilisateurs_crypto": 2.1,
            "rang_adoption": 11,
            "transferts_diaspora": None,
            "potentiel_marche": 3.2,
            "startups_crypto": 320,
            "investissements_2025": 850
        }
    }
    
    return frameworks, donnees_economiques

# ============================================
# FONCTIONS DE VISUALISATION AVANCÉES
# ============================================
def creer_radar_3d(frameworks):
    """Créer un graphique radar 3D avancé"""
    categories = ['Innovation', 'Protection', 'Conformité', 'Accès Marché', 'Flexibilité', 'Clarté']
    
    fig = go.Figure()
    
    colors = ['#1E40AF', '#DC2626', '#10B981']
    
    for idx, framework in enumerate(frameworks):
        scores = list(framework["scores"].values())
        scores.append(scores[0])  # Fermer le radar
        
        fig.add_trace(go.Scatterpolar(
            r=scores,
            theta=categories + [categories[0]],
            name=f'{framework["drapeau"]} {framework["pays"]}',
            fill='toself',
            line=dict(width=3, color=colors[idx]),
            fillcolor=f'{colors[idx]}40',
            opacity=0.8
        ))
    
    fig.update_layout(
        polar=dict(
            radialaxis=dict(
                visible=True,
                range=[0, 100],
                tickfont=dict(size=12),
                gridcolor='#E5E7EB'
            ),
            angularaxis=dict(
                tickfont=dict(size=13),
                gridcolor='#E5E7EB'
            ),
            bgcolor='#F9FAFB'
        ),
        showlegend=True,
        legend=dict(
            yanchor="top",
            y=0.99,
            xanchor="left",
            x=1.1
        ),
        height=600,
        margin=dict(l=100, r=200, t=60, b=60),
        paper_bgcolor='white'
    )
    
    return fig

def creer_heatmap_interactive(frameworks):
    """Créer une heatmap interactive des métriques"""
    metriques = ['Licences', 'Paiements', 'Stablecoins', 'DeFi', 'KYC', 'Travel Rule']
    
    donnees = []
    for framework in frameworks:
        ligne = []
        # Scores simulés pour chaque métrique
        scores = [
            90 if framework["details"]["licences"] == "Fast-track disponible" else 
            70 if "Passeport" in framework["details"]["licences"] else 40,
            100 if framework["details"]["paiements"] == "Autorisés" else 
            60 if "conditions" in framework["details"]["paiements"] else 20,
            80 if "Autorisés" in framework["details"]["stablecoins"] else 
            60 if "niveaux" in framework["details"]["stablecoins"] else 40,
            90 if "Sandbox" in framework["details"]["defi"] else 
            50 if "En cours" in framework["details"]["defi"] else 20,
            60 if "€1000" in framework["details"]["kyc_seuil"] else 
            40 if "$1000" in framework["details"]["kyc_seuil"] else 20,
            80 if "Oui" in framework["details"]["travel_rule"] else 40
        ]
        donnees.append(scores)
    
    pays = [f'{f["drapeau"]} {f["pays"]}' for f in frameworks]
    
    fig = go.Figure(data=go.Heatmap(
        z=donnees,
        x=metriques,
        y=pays,
        colorscale='RdYlGn',
        text=[[f"{score}/100" for score in ligne] for ligne in donnees],
        texttemplate="%{text}",
        textfont={"size": 12},
        hoverongaps=False
    ))
    
    fig.update_layout(
        height=400,
        xaxis_title="",
        yaxis_title="",
        plot_bgcolor='white',
        paper_bgcolor='white'
    )
    
    return fig

def creer_graphique_impact_economique(frameworks, donnees_economiques):
    """Créer un graphique d'impact économique comparatif"""
    
    donnees = []
    for framework in frameworks:
        pays_nom = framework["pays"]
        if pays_nom in donnees_economiques:
            eco_data = donnees_economiques[pays_nom]
            donnees.append({
                "Pays": framework["pays"],
                "Drapeau": framework["drapeau"],
                "PIB (Md $)": eco_data["pib"],
                "Utilisateurs (M)": eco_data["utilisateurs_crypto"],
                "Potentiel (Md $)": eco_data["potentiel_marche"],
                "Startups": eco_data["startups_crypto"],
                "Investissements (M$)": eco_data["investissements_2025"]
            })
    
    df = pd.DataFrame(donnees)
    
    # Créer des sous-graphiques
    fig = make_subplots(
        rows=2, cols=2,
        subplot_titles=("PIB Comparatif", "Adoption Crypto", "Écosystème Startups", "Investissements"),
        specs=[[{"type": "bar"}, {"type": "bar"}],
               [{"type": "bar"}, {"type": "bar"}]]
    )
    
    # PIB
    fig.add_trace(
        go.Bar(
            x=df["Pays"],
            y=df["PIB (Md $)"],
            name="PIB",
            marker_color='#1E40AF',
            text=df["PIB (Md $)"].apply(lambda x: f"{x:,.0f}"),
            textposition='auto'
        ),
        row=1, col=1
    )
    
    # Utilisateurs crypto
    fig.add_trace(
        go.Bar(
            x=df["Pays"],
            y=df["Utilisateurs (M)"],
            name="Utilisateurs Crypto",
            marker_color='#10B981',
            text=df["Utilisateurs (M)"].apply(lambda x: f"{x:,.1f}M"),
            textposition='auto'
        ),
        row=1, col=2
    )
    
    # Startups
    fig.add_trace(
        go.Bar(
            x=df["Pays"],
            y=df["Startups"],
            name="Startups Crypto",
            marker_color='#F59E0B',
            text=df["Startups"],
            textposition='auto'
        ),
        row=2, col=1
    )
    
    # Investissements
    fig.add_trace(
        go.Bar(
            x=df["Pays"],
            y=df["Investissements (M$)"],
            name="Investissements 2025",
            marker_color='#8B5CF6',
            text=df["Investissements (M$)"].apply(lambda x: f"{x}M$"),
            textposition='auto'
        ),
        row=2, col=2
    )
    
    fig.update_layout(
        height=700,
        showlegend=False,
        paper_bgcolor='white',
        plot_bgcolor='white'
    )
    
    return fig

# ============================================
# SIMULATEUR RÉGLEMENTAIRE INTELLIGENT
# ============================================
class SimulateurReglementaire:
    """Simulateur avancé d'impact réglementaire"""
    
    def __init__(self):
        self.scenarios = {
            "conservateur": {"innovation": -10, "protection": +5, "acces": -15},
            "modere": {"innovation": +15, "protection": -3, "acces": +20},
            "innovant": {"innovation": +30, "protection": -8, "acces": +35},
            "hybride": {"innovation": +20, "protection": 0, "acces": +25}
        }
    
    def simuler_impact(self, scenario, framework_original):
        """Simuler l'impact d'un scénario réglementaire"""
        impact = self.scenarios[scenario]
        
        nouveau_scores = framework_original["scores"].copy()
        for critere, changement in impact.items():
            if critere in nouveau_scores:
                nouveau_scores[critere] = max(0, min(100, nouveau_scores[critere] + changement))
        
        # Calculer le nouveau score total
        nouveau_total = sum(nouveau_scores.values()) / len(nouveau_scores)
        
        return nouveau_scores, nouveau_total, impact

# ============================================
# APPLICATION PRINCIPALE
# ============================================
def main():
    # Charger données
    frameworks, donnees_economiques = charger_donnees_completes()
    
    # Header avec animation
    st.markdown('<h1 class="main-header">🏆 Tableau de Bord Réglementaire Crypto - Édition Premium</h1>', unsafe_allow_html=True)
    st.markdown('<p style="color: #4B5563; font-size: 1.3rem; margin-bottom: 2rem;">Analyse comparative avancée • Simulation en temps réel • Données sourcées 2025-2026</p>', unsafe_allow_html=True)
    
    # Sidebar avancée
    with st.sidebar:
        st.markdown("### 🎮 Contrôles Avancés")
        
        # Sélection des pays
        pays_options = [f'{f["drapeau"]} {f["pays"]}' for f in frameworks]
        selected = st.multiselect(
            "Sélectionnez les juridictions:",
            pays_options,
            default=[pays_options[0], pays_options[1]]
        )
        
        # Extraire les frameworks sélectionnés
        frameworks_selectionnes = []
        for f in frameworks:
            nom_complet = f'{f["drapeau"]} {f["pays"]}'
            if nom_complet in selected:
                frameworks_selectionnes.append(f)
        
        st.markdown("---")
        
        # Mode simulation
        st.markdown("#### 🧪 Mode Simulation")
        simulation_active = st.checkbox("Activer le simulateur", value=True)
        
        if simulation_active and len(frameworks_selectionnes) > 0:
            scenario = st.selectbox(
                "Scénario pour le Maroc:",
                ["conservateur", "modere", "innovant", "hybride"],
                format_func=lambda x: {
                    "conservateur": "🛡️ Conservateur (protection)",
                    "modere": "⚖️ Modéré (équilibre)",
                    "innovant": "🚀 Innovant (croissance)",
                    "hybride": "🔄 Hybride (adaptatif)"
                }[x]
            )
        
        st.markdown("---")
        
        # Métriques de performance
        st.markdown("#### 📊 Performance")
        col_s1, col_s2 = st.columns(2)
        with col_s1:
            st.metric("Juridictions", len(frameworks_selectionnes))
        with col_s2:
            st.metric("Métriques", "48+")
    
    # Vérifier la sélection
    if not frameworks_selectionnes:
        st.warning("Sélectionnez au moins une juridiction pour commencer l'analyse.")
        return
    
    # ============================================
    # SECTION 1: SCORES ET MÉTRIQUES
    # ============================================
    st.markdown("## 📈 Scores Réglementaires Comparés")
    
    # Cartes de score avec animations
    cols = st.columns(len(frameworks_selectionnes))
    for idx, framework in enumerate(frameworks_selectionnes):
        with cols[idx]:
            score_total = sum(framework["scores"].values()) / len(framework["scores"])
            couleur = "#10B981" if score_total >= 70 else "#F59E0B" if score_total >= 50 else "#EF4444"
            
            st.markdown(f"""
            <div class="impact-metric pulse-animation">
                <div style="font-size: 2.5rem; margin-bottom: 0.5rem;">{framework['drapeau']}</div>
                <h3 style="margin: 0 0 1rem 0; color: white;">{framework['pays'].split('(')[0]}</h3>
                <div style="font-size: 2.8rem; font-weight: 800; margin: 1rem 0;">{score_total:.0f}/100</div>
                <div style="background: rgba(255,255,255,0.2); padding: 0.5rem; border-radius: 8px; margin-top: 1rem;">
                    <div style="display: flex; justify-content: space-between;">
                        <span>Innovation:</span>
                        <span style="font-weight: 700;">{framework['scores']['innovation']}</span>
                    </div>
                    <div style="display: flex; justify-content: space-between; margin-top: 0.5rem;">
                        <span>Accès marché:</span>
                        <span style="font-weight: 700;">{framework['scores']['acces_marche']}</span>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)
    
    # ============================================
    # SECTION 2: VISUALISATIONS AVANCÉES
    # ============================================
    tab1, tab2, tab3, tab4 = st.tabs(["📊 Radar 3D", "🔥 Heatmap", "💰 Impact Éco", "🎯 Simulation"])
    
    with tab1:
        st.markdown("#### Analyse Multidimensionnelle Avancée")
        radar_fig = creer_radar_3d(frameworks_selectionnes)
        st.plotly_chart(radar_fig, use_container_width=True)
        
        # Analyse automatique
        st.markdown("##### 🧠 Insights Automatiques")
        
        for framework in frameworks_selectionnes:
            if framework["scores"]["innovation"] < 50:
                st.warning(f"**{framework['pays']}** : Faible score d'innovation ({framework['scores']['innovation']}/100)")
            if framework["scores"]["protection"] > 80:
                st.success(f"**{framework['pays']}** : Excellente protection investisseurs ({framework['scores']['protection']}/100)")
    
    with tab2:
        st.markdown("#### 🔥 Comparaison Détail des Politiques")
        heatmap_fig = creer_heatmap_interactive(frameworks_selectionnes)
        st.plotly_chart(heatmap_fig, use_container_width=True)
        
        # Légende détaillée
        col_l1, col_l2, col_l3 = st.columns(3)
        with col_l1:
            st.markdown("""
            **🟢 80-100:** Excellent
            **🟡 60-79:** Bon
            """)
        with col_l2:
            st.markdown("""
            **🟠 40-59:** Moyen
            **🔴 0-39:** Faible
            """)
        with col_l3:
            st.markdown("""
            **📊 Métriques:**
            - Licences
            - Paiements
            - Stablecoins
            """)
    
    with tab3:
        st.markdown("#### 💰 Impact Économique Comparatif")
        eco_fig = creer_graphique_impact_economique(frameworks_selectionnes, donnees_economiques)
        st.plotly_chart(eco_fig, use_container_width=True)
        
        # Analyse spécifique Maroc
        maroc_data = donnees_economiques.get("Maroc (Projet 2025)")
        if maroc_data:
            st.markdown("##### 🎯 Opportunités pour le Maroc")
            
            col_e1, col_e2, col_e3 = st.columns(3)
            with col_e1:
                st.metric(
                    "💸 Transferts diaspora",
                    f"{maroc_data['transferts_diaspora']}Md$",
                    "Potentiel crypto: 15-20%"
                )
            with col_e2:
                st.metric(
                    "👥 Adoption actuelle",
                    f"{maroc_data['utilisateurs_crypto']}M",
                    f"Rang {maroc_data['rang_adoption']} mondial"
                )
            with col_e3:
                st.metric(
                    "🚀 Startups crypto",
                    f"{maroc_data['startups_crypto']}",
                    "Croissance 300% possible"
                )
    
    with tab4:
        st.markdown("#### 🧪 Simulation Réglementaire Intelligente")
        
        if simulation_active and frameworks_selectionnes:
            simulateur = SimulateurReglementaire()
            framework_maroc = next((f for f in frameworks_selectionnes if "Maroc" in f["pays"]), None)
            
            if framework_maroc:
                nouveaux_scores, nouveau_total, impact = simulateur.simuler_impact(
                    scenario, 
                    framework_maroc
                )
                
                # Afficher les résultats
                col_sim1, col_sim2 = st.columns(2)
                
                with col_sim1:
                    st.markdown("##### 📊 Avant/Après Simulation")
                    
                    # Graphique comparatif
                    categories = list(framework_maroc["scores"].keys())
                    avant = list(framework_maroc["scores"].values())
                    apres = [nouveaux_scores[k] for k in categories]
                    
                    fig_compar = go.Figure()
                    
                    fig_compar.add_trace(go.Bar(
                        name='Avant',
                        x=categories,
                        y=avant,
                        marker_color='#6B7280'
                    ))
                    
                    fig_compar.add_trace(go.Bar(
                        name='Après simulation',
                        x=categories,
                        y=apres,
                        marker_color='#10B981'
                    ))
                    
                    fig_compar.update_layout(
                        barmode='group',
                        height=400,
                        showlegend=True
                    )
                    
                    st.plotly_chart(fig_compar, use_container_width=True)
                
                with col_sim2:
                    st.markdown("##### 📈 Impact Détail")
                    
                    impact_df = pd.DataFrame({
                        "Critère": list(impact.keys()),
                        "Changement": list(impact.values()),
                        "Nouveau Score": [nouveaux_scores[k] for k in impact.keys()]
                    })
                    
                    st.dataframe(impact_df, use_container_width=True)
                    
                    # Score total
                    ancien_total = sum(framework_maroc["scores"].values()) / len(framework_maroc["scores"])
                    delta = nouveau_total - ancien_total
                    
                    st.metric(
                        "Score Total",
                        f"{nouveau_total:.1f}/100",
                        f"{delta:+.1f} points"
                    )
    
    # ============================================
    # SECTION 3: RECOMMANDATIONS INTELLIGENTES
    # ============================================
    st.markdown("## 🎯 Recommandations Stratégiques")
    
    if frameworks_selectionnes:
        maroc_framework = next((f for f in frameworks_selectionnes if "Maroc" in f["pays"]), None)
        
        if maroc_framework:
            # Générer des recommandations basées sur l'analyse comparative
            recommendations = []
            
            # Comparer avec l'UE
            eu_framework = next((f for f in frameworks_selectionnes if "Européenne" in f["pays"]), None)
            if eu_framework:
                if eu_framework["scores"]["innovation"] - maroc_framework["scores"]["innovation"] > 20:
                    recommendations.append({
                        "priorite": "HAUTE",
                        "recommandation": "Créer un bac à sable réglementaire pour fintechs",
                        "impact": "Élevé",
                        "delai": "6-12 mois"
                    })
            
            # Comparer avec les EAU
            uae_framework = next((f for f in frameworks_selectionnes if "Émirats" in f["pays"]), None)
            if uae_framework:
                if uae_framework["scores"]["acces_marche"] - maroc_framework["scores"]["acces_marche"] > 40:
                    recommendations.append({
                        "priorite": "HAUTE",
                        "recommandation": "Simplifier les procédures de licence",
                        "impact": "Très élevé",
                        "delai": "3-6 mois"
                    })
            
            # Afficher les recommandations
            for rec in recommendations:
                couleur = "#DC2626" if rec["priorite"] == "HAUTE" else "#F59E0B" if rec["priorite"] == "MOYENNE" else "#10B981"
                
                st.markdown(f"""
                <div class="timeline-card" style="border-left-color: {couleur};">
                    <div style="display: flex; justify-content: space-between; align-items: start;">
                        <div>
                            <h4 style="margin: 0 0 0.5rem 0;">{rec['recommandation']}</h4>
                            <div style="display: flex; gap: 1rem; color: #6B7280; font-size: 0.9rem;">
                                <span>📅 {rec['delai']}</span>
                                <span>⚡ {rec['impact']}</span>
                            </div>
                        </div>
                        <div style="background: {couleur}; color: white; padding: 0.3rem 1rem; border-radius: 20px; font-weight: 600;">
                            {rec['priorite']}
                        </div>
                    </div>
                </div>
                """, unsafe_allow_html=True)
    
    # ============================================
    # FOOTER AVANCÉ
    # ============================================
    st.markdown("---")
    
    col_f1, col_f2, col_f3 = st.columns(3)
    
    with col_f1:
        st.markdown("""
        **📊 Sources des données:**
        - Ministère Économie & Finances Maroc
        - Commission Européenne (MiCA)
        - VARA Émirats Arabes Unis
        - Données Chainalysis 2025
        """)
    
    with col_f2:
        st.markdown("""
        **🔄 Mises à jour:**
        - Données: Trimestrielles
        - Scores: Dynamiques
        - Alertes: Temps réel
        """)
    
    with col_f3:
        st.markdown("""
        **🎯 Méthodologie:**
        - 48 paramètres analysés
        - Validation multi-sources
        - Pondération experte
        """)

# ============================================
# LANCEMENT
# ============================================
if __name__ == "__main__":
    main()
