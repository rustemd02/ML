import random
import pandas as pd

def read_csv(filename):
    data = pd.read_csv(filename, delimiter=';')
    return data

if __name__ == '__main__':
    diseases = read_csv('disease.csv')
    symptoms = read_csv('symptom.csv')
    disease_map = {}

    diseases_names = diseases['disease']
    for dis in diseases_names:
        disease_map[dis] = diseases[(diseases['disease'] == dis)]

    symptoms_names = symptoms['symptom']

    patient_symptoms = {}
    for i in symptoms_names:
        patient_symptoms[i] = random.randint(0,1)
    for i in patient_symptoms:
        if patient_symptoms[i] == 1:
            print(i)


