"""
Script de ejemplo que:
1) Aplica mapeos a columnas con texto para dejarlas como valores numéricos.
2) Genera una matriz 'outdated' (desplazando información del sorteo anterior).
3) Entrena un modelo con TODAS las columnas (excepto 'sorteo_id' y 'loto_posicion_en_4_5'). 
4) Permite predecir a partir de un sorteo_id futuro (usando la info del sorteo anterior).
"""

from GAP_Utils.Utils import Play_end_mp3
import sqlite3
import os
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import MinMaxScaler
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Dropout, Input
from tensorflow.keras.callbacks import EarlyStopping, ReduceLROnPlateau
import joblib  # Para guardar el scaler

# -----------------------------------------------------------------------------------
# 1) Mapeo de columnas con texto a valores numéricos
# -----------------------------------------------------------------------------------
def mapear_columnas(df):
    """
    Aplica mapeos a varias columnas del DataFrame para convertir textos en valores numéricos.
    Si alguna columna no existe en df, se ignora.
    Si un valor no está en el mapeo, se pone como 0 (o NaN y luego se llena con 0).
    """
    mapping_dict = {
        # Mapeo de 'week_day': domingo, martes, jueves
        'week_day': {
            'domingo': 7,
            'martes': 2,
            'jueves': 4
        },
        # Ejemplo de mapeos para columnas "JUBILAZO"
        # Ajusta o añade según tus necesidades reales:
        'mpw_JUBILAZO_1000000': {
            'JUBILAZO': 1,
            '0': 0
        },
        'mpw_JUBILAZO_500000': {
            'JUBILAZO': 1,
            '0': 0,
            '1': 1  # si aparece como texto
        },
        'mpw_JUBILAZO_50_AÑOS_1000000': {
            'JUBILAZO 50 AÑOS': 1,
            '0': 0
        },
        'mpw_JUBILAZO_50_AÑOS_500000': {
            'JUBILAZO 50 AÑOS': 1,
            '0': 0,
            '1': 1
        },
        # etc. Agrega más columnas si es necesario...
    }

    for col, map_dict in mapping_dict.items():
        if col in df.columns:
            df[col] = df[col].map(map_dict)  # Convertimos texto -> número
            df[col] = df[col].fillna(0)      # Si algún valor no está en el diccionario, queda NaN; lo rellenamos con 0

    return df


# -----------------------------------------------------------------------------------
# 2) Generar la matriz "outdated" desplazando los datos del sorteo anterior
# -----------------------------------------------------------------------------------
def generate_outdated_matrix():
    """
    Toma la base de datos loto.db y genera una matriz virtual con los datos cruzados con resultados anteriores:
        - Toma un número de sorteo (ejemplo: 5202) con su fecha correcta (10 de diciembre de 2024) 
          y le asigna todos los valores del resultado anterior (del 5201).
    Devuelve la base en db, para su posterior uso (en entrenamiento de modelos).
    """
    db_path = 'loto.db'
    conn = sqlite3.connect(db_path)
    query = "SELECT * FROM sorteos;"
    df = pd.read_sql_query(query, conn)
    conn.close()

    # 2.1) Mapear columnas texto -> numéricas
    df = mapear_columnas(df)

    # 2.2) Función interna para desplazar columnas
    def generar_tabla_virtual(df_inner):
        columnas_originales = ['sorteo_id', 'day', 'month', 'year', 'loto_posicion_en_4_5']
        columnas_modificadas = [col for col in df_inner.columns if col not in columnas_originales]
        
        df_virtual = df_inner[columnas_originales].copy()
        shifted_columns = {col: df_inner[col].shift(1) for col in columnas_modificadas}
        
        df_virtual = pd.concat([df_virtual, pd.DataFrame(shifted_columns)], axis=1)
        # Quitamos la primera fila (no tiene sorteo anterior)
        df_virtual = df_virtual.iloc[1:].reset_index(drop=True)
        return df_virtual

    df_virtual = generar_tabla_virtual(df)
    return df_virtual


# -----------------------------------------------------------------------------------
# 3) Construir y describir el modelo (para nombrar archivos)
# -----------------------------------------------------------------------------------
def build_model(input_dim):
    """
    Crea un modelo Keras con varias capas y retorna (modelo, lista_de_capas).
    """
    layers = [
        Input(shape=(input_dim,)),
        Dense(1024, activation='relu'),
        Dropout(0.3),
        Dense(512, activation='relu'),
        Dropout(0.3),
        Dense(256, activation='relu'),
        Dropout(0.3),
        Dense(128, activation='relu'),
        Dropout(0.3),
        Dense(64, activation='relu'),
        Dropout(0.3),
        Dense(32, activation='relu'),
        Dense(1, activation='linear')
    ]
    model = Sequential(layers)
    return model, layers

def get_architecture_name(layers_list):
    """
    Toma la lista de capas y arma un string describiendo los 'units' de las capas Dense.
    """
    arch_parts = []
    from tensorflow.keras.layers import Dense, Dropout
    for layer in layers_list:
        if isinstance(layer, Dense):
            arch_parts.append(str(layer.units))
        # Podrías agregar info de Dropout, etc.
    return "_".join(arch_parts)


# -----------------------------------------------------------------------------------
# 4) Entrenar el modelo con TODAS las columnas (excepto 'sorteo_id' y 'loto_posicion_en_4_5')
# -----------------------------------------------------------------------------------
def train_loto_model(data, epochs=50, test_size=0.2, batch_size=32):
    """
    Entrena un modelo de red neuronal para predecir 'loto_posicion_en_4_5'
    usando TODAS las columnas numéricas, excepto 'sorteo_id' y 'loto_posicion_en_4_5'.
    Guarda el modelo y los escalers. Retorna (model, scaler_X, scaler_y, history, features).
    """

    # 4.1) Separar features y target
    all_cols = list(data.columns)
    all_cols.remove('sorteo_id')
    all_cols.remove('loto_posicion_en_4_5')
    features = all_cols
    target = 'loto_posicion_en_4_5'

    X = data[features]
    y = data[target].values.reshape(-1, 1)

    # 4.2) Escalado
    scaler_X = MinMaxScaler()
    X_scaled = scaler_X.fit_transform(X)

    scaler_y = MinMaxScaler()
    y_scaled = scaler_y.fit_transform(y)

    # 4.3) Train-test split
    X_train, X_test, y_train, y_test = train_test_split(
        X_scaled, y_scaled, test_size=test_size, random_state=42
    )

    # 4.4) Crear modelo y compilar
    model, layers_list = build_model(input_dim=X_train.shape[1])
    architecture_name = get_architecture_name(layers_list)
    model.compile(optimizer='adam', loss='mse', metrics=['mae'])

    # 4.5) Callbacks
    early_stop = EarlyStopping(monitor='val_loss', patience=10, restore_best_weights=True)
    reduce_lr = ReduceLROnPlateau(monitor='val_loss', factor=0.5, patience=5, min_lr=1e-6, verbose=1)

    # 4.6) Entrenar
    history = model.fit(
        X_train, y_train,
        validation_split=0.2,
        epochs=epochs,
        batch_size=batch_size,
        verbose=1,
        callbacks=[early_stop, reduce_lr]
    )

    # 4.7) Evaluar
    loss, mae = model.evaluate(X_test, y_test, verbose=0)
    print(f"Mean Squared Error en test: {loss:,.4f}")
    print(f"Mean Absolute Error en test: {mae:,.4f}")

    # 4.8) Guardar modelo y escalers
    current_dir = os.path.dirname(os.path.abspath(__file__))
    models_folder = os.path.join(current_dir, 'models')
    if not os.path.exists(models_folder):
        os.makedirs(models_folder)

    model_filename  = f"model-arch{architecture_name}-epochs{epochs}-test{test_size}-batch{batch_size}.keras"
    scalerX_filename= f"scalerX-arch{architecture_name}-epochs{epochs}-test{test_size}-batch{batch_size}.pkl"
    scalerY_filename= f"scalerY-arch{architecture_name}-epochs{epochs}-test{test_size}-batch{batch_size}.pkl"

    model_path = os.path.join(models_folder, model_filename)
    model.save(model_path)
    print(f"Modelo guardado en: {model_path}")

    scalerX_path = os.path.join(models_folder, scalerX_filename)
    joblib.dump(scaler_X, scalerX_path)
    print(f"Scaler de X guardado en: {scalerX_path}")

    scalerY_path = os.path.join(models_folder, scalerY_filename)
    joblib.dump(scaler_y, scalerY_path)
    print(f"Scaler de y guardado en: {scalerY_path}")

    return model, scaler_X, scaler_y, history, features


# -----------------------------------------------------------------------------------
# 5) Construir la fila ficticia para un sorteo futuro
# -----------------------------------------------------------------------------------
def build_future_row_for_prediction(df, future_sorteo_id, future_day, future_month, future_year):
    """
    Usa la fila del sorteo_id anterior para crear una nueva fila,
    sobreescribiendo sorteo_id, day, month, year con los datos futuros,
    y dejando 'loto_posicion_en_4_5' en NaN.
    """
    prev_id = future_sorteo_id - 1
    df_anterior = df.loc[df['sorteo_id'] == prev_id]
    if df_anterior.empty:
        raise ValueError(f"No se encontró la fila con sorteo_id={prev_id}. Imposible armar datos históricos.")

    row_futura = df_anterior.copy()
    row_futura['sorteo_id'] = future_sorteo_id
    row_futura['day'] = future_day
    row_futura['month'] = future_month
    row_futura['year'] = future_year
    row_futura['loto_posicion_en_4_5'] = np.nan
    return row_futura


# -----------------------------------------------------------------------------------
# 6) Predicción
# -----------------------------------------------------------------------------------
def predict_loto_value(model, scaler_X, scaler_y, df, features, future_sorteo_id, future_day, future_month, future_year):
    """
    1) Construye la fila ficticia (info del sorteo anterior + day/month/year futuros).
    2) Toma solo 'features', escala, predice y aplica inverse_transform a la salida.
    3) Retorna el valor predicho.
    """
    # 1) Fila ficticia con data del sorteo anterior
    future_row = build_future_row_for_prediction(
        df,
        future_sorteo_id,
        future_day,
        future_month,
        future_year
    )
    # 2) Extraer solo features
    future_data = future_row[features].copy()

    # 3) Escalar
    future_data_scaled = scaler_X.transform(future_data)

    # 4) Predicción
    predictions_scaled = model.predict(future_data_scaled)

    # 5) Inverse transform
    predictions = scaler_y.inverse_transform(predictions_scaled)

    return predictions[0][0]


# -----------------------------------------------------------------------------------
# 7) Flujo principal
# -----------------------------------------------------------------------------------
if __name__ == "__main__":
    # 7.1) Generar df (matriz virtual con SHIFT)
    df = generate_outdated_matrix()

    # 7.2) Entrenar con TODAS las columnas (menos sorteo_id y la etiqueta)
    model, scalerX, scalerY, history, features = train_loto_model(
        df,
        epochs=50,
        test_size=0.2,
        batch_size=32
    )

    # 7.3) Ejemplo de predicción para un sorteo futuro
    future_sorteo_id = 5208
    future_day = 24
    future_month = 12
    future_year = 2024

    prediction = predict_loto_value(
        model,
        scalerX,
        scalerY,
        df,
        features,
        future_sorteo_id,
        future_day,
        future_month,
        future_year
    )

    print(f"Predicción para el sorteo {future_sorteo_id} (día={future_day}, mes={future_month}, año={future_year}): {prediction:,.2f}")

    Play_end_mp3()
