import streamlit as st
from pgmpy.factors.discrete import TabularCPD
from pgmpy.models import BayesianNetwork
from pgmpy.inference import VariableElimination
import networkx as nx
import random
import matplotlib.pyplot as plt

def part2():
    st.title("Partie 2 - Bayesian Network")

    model = BayesianNetwork([('TempsEtude', 'Reussite'), ('Stress', 'Reussite')])
    nx_graph = nx.DiGraph(model.edges())
    nx.draw(nx_graph, with_labels=True, font_weight='bold', node_size=3200, node_color='skyblue', font_size=8, font_color='black', arrowsize=10)
    st.pyplot()

    Tempetu_cpd = TabularCPD(variable='TempsEtude', variable_card=2, values=[[0.3], [0.7]])
    Stress_cpd = TabularCPD(variable='Stress', variable_card=2, values=[[0.4], [0.6]])
    Reussite_cpd = TabularCPD(variable='Reussite', variable_card=2, values=[[0.99,0.8,0.7,0.4], [0.01,0.2,0.3,0.6]], evidence=['TempsEtude', 'Stress'], evidence_card=[2, 2])

    model.add_cpds(Tempetu_cpd, Stress_cpd, Reussite_cpd)
    st.write("Conditional Probability Distributions:")
    st.write(model.get_cpds())

    st.write("Active Trail Nodes:")
    st.write(model.active_trail_nodes('TempsEtude'))
    st.write(model.active_trail_nodes('Stress'))
    st.write(model.active_trail_nodes('Reussite'))

    inference = VariableElimination(model)
    st.write("Query Results:")
    probability = inference.query(variables=['TempsEtude'])
    st.text(probability)

    probability = inference.query(variables=['Stress'])
    st.text(probability)

    probability = inference.query(variables=['Reussite'], evidence={'TempsEtude': 1})
    st.text(probability)

    probability = inference.query(variables=['Reussite'], evidence={'Stress': 1})
    st.text(probability)

    probability = inference.query(variables=['Reussite'], evidence={'TempsEtude': 1, 'Stress': 0})
    st.text(probability)

    probability = inference.query(variables=['Reussite'], evidence={'TempsEtude': 1, 'Stress': 1})
    st.text(probability)

def part3():
    st.title("Partie 3 - Bayesian Network")

    model = BayesianNetwork([('TypeContenu', 'Partage'), ('NombreAmis', 'Partage'), ('PopularitePost', 'Partage'),('PopularitePost', 'NombreAmis')])
    nx_graph = nx.DiGraph(model.edges())
    nx.draw(nx_graph, with_labels=True, font_weight='bold', node_size=3200, node_color='skyblue', font_size=8, font_color='black', arrowsize=10)
    st.pyplot()

    TypeContenu_cpd=TabularCPD(variable='TypeContenu', variable_card=2, values=[[0.8], [0.2]])
    PopularitePost_cpd = TabularCPD(variable='PopularitePost', variable_card=2, values=[[0.5], [0.5]])
    Partage_cpd = TabularCPD(variable='Partage', variable_card=2, values=[[0.2,0.3,0.7,0.1,0.9,0.6,0.4,0.11],[0.8,0.7,0.3,0.9,0.1,0.4,0.6,0.89]], evidence=['TypeContenu', 'NombreAmis', 'PopularitePost'], evidence_card=[2, 2, 2])
    NombreAmis_cpd = TabularCPD(variable='NombreAmis', variable_card=2, values=[[0.7,0.3],[0.3,0.7]], evidence=['PopularitePost'], evidence_card=[2])

    model.add_cpds(TypeContenu_cpd, PopularitePost_cpd, Partage_cpd, NombreAmis_cpd)
    st.write("Conditional Probability Distributions:")
    st.write(model.get_cpds())

    st.write("Active Trail Nodes:")
    st.write(model.active_trail_nodes('TypeContenu'))
    st.write(model.active_trail_nodes('NombreAmis'))
    st.write(model.active_trail_nodes('PopularitePost'))
    st.write(model.active_trail_nodes('Partage'))

    inference = VariableElimination(model)
    st.write("Query Results:")
    probability = inference.query(variables=['TypeContenu'])
    st.text(probability)

    probability = inference.query(variables=['NombreAmis'])
    st.text(probability)

    probability = inference.query(variables=['PopularitePost'])
    st.text(probability)

    probability = inference.query(variables=['Partage'])
    st.text(probability)

    probability = inference.query(variables=['Partage'], evidence={'TypeContenu': 1})
    st.text(probability)

    probability = inference.query(variables=['Partage'], evidence={'TypeContenu': 1, 'NombreAmis': 0, 'PopularitePost': 1})
    st.text(probability)

def part4(nbn,nbma):
    st.title("Partie 4 - Bayesian Network")

    model = BayesianNetwork()
    num_variables = nbn
    model.add_nodes_from(range(num_variables))
    data0=dict()
    for i in range(num_variables):
        data0[i]=[]
    for i in range(1, num_variables):
        parents = random.sample(range(i), min(nbma, i))
        model.add_edges_from([(parent, i) for parent in parents])
        for parent in parents:
            data0[i].append(parent)
    l=[]
    for i in range(num_variables):
        if len(data0[i])==0:
            prob=random.random()
            l.append(TabularCPD(variable=i, variable_card=2, values=[[prob], [1-prob]]))
        else:
            left=[]
            right=[]
            long=2**len(data0[i])
            for j in range(long):
                left.append(random.random())
                right.append(1-left[j])

            l.append(TabularCPD(variable=i, variable_card=2, values=[left,right], evidence=data0[i], evidence_card=[2 for j in range(len(data0[i]))]))

    nx_graph = nx.DiGraph(model.edges())
    nx.draw(nx_graph, with_labels=True, font_weight='bold', node_size=3200, node_color='skyblue', font_size=8, font_color='black', arrowsize=10)
    st.pyplot()
    st.write("Conditional Probability Distributions:")
    for i in l:
        model.add_cpds(i)
    st.write(model.get_cpds())

# Sélection de la partie à afficher
if __name__ == "__main__":
    st.set_option('deprecation.showPyplotGlobalUse', False)
    st.sidebar.title("Choisissez la partie a executer")
    partie_selectionnee = st.sidebar.radio("Sélectionnez la partie", ["Partie 2", "Partie 3", "Partie 4"])

    if partie_selectionnee == "Partie 2":
        part2()
    elif partie_selectionnee == "Partie 3":
        part3()
    elif partie_selectionnee == "Partie 4":
        st.sidebar.header("Entrées")
        nbn = st.sidebar.slider("nombre do noed", min_value=1, max_value=100, value=1)
        nbma = st.sidebar.slider("nombre maximeum d'ark dans un noed", min_value=0, max_value=nbn, value=1)
        part4(nbn,nbma)
