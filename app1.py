import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

def calculate_ratios(data):
    # Ratios sélectionnés
    fond_de_roulement = data['actifs_courts_termes'] / data['passifs_courts_termes']
    marge_nette = round((data['resultat_net'] / data['revenus']) * 100, 1)
    ratio_endettement = round(data['passifs_totaux'] / data['capitaux_propres'], 1)
    roe = round((data['resultat_net'] / data['capitaux_propres']) * 100, 1)

    # Calcul du CMPC (WACC)
    # WACC = (E/(E+D)) * r_e + (D/(E+D)) * r_d * (1 - T)
    total_capital = data['capitaux_propres'] + data['passifs_totaux']
    if total_capital > 0:
        wacc = (data['capitaux_propres'] / total_capital) * data['cost_of_equity'] + \
               (data['passifs_totaux'] / total_capital) * data['cost_of_debt'] * (1 - data['taux_imposition'])
    else:
        wacc = 0.0

    cmpc_percent = round(wacc * 100, 1)

    return {
        "Fond de roulement": round(fond_de_roulement, 1),
        "Marge nette (%)": marge_nette,
        "Ratio d’endettement": ratio_endettement,
        "ROE (Rentabilité des capitaux propres) (%)": roe,
        "CMPC (WACC) (%)": cmpc_percent
    }

def generate_wacc(equity, debt, re, rd, t):
    # Génère un WACC selon la formule WACC = (E/(E+D))*re + (D/(E+D))*rd*(1 - t)
    total = equity + debt
    if total == 0:
        return 0
    return (equity/total)*re + (debt/total)*rd*(1 - t)

def generate_recommendations(ratios, moyennes):
    recommendations = []
    for ratio, value in ratios.items():
        if ratio not in moyennes:
            # Pas de comparaison si le ratio n'est pas dans la moyenne sectorielle
            continue
        moyenne = moyennes[ratio]
        if moyenne == 0:
            # Évite la division par zéro ou la comparaison improbable
            recommendations.append(f"✅ {ratio}: Aucune donnée sectorielle pour comparer.")
            continue

        # Calcul de l'écart relatif
        seuil_haut = moyenne * 1.2
        seuil_bas = moyenne * 0.8

        if value > seuil_haut:
            if ratio == "Fond de roulement":
                details = ("Un fond de roulement nettement supérieur à la moyenne peut signifier une excellente "
                           "capacité à gérer ses liquidités et à faire face à ses engagements à court terme. "
                           "Toutefois, un trop grand écart peut aussi indiquer un excès de liquidités peu investies.")
            elif ratio == "Marge nette (%)":
                details = ("Une marge nette nettement plus élevée que la moyenne du secteur peut être le résultat d'une "
                           "efficacité opérationnelle remarquable ou d'un positionnement de prix avantageux. "
                           "Mais assurez-vous de ne pas négliger la R&D, la qualité ou le service client.")
            elif ratio == "Ratio d’endettement":
                details = ("Un ratio d’endettement significativement plus élevé peut impliquer un levier financier important, "
                           "amplifiant à la fois les bénéfices et les risques. Une vigilance accrue sur la capacité de remboursement "
                           "et les coûts d’intérêt est nécessaire.")
            elif ratio == "ROE (Rentabilité des capitaux propres) (%)":
                details = ("Un ROE nettement plus élevé indique que l'entreprise utilise de manière très efficace "
                           "les capitaux investis. Toutefois, vérifiez si cette rentabilité résulte d’une forte prise de risque "
                           "ou d’un endettement excessif.")
            elif ratio == "CMPC (WACC) (%)":
                details = ("Un CMPC nettement plus élevé que celui du secteur peut indiquer que le marché perçoit "
                           "l’entreprise comme plus risquée, ou que le coût de financement est plus onéreux. "
                           "Tenter d’optimiser la structure financière pourrait réduire ce coût.")
            else:
                details = ("La valeur de ce ratio est nettement supérieure à la moyenne sectorielle, "
                           "ce qui peut être un signe de performance, mais également un indicateur de risque.")
            recommendations.append(f"🔼 {ratio}: La valeur est significativement plus élevée que la moyenne sectorielle. {details}")

        elif value < seuil_bas:
            if ratio == "Fond de roulement":
                details = ("Un fond de roulement trop bas peut signifier un risque élevé de problèmes de liquidité. "
                           "Il convient de revoir la gestion des stocks, des créances et du crédit fournisseur.")
            elif ratio == "Marge nette (%)":
                details = ("Une marge nette inférieure à la moyenne suggère une pression sur les coûts ou "
                           "une politique tarifaire moins avantageuse. Vous pourriez chercher à réduire vos charges "
                           "ou améliorer votre positionnement sur le marché.")
            elif ratio == "Ratio d’endettement":
                details = ("Un endettement trop faible par rapport au secteur peut signifier un faible levier financier, "
                           "mais également une perte d’opportunité si la dette peut financer une croissance rentable.")
            elif ratio == "ROE (Rentabilité des capitaux propres) (%)":
                details = ("Un ROE bas peut indiquer une mauvaise utilisation des ressources ou une rentabilité insuffisante. "
                           "Réévaluez la stratégie, la structure des coûts et la croissance potentielle.")
            elif ratio == "CMPC (WACC) (%)":
                details = ("Un CMPC bien plus bas que la moyenne du secteur peut sembler positif (faible risque, financement peu coûteux), "
                           "mais vérifiez si la rentabilité couvre ce coût du capital. Un CMPC trop bas peut aussi refléter "
                           "une structure inadaptée ou des opportunités de rendement manquées.")
            else:
                details = ("La valeur de ce ratio est nettement inférieure à la moyenne. "
                           "Assurez-vous que ce résultat reflète un choix stratégique et non un manque de performance.")
            recommendations.append(f"🔽 {ratio}: La valeur est inférieure à la moyenne sectorielle. {details}")
        else:
            if ratio == "Fond de roulement":
                details = ("Votre fond de roulement est dans la moyenne. Veillez à maintenir un bon équilibre "
                           "entre liquidités disponibles et investissements à court terme.")
            elif ratio == "Marge nette (%)":
                details = ("Votre marge nette est dans la moyenne du secteur. Une marge stable ou en légère progression "
                           "peut être un signe de bonne gestion opérationnelle.")
            elif ratio == "Ratio d’endettement":
                details = ("Votre ratio d’endettement est en ligne avec celui du secteur. Continuez à surveiller "
                           "votre capacité de remboursement et vos coûts de financement.")
            elif ratio == "ROE (Rentabilité des capitaux propres) (%)":
                details = ("Votre ROE est conforme à la moyenne sectorielle. Il peut être intéressant de cibler "
                           "des améliorations opérationnelles pour pousser la rentabilité.")
            elif ratio == "CMPC (WACC) (%)":
                details = ("Votre CMPC est aligné sur la moyenne sectorielle. Assurez-vous que votre rendement "
                           "dépasse ce coût du capital pour créer de la valeur.")
            else:
                details = ("La valeur de ce ratio est proche de la moyenne, ce qui indique une performance standard "
                           "par rapport au secteur.")
            recommendations.append(f"✅ {ratio}: La valeur est conforme aux standards du secteur. {details}")
    return recommendations

# Moyennes sectorielles pour comparaison (y compris CMPC (WACC) (%) )
moyennes_sectorielles = {
    "Technologie": {
        "Fond de roulement": 1.8,
        "Marge nette (%)": 15.0,
        "Ratio d’endettement": 0.5,
        "ROE (Rentabilité des capitaux propres) (%)": 18.0,
        "CMPC (WACC) (%)": 8.0
    },
    "Santé": {
        "Fond de roulement": 2.2,
        "Marge nette (%)": 12.0,
        "Ratio d’endettement": 0.4,
        "ROE (Rentabilité des capitaux propres) (%)": 14.0,
        "CMPC (WACC) (%)": 7.5
    },
    "Finance": {
        "Fond de roulement": 1.5,
        "Marge nette (%)": 20.0,
        "Ratio d’endettement": 0.8,
        "ROE (Rentabilité des capitaux propres) (%)": 12.0,
        "CMPC (WACC) (%)": 6.5
    },
    "Industrie": {
        "Fond de roulement": 1.7,
        "Marge nette (%)": 10.0,
        "Ratio d’endettement": 0.6,
        "ROE (Rentabilité des capitaux propres) (%)": 10.0,
        "CMPC (WACC) (%)": 9.2
    },
    "Énergie": {
        "Fond de roulement": 1.4,
        "Marge nette (%)": 8.0,
        "Ratio d’endettement": 0.7,
        "ROE (Rentabilité des capitaux propres) (%)": 9.0,
        "CMPC (WACC) (%)": 8.8
    },
    "Consommation discrétionnaire": {
        "Fond de roulement": 1.6,
        "Marge nette (%)": 7.0,
        "Ratio d’endettement": 0.5,
        "ROE (Rentabilité des capitaux propres) (%)": 11.0,
        "CMPC (WACC) (%)": 8.3
    },
    "Consommation de base": {
        "Fond de roulement": 1.9,
        "Marge nette (%)": 9.0,
        "Ratio d’endettement": 0.4,
        "ROE (Rentabilité des capitaux propres) (%)": 10.0,
        "CMPC (WACC) (%)": 7.9
    },
    "Immobilier": {
        "Fond de roulement": 1.3,
        "Marge nette (%)": 18.0,
        "Ratio d’endettement": 1.0,
        "ROE (Rentabilité des capitaux propres) (%)": 8.0,
        "CMPC (WACC) (%)": 6.8
    },
    "Matériaux": {
        "Fond de roulement": 1.7,
        "Marge nette (%)": 11.0,
        "Ratio d’endettement": 0.6,
        "ROE (Rentabilité des capitaux propres) (%)": 12.0,
        "CMPC (WACC) (%)": 8.5
    },
    "Télécommunications": {
        "Fond de roulement": 1.5,
        "Marge nette (%)": 16.0,
        "Ratio d’endettement": 0.7,
        "ROE (Rentabilité des capitaux propres) (%)": 13.0,
        "CMPC (WACC) (%)": 9.0
    }
}

# Interface Streamlit
st.set_page_config(page_title="Analyse Financière", layout="wide")

# Page d'accueil
st.title("📊 Tableau de bord d'analyse financière")
st.write("Bienvenue sur le tableau de bord d'analyse financière. Entrez les données de votre entreprise et comparez vos ratios, y compris le CMPC, aux moyennes du secteur.")

# Sélection de l'industrie
industrie = st.sidebar.selectbox("Sélectionnez votre industrie", list(moyennes_sectorielles.keys()))

# Inputs utilisateur
st.sidebar.header("📋 Données de l'entreprise")
revenus = st.sidebar.number_input("Chiffre d'affaires", min_value=0.0, step=1000.0)
resultat_net = st.sidebar.number_input("Résultat net", min_value=0.0, step=1000.0)
actifs_courts_termes = st.sidebar.number_input("Actifs à court terme", min_value=0.0, step=1000.0)
passifs_courts_termes = st.sidebar.number_input("Passifs à court terme", min_value=0.0, step=1000.0)
actifs_totaux = st.sidebar.number_input("Actifs totaux", min_value=0.0, step=1000.0)
passifs_totaux = st.sidebar.number_input("Passifs totaux", min_value=0.0, step=1000.0)
capitaux_propres = st.sidebar.number_input("Capitaux propres", min_value=0.0, step=1000.0)

# Inputs pour le calcul du CMPC
st.sidebar.subheader("Paramètres du CMPC")
cost_of_equity = st.sidebar.number_input("Coût des fonds propres (r_e)", min_value=0.0, max_value=1.0, value=0.1, step=0.01)
cost_of_debt = st.sidebar.number_input("Coût de la dette (r_d)", min_value=0.0, max_value=1.0, value=0.05, step=0.01)
taux_imposition = st.sidebar.number_input("Taux d'imposition (0-1)", min_value=0.0, max_value=1.0, value=0.25, step=0.01)

# Calcul des ratios si toutes les valeurs sont renseignées
if st.sidebar.button("🔍 Analyser"):
    data = {
        'revenus': revenus,
        'resultat_net': resultat_net,
        'actifs_courts_termes': actifs_courts_termes,
        'passifs_courts_termes': passifs_courts_termes,
        'actifs_totaux': actifs_totaux,
        'passifs_totaux': passifs_totaux,
        'capitaux_propres': capitaux_propres,
        'cost_of_equity': cost_of_equity,
        'cost_of_debt': cost_of_debt,
        'taux_imposition': taux_imposition
    }

    # 1) Calcul des ratios
    ratios = calculate_ratios(data)
    moyennes = moyennes_sectorielles[industrie]

    # 2) Tableaux
    st.write("### 📈 Ratios Financiers de l'entreprise (incluant le CMPC)")
    df_ratios = pd.DataFrame(ratios.items(), columns=["Ratio", "Valeur entreprise"])
    st.dataframe(df_ratios, hide_index=True)

    st.write(f"### 📊 Comparaison avec la moyenne du secteur : {industrie}")
    df_comparaison = pd.DataFrame({
        "Ratio": list(moyennes.keys()),
        "Valeur entreprise": [ratios.get(r, 0) for r in moyennes.keys()],
        "Moyenne sectorielle": list(moyennes.values())
    })
    st.dataframe(df_comparaison, hide_index=True)

    # 3) Recommandations textuelles
    recommendations = generate_recommendations(ratios, moyennes)
    st.write("### 💡 Recommandations")
    for rec in recommendations:
        st.write(rec)

    # 4) Graphique comparatif (Ratios)
    st.write("### 📊 Visualisation des ratios")
    fig, ax = plt.subplots(figsize=(8, 5))
    x = np.arange(len(moyennes.keys()))
    width = 0.35

    # Valeurs pour l'entreprise et le secteur dans le même ordre
    entreprise_values = [ratios.get(r, 0) for r in moyennes.keys()]
    secteur_values = list(moyennes.values())

    bars1 = ax.bar(x - width/2, entreprise_values, width, label="Entreprise", color='skyblue')
    bars2 = ax.bar(x + width/2, secteur_values, width, label="Moyenne sectorielle", color='orange', alpha=0.7)

    ax.set_xticks(x)
    ax.set_xticklabels(moyennes.keys(), rotation=45, ha='right')
    ax.legend()

    for bar in bars1 + bars2:
        ax.text(bar.get_x() + bar.get_width()/2, bar.get_height(), f'{bar.get_height():.1f}', ha='center', va='bottom', fontsize=9)

    st.pyplot(fig)

# Documentation / Help
if st.sidebar.checkbox("📚 Voir la documentation / Aide"):
    st.write("# Documentation / Aide")
    st.write("## Les principaux ratios")
    st.markdown("""  
    **Fond de roulement** : Mesure la capacité de l'entreprise à faire face à ses obligations à court terme.  
    **Marge nette (%)** : Pourcentage qui indique la rentabilité après toutes charges.  
    **Ratio d’endettement** : Évalue la proportion de dettes par rapport aux capitaux propres.  
    **ROE** : Return on Equity, ou rentabilité des capitaux propres, indique comment l'entreprise rémunère ses actionnaires.  
    **CMPC (WACC) (%)** : Coût moyen pondéré du capital, reflète le coût global du financement (fonds propres + dettes) de l'entreprise.  
    """)

    st.write("## Logique de calcul du CMPC")
    st.markdown("""  
    Le CMPC (WACC) est calculé selon la formule :   
    \( CMPC = rac{E}{E + D} 	imes r_e + rac{D}{E + D} 	imes r_d 	imes (1 - T) \)  
    - E : Montant des capitaux propres  
    - D : Montant de la dette  
    - \( r_e \) : Coût des fonds propres  
    - \( r_d \) : Coût de la dette  
    - T : Taux d'imposition  
    """)

    
