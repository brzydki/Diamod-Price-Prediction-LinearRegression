import pickle
import numpy as np
import pandas as pd
from scipy.optimize import minimize


def predict():
    with open('temp.txt', 'r') as file:
        file_path = file.read().strip()


    df = pd.read_csv(file_path)

    with open('diamondmodel.pkl', 'rb') as f:
        loaded_model = pickle.load(f)

    X = df.values
    prediction = loaded_model.predict(X)

    if prediction[0] <= 0:
        return "Ошибка в данных"
    else:
        return prediction[0]


def valuepredict(target_price):
    def cost_function(X_input):
        columns = ['Feature1', 'Feature2', 'Feature3', 'Feature4', 'Feature5', 'Feature6']


        with open('temp.txt', 'r') as file:
            file_path = file.read().strip()


        df_temp = pd.DataFrame([X_input], columns=columns)
        df_temp.to_csv(file_path, index=False)

        prediction = predict()
        if isinstance(prediction, str) and "Ошибка" in prediction:
            return float('inf')

        cost = abs(prediction - target_price)
        return cost


    with open('temp.txt', 'r') as file:
        file_path = file.read().strip()


    df = pd.read_csv(file_path)
    X = df.values.flatten()
    initial_guess = X


    with open('X_data.pkl', 'wb') as f:
        pickle.dump(X.tolist(), f)


    result = minimize(cost_function, initial_guess, method='Nelder-Mead')

    with open('result_x.pkl', 'wb') as f:
        pickle.dump(result.x.tolist(), f)

    return result.x
