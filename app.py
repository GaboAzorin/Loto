import streamlit as st
from new_app_methods import *

#ChatGPT que me está ayudando:
#https://chatgpt.com/c/6758e7f1-bbbc-8003-863e-5c80182ae5b5

# Cambio de título de página
st.set_page_config(
   page_title="Predictor Gabo",
   layout="wide",
   initial_sidebar_state="expanded",
)

# Página original
st.header("Predictor")

day, month, year, week_day, month_str, hour = get_full_date()

welcome, dayToCheck, monthToCheck = welcome_phrase(day, month, year, week_day, month_str, hour)

st.write(welcome)

st.write(get_sorteo(dayToCheck, monthToCheck, 2024))

# Página nueva

import os
import joblib
import tensorflow as tf
import pandas as pd
import numpy as np

# Importa tus funciones desde tu script principal
# Ajusta el nombre de tu archivo si no se llama "new_app_model_methods"
from new_app_model_methods import (
    generate_outdated_matrix,
    predict_loto_value,
    build_future_row_for_prediction
)

def main():
    st.title("Predicción Loto")

    # 1) Cargar la matriz virtual (df) solo una vez.
    #    Puedes hacer un cache si quieres, para que no se cargue cada vez que refrescas la app.
    @st.cache_data
    def load_data():
        df = generate_outdated_matrix()
        return df

    df = load_data()

    # 2) Mostrar inputs para day, month, year, sorteo_id
    st.subheader("Datos del sorteo futuro")
    future_sorteo_id = st.number_input("Sorteo ID", min_value=1, value=5208, step=1)
    future_day = st.number_input("Día", min_value=1, max_value=31, value=24)
    future_month = st.number_input("Mes", min_value=1, max_value=12, value=12)
    future_year = st.number_input("Año", min_value=2023, max_value=2100, value=2024)

    # 3) Listar modelos disponibles en carpeta "models"
    st.subheader("Seleccionar modelo")
    models_dir = "models"
    if not os.path.exists(models_dir):
        st.error("No se encontró la carpeta 'models'. Asegúrate de tener modelos entrenados.")
        return

    # Filtramos archivos que sean .keras (o .h5) para listar
    all_files = os.listdir(models_dir)
    model_files = [f for f in all_files if f.endswith(".keras") or f.endswith(".h5")]

    if len(model_files) == 0:
        st.error("No hay modelos disponibles en la carpeta 'models'.")
        return

    # Selectbox para escoger un modelo
    selected_model_file = st.selectbox("Modelos disponibles:", model_files)

    # 4) Botón para predecir
    if st.button("Predecir"):
        # 4.1) Cargamos el modelo seleccionado
        model_path = os.path.join(models_dir, selected_model_file)
        model = tf.keras.models.load_model(model_path)

        # 4.2) Inferimos el nombre base de escalers
        #     Por convención, asumimos que si el modelo es:
        #     model-arch128_64_32-epochs40-test0.2-batch32.keras
        #     entonces los escalers se llaman:
        #     scalerX-arch128_64_32-epochs40-test0.2-batch32.pkl
        #     scalerY-arch128_64_32-epochs40-test0.2-batch32.pkl
        #     Quitamos la extensión y reemplazamos "model" con "scalerX" y "scalerY".
        base_name = selected_model_file.replace(".keras", "").replace(".h5", "")
        scalerX_name = "scalerX" + base_name[len("model"):] + ".pkl"
        scalerY_name = "scalerY" + base_name[len("model"):] + ".pkl"

        scalerX_path = os.path.join(models_dir, scalerX_name)
        scalerY_path = os.path.join(models_dir, scalerY_name)

        if not (os.path.exists(scalerX_path) and os.path.exists(scalerY_path)):
            st.error("No se encontraron los scalerX o scalerY correspondientes al modelo seleccionado.")
            return

        scaler_X = joblib.load(scalerX_path)
        scaler_y = joblib.load(scalerY_path)

        # 4.3) Usar la misma lista de 'features' con la que se entrenó
        #     Aquí, la forma más sencilla es: asumimos que "features" = todas las col. (except sorteo_id, loto_posicion_en_4_5)
        #     Sin embargo, en la app final, deberías almacenar la lista 'features' en un .pkl o similar.
        #     Por simplicidad, aquí la generamos de la misma manera que en 'train_loto_model'.
        #     Es decir, con "df" que ya tenemos cargado.
        all_cols = list(df.columns)
        all_cols.remove('sorteo_id')
        all_cols.remove('loto_posicion_en_4_5')
        features = all_cols

        # 4.4) Construir fila ficticia con la info del sorteo anterior
        #     Nota: 'predict_loto_value' ya lo hace internamente, pero si prefieres llamarlo directamente:
        try:
            prediction = predict_loto_value(
                model,
                scaler_X,
                scaler_y,
                df,
                features,
                future_sorteo_id,
                future_day,
                future_month,
                future_year
            )
            st.success(f"Predicción para el sorteo {future_sorteo_id}: {round(prediction):,.2f}, que equivale los números: {get_nums_from_index(round(prediction))}")
        except ValueError as e:
            st.error(f"Error al predecir: {e}")

if __name__ == "__main__":
    main()
