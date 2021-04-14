import pandas as pd
import numpy as np

def topsis(df, weights):
    names = df.iloc[:, 0].values
    matrix = df.iloc[:, 1:].values

    #NORMALISASI
    normalised_matrix = []
    for row in matrix.T:
        div = np.sqrt(sum([a**2 for a in row]))
        normalised_matrix.append([a/div for a in row])
    normalised_matrix = np.array(normalised_matrix).T
    normalised_matrix

    #PEMBOBOTAN
    weighted_matrix = normalised_matrix*weights
    weighted_matrix

    #MENCARI SOLUSI IDEAL POSITIF & NEGATIF
    benefit = [False, True, False, True, False]
    positive_ideal = []
    negative_ideal = []
    for i in range(len(benefit)):
        if benefit[i]:
            positive_ideal.append(max(weighted_matrix.T[i]))
            negative_ideal.append(min(weighted_matrix.T[i]))
        else :
            positive_ideal.append(min(weighted_matrix.T[i]))
            negative_ideal.append(max(weighted_matrix.T[i]))
    positive_ideal = np.array(positive_ideal)
    negative_ideal = np.array(negative_ideal)

    #MENGHITUNG JARAK DENGAN IDEAL
    positive_distance = np.sqrt(((weighted_matrix-positive_ideal)**2).sum(axis=1))
    negative_distance = np.sqrt(((weighted_matrix-negative_ideal)**2).sum(axis=1))
    
    #MENGHITUNG NILAI PREFERENSI
    v = [a/(a+b) for a,b in zip(negative_distance, positive_distance)]

    result = pd.DataFrame({
        "Nama Daerah":names, 
        "Nilai V":v,
        }).sort_values(by=["Nilai V"], ascending=False)
    result["Rank"] = [i for i in range(1, len(names)+1)]

    return result
