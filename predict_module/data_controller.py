import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.neural_network import MLPRegressor
import joblib
import json


data = pd.read_csv("predict_module/clean_data.csv")
reg24 = joblib.load('predict_module/tumor_size_predictor24.joblib')
# Загружаем информацию о признаках
with open('predict_module/model_features24.json', 'r') as f:
    feature_info = json.load(f)

print("Загруженные признаки:", feature_info['feature_columns'])


def __get_corr_histories(hr, her2, mp, menopausal_status):
  return data[data["hr"] == hr][data["her2"] == her2][data["mp"] == mp][data["menopausal_status"] == menopausal_status]


def get_chances(hr, her2, mp, menopausal_status):
    cor_histories = __get_corr_histories(hr, her2, mp, menopausal_status)
    pcr_1 = cor_histories[cor_histories["pcr"] == 1]["arm"].value_counts()
    pcr_0 = cor_histories[cor_histories["pcr"] == 0]["arm"].value_counts()
    res = {}
    for k in pcr_1.to_dict().keys():
        v = pcr_1.to_dict()[k]
        try:
            res[k] = v / (v + pcr_0.to_dict()[k])
        except:
            res[k] = 1
    return res


def prepare_new_data(new_data, feature_columns):
    """
    new_data: DataFrame с исходными данными
    feature_columns: список ожидаемых признаков
    """
    # Создаем dummy переменные (как при обучении)
    prepared_data = pd.get_dummies(new_data, columns=["menopausal_status", "arm"])    
    # Убеждаемся, что все нужные колонки присутствуют
    for col in feature_columns:
        if col not in prepared_data.columns:
            prepared_data[col] = 0
    # Упорядочиваем колонки как при обучении
    prepared_data = prepared_data[feature_columns]
    
    return prepared_data


def predict_24month(arm, hr, her2, mp, menopausal_status, age, tumor_size_week_0, tumor_size_week_4, tumor_size_week_12):
    new_patient_data = pd.DataFrame({
        'arm': ['paclitaxel_' + arm],
        'hr': [hr],
        'her2': [her2],
        'mp': [mp],
        'menopausal_status': [menopausal_status],
        'age': [age],
        'tumor_size_week_0': [tumor_size_week_0],
        'tumor_size_week_4': [tumor_size_week_4],
        'tumor_size_week_12': [tumor_size_week_12]
    })

    # Подготавливаем данные
    X_new = prepare_new_data(new_patient_data, feature_info['feature_columns'])
    print(X_new)

    prediction = reg24.predict(X_new)

    return prediction[0]
