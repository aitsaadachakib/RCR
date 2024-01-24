import streamlit as st
import pycosat

class Sigma:
    def __init__(self, path_file):
        self.lower = 0
        self.upper = 0
        self.weights = []
        self.formulas = []
        self.strates_weights = []
        self.length = 0
        self.read_file(path_file)

    def read_file(self, path_file):
        with open(path_file) as file:
            for line in file:
                information = line.split()
                size = len(information)
                self.weights.append(float(information[0]))
                self.formulas.append([int(information[i]) for i in range(1, size)])
        self.length = len(self.weights)

    def get_length(self):
        return self.length

    def get_weights(self):
        return self.weights

    def get_formulas(self):
        return self.formulas

    def sort_weights(self):
        for i in range(len(self.weights) - 1, 0, -1):
            for j in range(i):
                if self.weights[j] < self.weights[j + 1]:
                    self.weights[j], self.weights[j + 1] = self.weights[j + 1], self.weights[j]
                    self.formulas[j], self.formulas[j + 1] = self.formulas[j + 1], self.formulas[j]

    def compute_strates(self):
        no_doubles = set(self.weights)
        self.upper = len(no_doubles)
        self.strates_weights = sorted(no_doubles)

    def get_strates_number(self):
        return self.upper

    def get_strates_weights(self):
        return self.strates_weights

    def get_preprocessed_formulas(self, sub_formulas):
        dict_cor = {}
        returned_formulas = []
        cpt = 1
        i = 0
        for form in sub_formulas:
            j = 0
            returned_formulas.insert(i, [])
            for pred in form:
                if pred not in dict_cor.keys():
                    if pred > 0:
                        dict_cor[pred] = cpt
                        dict_cor[-pred] = -cpt
                        cpt += 1
                    else:
                        dict_cor[-pred] = cpt
                        dict_cor[pred] = -cpt
                        cpt += 1
                returned_formulas[i].insert(j, dict_cor[pred])
                j += 1
            i += 1
        return returned_formulas

# Function to run the Sigma solver
def run_sigma_solver( evidence):
    base_de_connaissance = Sigma("file.txt")
    base_de_connaissance.sort_weights()
    base_de_connaissance.compute_strates()

    iteration = 1
    while base_de_connaissance.lower < base_de_connaissance.upper:
        r = int((base_de_connaissance.lower + base_de_connaissance.upper + 1) / 2)

        liste = base_de_connaissance.get_weights()
        value_of_r = -1
        for i in range(len(liste)):
            if base_de_connaissance.get_strates_weights()[r - 1] > liste[i]:
                value_of_r = i
                break
        if value_of_r == -1:
            value_of_r = len(liste) - 1

        for j in range(len(liste)):
            if base_de_connaissance.get_strates_weights()[base_de_connaissance.upper - 1] == liste[j]:
                valueU = j
                break
        cnf = base_de_connaissance.formulas[valueU:value_of_r]

        for i in range(len(evidence)):
            liste = []
            liste.append(-1 * evidence[i])
            cnf.append(liste)
        cnf = base_de_connaissance.get_preprocessed_formulas(cnf)

        result = pycosat.solve(cnf)
        if type(result) == type([]):
            base_de_connaissance.upper = r - 1
        else:
            base_de_connaissance.lower = r

        iteration = iteration + 1

    Val = base_de_connaissance.get_strates_weights()[r - 1]
    return Val

# Streamlit app
def main():
    st.title("Sigma Solver App")

    # File upload and evidence input
    
    
    evidence_input = st.text_input("Enter evidence (comma-separated integers)", "1,-2,-3")
    evidence = [int(x) for x in evidence_input.split(',')]

        # Run the solver when the user clicks the button
    if st.button("Run Solver"):
        result = run_sigma_solver( evidence)

        # Display the result
        st.success(f"Result: Val({evidence}, Sigma) = {result}")

if __name__ == "__main__":
    main()
