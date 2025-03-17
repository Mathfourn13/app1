import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

# Configuration de la mise en page et du style
st.set_page_config(page_title='Application Financière', layout='wide')
st.markdown("""
    <style>
        body {background-color: #121212; color: white;}
        .main {background-color: #1e1e1e;}
    </style>
""", unsafe_allow_html=True)

def calcul_cmpc():
    st.title("Calcul du CMPC")
    
    st.sidebar.subheader("Paramètres du CMPC")
    ke = st.sidebar.number_input("Coût des fonds propres (%)", min_value=0.0, max_value=100.0, value=10.0) / 100
    kd = st.sidebar.number_input("Coût de la dette (%)", min_value=0.0, max_value=100.0, value=5.0) / 100
    taxe = st.sidebar.number_input("Taux d'imposition (%)", min_value=0.0, max_value=100.0, value=30.0) / 100
    poids_fonds_propres = st.sidebar.slider("Proportion des fonds propres", min_value=0.0, max_value=1.0, value=0.6)
    poids_dette = 1 - poids_fonds_propres
    
    cmpc = (poids_fonds_propres * ke) + (poids_dette * kd * (1 - taxe))
    
    st.write(f"### CMPC Calculé : {cmpc:.2%}")
    
    fig, ax = plt.subplots()
    ax.pie([poids_fonds_propres, poids_dette], labels=["Fonds Propres", "Dette"], autopct='%1.1f%%', colors=['#003f5c', '#bc5090'])
    ax.set_title("Structure du Capital")
    st.pyplot(fig)

def valeur_future():
    st.title("Valeur Future d'un Investissement")
    
    st.sidebar.subheader("Paramètres de la Valeur Future")
    capital_initial = st.sidebar.number_input("Montant initial (en $ CAD)", min_value=0.0, value=1000.0)
    taux_interet = st.sidebar.number_input("Taux d'intérêt annuel (%)", min_value=0.0, max_value=100.0, value=5.0) / 100
    duree = st.sidebar.slider("Durée de l'investissement (années)", min_value=1, max_value=50, value=10)
    
    valeurs = [capital_initial * (1 + taux_interet) ** t for t in range(duree + 1)]
    
    st.write(f"### Valeur Future après {duree} ans : {valeurs[-1]:,.2f} $ CAD")
    
    fig, ax = plt.subplots()
    ax.plot(range(duree + 1), valeurs, marker='o', linestyle='-', color='#ff6361')
    ax.set_title("Évolution de la Valeur Future")
    ax.set_xlabel("Années")
    ax.set_ylabel("Montant ($ CAD)")
    ax.grid(True, linestyle='--', alpha=0.6)
    ax.set_facecolor('#1e1e1e')
    st.pyplot(fig)

def valeur_presente():
    st.title("Valeur Présente d'un Investissement")
    
    st.sidebar.subheader("Paramètres de la Valeur Présente")
    capital_futur = st.sidebar.number_input("Montant futur (en $ CAD)", min_value=0.0, value=2000.0)
    taux_actualisation = st.sidebar.number_input("Taux d'actualisation (%)", min_value=0.0, max_value=100.0, value=5.0) / 100
    duree = st.sidebar.slider("Durée de l'investissement (années)", min_value=1, max_value=50, value=10)
    
    valeurs = [capital_futur / ((1 + taux_actualisation) ** t) for t in range(duree + 1)]
    
    st.write(f"### Valeur Présente actuelle : {valeurs[-1]:,.2f} $ CAD")
    
    fig, ax = plt.subplots()
    ax.plot(range(duree + 1), valeurs, marker='o', linestyle='-', color='#ffa600')
    ax.set_title("Évolution de la Valeur Présente")
    ax.set_xlabel("Années")
    ax.set_ylabel("Montant ($ CAD)")
    ax.grid(True, linestyle='--', alpha=0.6)
    ax.set_facecolor('#1e1e1e')
    st.pyplot(fig)

# Sidebar pour choisir l'application
st.sidebar.title("Menu")
choix = st.sidebar.radio("Sélectionnez l'application", ["CMPC", "Valeur Future", "Valeur Présente"])

if choix == "CMPC":
    calcul_cmpc()
elif choix == "Valeur Future":
    valeur_future()
elif choix == "Valeur Présente":
    valeur_presente()
