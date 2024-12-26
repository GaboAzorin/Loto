import streamlit as st
import os
import joblib
import tensorflow as tf
import pandas as pd
import numpy as np
import math

# Importamos la función que calcula la fecha/id
# y también la de get_nums_from_index
from new_app_methods import calcular_sorteo_id_y_fecha, get_nums_from_index, get_next_sorteo_date_chile
from new_app_model_methods import (
    generate_outdated_matrix,
    predict_loto_value,
    build_future_row_for_prediction
)

def main():
    st.title("Predicción Loto")

    st.html('<p>Gabriel, bienvenido al predictor de resultados de loto.</p><p>Como sabes, debes escoger un <strong>día</strong>, <strong>mes</strong> y <strong>año</strong> para predecir el resultado.</p><p>Por defecto, la interfaz te muestra la fecha del <strong>próximo resultado que vendrá</strong>.</p>')

    @st.cache_data
    def load_data():
        df = generate_outdated_matrix()
        return df

    df = load_data()

    # -----------------------------
    # 1) Inputs de la fecha
    # -----------------------------
    st.subheader("Datos del sorteo futuro")

    default_day, default_month, default_year = get_next_sorteo_date_chile()

    future_day = st.number_input("Día", min_value=1, max_value=31, value=default_day)
    future_month = st.number_input("Mes", min_value=1, max_value=12, value=default_month)
    future_year = st.number_input("Año", min_value=2023, max_value=2100, value=default_year)

    # -----------------------------
    # 2) Cálculo del sorteo_id y ajuste de la fecha
    # -----------------------------
    adjusted_day, adjusted_month, adjusted_year, calculated_sorteo_id = \
        calcular_sorteo_id_y_fecha(future_day, future_month, future_year)

    # Si la fecha se ajustó, avisamos al usuario
    if (adjusted_day != future_day) or (adjusted_month != future_month) or (adjusted_year != future_year):
        st.warning(
            f"Tu fecha ({future_day}/{future_month}/{future_year}) "
            f"se ajustó al {adjusted_day}/{adjusted_month}/{adjusted_year} "
            f"por ser el siguiente día de sorteo (martes, jueves o domingo)."
        )

    # Mostrar el sorteo_id calculado como campo no editable
    sorteo_id_str = str(calculated_sorteo_id)
    st.text_input("Sorteo ID calculado", value=sorteo_id_str, disabled=True)

    # -----------------------------
    # 3) Selección de modelo en 'models'
    # -----------------------------
    models_dir = "models"
    if not os.path.exists(models_dir):
        st.error("No se encontró la carpeta 'models'. Asegúrate de tener modelos entrenados.")
        return

    all_files = os.listdir(models_dir)
    model_files = [f for f in all_files if f.endswith(".keras") or f.endswith(".h5")]

    if len(model_files) == 0:
        st.error("No hay modelos disponibles en la carpeta 'models'.")
        return

    selected_model_file = st.selectbox("Modelos disponibles:", model_files)

    # -----------------------------
    # 4) Botón para predecir
    # -----------------------------
    if st.button("Predecir"):
        model_path = os.path.join(models_dir, selected_model_file)
        model = tf.keras.models.load_model(model_path)

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

        all_cols = list(df.columns)
        all_cols.remove('sorteo_id')
        all_cols.remove('loto_posicion_en_4_5')
        features = all_cols

        # Llamamos a predict_loto_value con la fecha/ID AJUSTADOS
        try:
            prediction = predict_loto_value(
                model,
                scaler_X,
                scaler_y,
                df,
                features,
                calculated_sorteo_id,
                adjusted_day,
                adjusted_month,
                adjusted_year
            )

            # Con el valor 'prediction' en crudo, se asume que representa un "índice".
            # Lo redondeamos y llamamos a get_nums_from_index para obtener la combinación.
            rounded_pred = round(prediction)
            try:
                combination = get_nums_from_index(rounded_pred)
            except ValueError as e:
                # Por si 'prediction' está fuera de rango (1..4496388)
                combination = None

            if combination:
                st.success(
                    f"Predicción para el sorteo {calculated_sorteo_id} "
                    f"({adjusted_day}/{adjusted_month}/{adjusted_year}): "
                    f"{rounded_pred}  →  Combinación: {combination}"
                )
            else:
                st.warning(
                    f"Predicción para el sorteo {calculated_sorteo_id} "
                    f"({adjusted_day}/{adjusted_month}/{adjusted_year}): "
                    f"{rounded_pred} (no se pudo convertir a combinación válida)"
                )

        except ValueError as e:
            st.error(f"Error al predecir: {e}")

if __name__ == "__main__":
    main()
