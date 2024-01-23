import streamlit as st
import numpy as np
from fuzzylogic.classes import Domain, Set, Rule
from fuzzylogic.functions import trapezoid, triangular
import matplotlib.pyplot as plt

def fuzzy_heating_controller():
    st.title("Contrôleur Flou - Système de Chauffage")

    # Définir les domaines, ensembles et règles
    Temperature = Domain('Température ambiante', 0, 30)
    Isolation = Domain('Niveau d\'isolation', 0, 10)
    HeatingPower = Domain('Puissance de chauffage', 0, 100)
    HeaterOutput = Domain('Sortie du chauffage', 0, 100)
    st.set_option('deprecation.showPyplotGlobalUse', False)
    # Définir les ensembles flous pour la température
    Temperature.Cold = trapezoid(0, 5,5, 10)
    Temperature.Moderate = trapezoid(5, 10,10, 20)
    Temperature.Hot =trapezoid(15, 20, 20, 30)
    Temperature.Cold.plot()
    Temperature.Moderate.plot()
    Temperature.Hot.plot() 
 
    st.pyplot()

    # Définir les ensembles flous pour le niveau d'isolation
    Isolation.LowIsolation = trapezoid(0, 2,2, 4)
    Isolation.ModerateIsolation = trapezoid(2, 4, 4, 6)
    Isolation.HighIsolation =trapezoid(4, 6, 6, 10)

    Isolation.LowIsolation.plot()
    Isolation.ModerateIsolation.plot()
    Isolation.HighIsolation.plot() 
 
    st.pyplot()


    # Définir les ensembles flous pour la puissance de chauffage
    HeatingPower.LowPower = trapezoid(0, 20, 20, 40)
    HeatingPower.ModeratePower = trapezoid(20, 40, 40, 60)
    HeatingPower.HighPower = trapezoid(40, 60, 60, 100)

    HeatingPower.LowPower.plot()
    HeatingPower.ModeratePower.plot()
    HeatingPower.HighPower.plot() 
 
    st.pyplot()

    # Définir les ensembles flous pour la sortie du chauffage
    HeaterOutput.LowOutput = trapezoid(0, 20, 20, 40)
    HeaterOutput.ModerateOutput = trapezoid(20, 40, 40, 60)
    HeaterOutput.HighOutput = trapezoid(40, 60, 60, 100)

    HeaterOutput.LowOutput.plot()
    HeaterOutput.ModerateOutput.plot()
    HeaterOutput.HighOutput.plot() 
 
    st.pyplot()

    # Définir les règles
    rules = Rule({
        (Temperature.Cold, Isolation.LowIsolation, HeatingPower.LowPower): HeaterOutput.LowOutput,
        (Temperature.Cold, Isolation.LowIsolation, HeatingPower.ModeratePower): HeaterOutput.ModerateOutput,
        (Temperature.Cold, Isolation.LowIsolation, HeatingPower.HighPower): HeaterOutput.HighOutput,
        (Temperature.Cold, Isolation.ModerateIsolation, HeatingPower.LowPower): HeaterOutput.LowOutput,
        (Temperature.Cold, Isolation.ModerateIsolation, HeatingPower.ModeratePower): HeaterOutput.ModerateOutput,
        (Temperature.Cold, Isolation.ModerateIsolation, HeatingPower.HighPower): HeaterOutput.HighOutput,
        (Temperature.Cold, Isolation.HighIsolation, HeatingPower.LowPower): HeaterOutput.LowOutput,
        (Temperature.Cold, Isolation.HighIsolation, HeatingPower.ModeratePower): HeaterOutput.ModerateOutput,
        (Temperature.Cold, Isolation.HighIsolation, HeatingPower.HighPower): HeaterOutput.HighOutput,
        
        (Temperature.Moderate, Isolation.LowIsolation, HeatingPower.LowPower): HeaterOutput.LowOutput,
        (Temperature.Moderate, Isolation.LowIsolation, HeatingPower.ModeratePower): HeaterOutput.ModerateOutput,
        (Temperature.Moderate, Isolation.LowIsolation, HeatingPower.HighPower): HeaterOutput.HighOutput,
        (Temperature.Moderate, Isolation.ModerateIsolation, HeatingPower.LowPower): HeaterOutput.LowOutput,
        (Temperature.Moderate, Isolation.ModerateIsolation, HeatingPower.ModeratePower): HeaterOutput.ModerateOutput,
        (Temperature.Moderate, Isolation.ModerateIsolation, HeatingPower.HighPower): HeaterOutput.HighOutput,
        (Temperature.Moderate, Isolation.HighIsolation, HeatingPower.LowPower): HeaterOutput.LowOutput,
        (Temperature.Moderate, Isolation.HighIsolation, HeatingPower.ModeratePower): HeaterOutput.ModerateOutput,
        (Temperature.Moderate, Isolation.HighIsolation, HeatingPower.HighPower): HeaterOutput.HighOutput,
        
        (Temperature.Hot, Isolation.LowIsolation, HeatingPower.LowPower): HeaterOutput.LowOutput,
        (Temperature.Hot, Isolation.LowIsolation, HeatingPower.ModeratePower): HeaterOutput.ModerateOutput,
        (Temperature.Hot, Isolation.LowIsolation, HeatingPower.HighPower): HeaterOutput.HighOutput,
        (Temperature.Hot, Isolation.ModerateIsolation, HeatingPower.LowPower): HeaterOutput.LowOutput,
        (Temperature.Hot, Isolation.ModerateIsolation, HeatingPower.ModeratePower): HeaterOutput.ModerateOutput,
        (Temperature.Hot, Isolation.ModerateIsolation, HeatingPower.HighPower): HeaterOutput.HighOutput,
        (Temperature.Hot, Isolation.HighIsolation, HeatingPower.LowPower): HeaterOutput.LowOutput,
        (Temperature.Hot, Isolation.HighIsolation, HeatingPower.ModeratePower): HeaterOutput.ModerateOutput,
        (Temperature.Hot, Isolation.HighIsolation, HeatingPower.HighPower): HeaterOutput.HighOutput,
        
        # ... Ajoutez d'autres règles selon votre besoin
    })

    # Interface utilisateur pour les valeurs d'entrée
    st.sidebar.header("Entrées")
    ambient_temp = st.sidebar.slider("Température ambiante", min_value=0, max_value=30, value=0)
    insulation_level = st.sidebar.slider("Niveau d'isolation", min_value=0, max_value=10, value=0)
    heating_power = st.sidebar.slider("Puissance de chauffage", min_value=0, max_value=100, value=0)

    # Calcul des valeurs de sortie en utilisant la logique floue
    temp_output = list(Temperature(ambient_temp).values())
    temp_output=[float(x) for x in temp_output]

    insulation_output = list(Isolation(insulation_level).values())
    insulation_output=[float(x) for x in insulation_output]

    power_output = list(HeatingPower(heating_power).values())
    power_output=[float(x) for x in power_output]

    rc_LowOutput=max(
        min(temp_output[0],insulation_output[0],power_output[0]),
        min(temp_output[0],insulation_output[1],power_output[0]),
        min(temp_output[0],insulation_output[2],power_output[0]),
        min(temp_output[1],insulation_output[0],power_output[0]),
        min(temp_output[1],insulation_output[1],power_output[0]),
        min(temp_output[1],insulation_output[2],power_output[0]),
        min(temp_output[2],insulation_output[0],power_output[0]),
        min(temp_output[2],insulation_output[1],power_output[0]),
        min(temp_output[2],insulation_output[2],power_output[0]),
    )
    rc_ModerateOutput=max(
        min(temp_output[0],insulation_output[0],power_output[1]),
        min(temp_output[0],insulation_output[1],power_output[1]),
        min(temp_output[0],insulation_output[2],power_output[1]),
        min(temp_output[1],insulation_output[0],power_output[1]),
        min(temp_output[1],insulation_output[1],power_output[1]),
        min(temp_output[1],insulation_output[2],power_output[1]),
        min(temp_output[2],insulation_output[0],power_output[1]),
        min(temp_output[2],insulation_output[1],power_output[1]),
        min(temp_output[2],insulation_output[2],power_output[1]),
    )
    rc_HighOutput=max(
        min(temp_output[0],insulation_output[0],power_output[2]),
        min(temp_output[0],insulation_output[1],power_output[2]),
        min(temp_output[0],insulation_output[2],power_output[2]),
        min(temp_output[1],insulation_output[0],power_output[2]),
        min(temp_output[1],insulation_output[1],power_output[2]),
        min(temp_output[1],insulation_output[2],power_output[2]),
        min(temp_output[2],insulation_output[0],power_output[2]),
        min(temp_output[2],insulation_output[1],power_output[2]),
        min(temp_output[2],insulation_output[2],power_output[2]),
    )
    all_values = [rc_LowOutput, rc_ModerateOutput,  rc_HighOutput]

    st.write(f"LowOutput  {rc_LowOutput}")
    st.write(f"RModerateOutput {rc_ModerateOutput}")
    st.write(f"HighOutput {rc_HighOutput}")



    fig, axis = plt.subplots(figsize=(7, 5))

    x_HeaterOutput = HeaterOutput.range

    HeaterOutput_0 = np.zeros_like(x_HeaterOutput)
    parametres_RC = [HeaterOutput.LowOutput, HeaterOutput.ModerateOutput, HeaterOutput.HighOutput]
    j=0
    colors = ['y', 'b', 'g']
    for each in parametres_RC:
        axis.plot(x_HeaterOutput, each.array(), colors[j], linewidth=1)
        axis.fill_between(x_HeaterOutput, HeaterOutput_0, [min(all_values[j], x) for x in each.array()], facecolor=colors[j], alpha=0.7)
        j+=1
    st.pyplot(fig)


    # Appliquer les règles d'inférence floue
    output_values = rules({
        Temperature: ambient_temp,
        Isolation: insulation_level,
        HeatingPower: heating_power
    })
    st.write(f"Centre de gravite obtenu avec les valeurs Temperature = {ambient_temp}, Isolation = {insulation_level}  et HeatingPower = {heating_power} est egale a : {output_values}")


def main():
    fuzzy_heating_controller()


if __name__ == "__main__":
    main()