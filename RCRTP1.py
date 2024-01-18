import streamlit as st
import pydds
from pydds import MassFunction

def diagnostic_medical():
    st.header("Exemple 1: Diagnostic médical")

    # Simulation des évaluations médicales
    m1 = MassFunction({'F': 0.4, 'M': 0.45, 'C': 0.15})
    m2 = MassFunction({'M': 0.75, '': 0.25})
    m3 = MassFunction({'B': 0.18, 'M': 0.35, 'C': 0.5, 'N': 0.02})

    # Affichage des évaluations médicales
    st.subheader("Évaluations médicales")
    st.text(f"Expert 1: {m1}")
    st.text(f"Expert 2: {m2}")
    st.text(f"Expert 3: {m3}")

    # Fusion des évaluations médicales
    result = m1.combine_conjunctive(m2, m3)

    # Affichage du résultat de la fusion
    st.subheader("Résultat de la fusion (Dempster-Shafer Combinaison rule)")
    st.text(f"Résultat: {result}")

def recommandation_produits():
    st.header("Exemple 2: Évaluation de produits en ligne")

    # Simulation des évaluations de recommandation
    m1 = MassFunction({'B': 0.3, 'M': 0.4, 'C': 0.2, 'N': 0.1})
    m2 = MassFunction({'B': 0.1, 'M': 0.5, 'C': 0.3, 'N': 0.1})
    m3 = MassFunction({'B': 0.2, 'M': 0.3, 'C': 0.4, 'N': 0.1})

    # Affichage des évaluations de recommandation
    st.subheader("Évaluations de recommandation")
    st.text(f"Expert 1: {m1}")
    st.text(f"Expert 2: {m2}")
    st.text(f"Expert 3: {m3}")

    # Fusion des évaluations de recommandation
    result = m1.combine_conjunctive(m2, m3)

    # Affichage du résultat de la fusion
    st.subheader("Résultat de la fusion (Dempster-Shafer Combinaison rule)")
    st.text(f"Résultat: {result}")

def main():
    st.sidebar.title("Choisissez un exemple")
    selected_example = st.sidebar.radio("", ["Diagnostic médical", "Recommandation de produits en ligne"])

    if selected_example == "Diagnostic médical":
        diagnostic_medical()
    elif selected_example == "Recommandation de produits en ligne":
        recommandation_produits()

if __name__ == "__main__":
    main()
