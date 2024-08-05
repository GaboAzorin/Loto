import sqlite3
from random import sample
from collections import Counter
from itertools import combinations
import math

def obtener_combinaciones_existentes(db_path, juego):
    """
    Obtiene todas las combinaciones de números existentes en la base de datos para un juego específico.

    Args:
    db_path (str): Ruta al archivo de la base de datos SQLite.
    juego (str): Nombre del juego (e.g., "loto", "RECARGADO").

    Returns:
    set: Un conjunto de tuplas que representan las combinaciones existentes.
    """
    conexion = sqlite3.connect(db_path)
    cursor = conexion.cursor()

    columnas = [f"n{i}_{juego}" for i in range(1, 7)]
    query = f"SELECT {', '.join(columnas)} FROM sorteos WHERE {' AND '.join([f'{col} IS NOT NULL' for col in columnas])}"
    cursor.execute(query)
    resultados = cursor.fetchall()

    conexion.close()

    # Convertir resultados en un conjunto de tuplas ordenadas
    combinaciones_existentes = {tuple(sorted(comb)) for comb in resultados if None not in comb}
    return combinaciones_existentes

def generar_combinaciones_nuevas(db_path, juego, num_combinaciones=5):
    """
    Genera una lista de combinaciones de números que nunca se hayan dado antes.

    Args:
    db_path (str): Ruta al archivo de la base de datos SQLite.
    juego (str): Nombre del juego (e.g., "loto", "RECARGADO").
    num_combinaciones (int): Número de combinaciones a generar.

    Returns:
    list: Una lista de combinaciones nuevas.
    """
    combinaciones_existentes = obtener_combinaciones_existentes(db_path, juego)
    nuevas_combinaciones = []

    while len(nuevas_combinaciones) < num_combinaciones:
        combinacion = tuple(sorted(sample(range(1, 42), 6)))  # Generar una combinación aleatoria
        if combinacion not in combinaciones_existentes:
            nuevas_combinaciones.append(combinacion)
            combinaciones_existentes.add(combinacion)  # Agregar para evitar duplicados

    return nuevas_combinaciones

def generar_combinaciones_por_cluster(db_path, juego, num_combinaciones=5, num_clusters=50):
    """
    Genera combinaciones posibles basadas en los clusters más comunes.

    Args:
    db_path (str): Ruta al archivo de la base de datos SQLite.
    juego (str): Nombre del juego (e.g., "loto", "RECARGADO").
    num_combinaciones (int): Número de combinaciones a generar.
    num_clusters (int): Número de clusters para la división.

    Returns:
    list: Una lista de combinaciones nuevas basadas en el cluster más común.
    """
    conexion = sqlite3.connect(db_path)
    cursor = conexion.cursor()

    columnas = [f"n{i}_{juego}" for i in range(1, 7)]
    query = f"SELECT {', '.join(columnas)} FROM sorteos WHERE {' AND '.join([f'{col} IS NOT NULL' for col in columnas])}"
    cursor.execute(query)
    resultados = cursor.fetchall()
    
    # Calcular el índice de combinación y determinar el cluster
    total_combinaciones = 4496388  # Aproximadamente 4.5 millones
    tamano_cluster = total_combinaciones // num_clusters
    contadores = Counter()

    for resultado in resultados:
        if None in resultado:
            continue
        indice = get_combination_index(resultado)
        cluster = (indice - 1) // tamano_cluster + 1
        contadores[cluster] += 1

    # Encontrar el cluster más común
    cluster_mas_frecuente = contadores.most_common(1)[0][0]

    # Generar combinaciones basadas en el cluster más común
    nuevas_combinaciones = []
    combinaciones_existentes = obtener_combinaciones_existentes(db_path, juego)

    while len(nuevas_combinaciones) < num_combinaciones:
        # Generar una combinación aleatoria dentro del rango del cluster
        cluster_inicio = (cluster_mas_frecuente - 1) * tamano_cluster + 1
        cluster_fin = cluster_mas_frecuente * tamano_cluster
        combinacion_indices = sample(range(cluster_inicio, cluster_fin + 1), 1)
        combinacion = tuple(sorted(list(combinations(range(1, 42), 6))[combinacion_indices[0]]))

        if combinacion not in combinaciones_existentes:
            nuevas_combinaciones.append(combinacion)
            combinaciones_existentes.add(combinacion)

    conexion.close()
    return nuevas_combinaciones

# Función auxiliar para obtener el índice de combinación
def get_combination_index(nums):
    nums = sorted(nums)  # Aseguramos que los números están ordenados
    indice = 0
    
    def combinaciones(n, r):
        return math.comb(n, r)

    for i, num in enumerate(nums):
        for prev_num in range(nums[i - 1] + 1 if i != 0 else 1, num):
            indice += combinaciones(41 - prev_num, 6 - i - 1)
            
    return indice + 1  # +1 para que comience desde 1 en vez de 0

import sqlite3
from random import sample
from collections import Counter

def obtener_numeros_comunes_ultimo_ano(db_path, juego):
    """
    Obtiene los números más comunes del último año para un juego específico.

    Args:
    db_path (str): Ruta al archivo de la base de datos SQLite.
    juego (str): Nombre del juego (e.g., "loto").

    Returns:
    list: Lista de los tres números más comunes del último año.
    """
    conexion = sqlite3.connect(db_path)
    cursor = conexion.cursor()

    # Obtener el año actual
    cursor.execute("SELECT MAX(year) FROM sorteos")
    ultimo_ano = cursor.fetchone()[0]

    # Consultar los números sorteados en el último año para el juego específico
    columnas = [f"n{i}_{juego}" for i in range(1, 7)]
    query = f"SELECT {', '.join(columnas)} FROM sorteos WHERE year = ? AND {' AND '.join([f'{col} IS NOT NULL' for col in columnas])}"
    cursor.execute(query, (ultimo_ano,))
    sorteos = cursor.fetchall()
    conexion.close()

    # Contar la frecuencia de cada número
    contador_numeros = Counter()
    for sorteo in sorteos:
        for numero in sorteo:
            contador_numeros[numero] += 1

    # Obtener los tres números más comunes
    numeros_mas_comunes = [num for num, _ in contador_numeros.most_common(3)]
    return numeros_mas_comunes

def generar_combinaciones_con_numeros_comunes(db_path, juego, num_combinaciones=5):
    """
    Genera combinaciones probables utilizando los tres números más comunes del último año, 
    asegurando que nunca se hayan dado antes.

    Args:
    db_path (str): Ruta al archivo de la base de datos SQLite.
    juego (str): Nombre del juego (e.g., "loto").
    num_combinaciones (int): Número de combinaciones a generar.

    Returns:
    list: Una lista de combinaciones nuevas.
    """
    # Obtener los tres números más comunes del último año
    numeros_comunes = obtener_numeros_comunes_ultimo_ano(db_path, juego)

    # Obtener combinaciones existentes para evitar duplicados
    combinaciones_existentes = obtener_combinaciones_existentes(db_path, juego)
    nuevas_combinaciones = []

    while len(nuevas_combinaciones) < num_combinaciones:
        # Generar una combinación utilizando los tres números comunes
        combinacion = set(numeros_comunes)

        # Completar con números aleatorios sin repetir
        while len(combinacion) < 6:
            numero_aleatorio = sample(range(1, 42), 1)[0]
            combinacion.add(numero_aleatorio)

        combinacion = tuple(sorted(combinacion))

        # Verificar que la combinación no haya ocurrido antes
        if combinacion not in combinaciones_existentes:
            nuevas_combinaciones.append(combinacion)
            combinaciones_existentes.add(combinacion)

    return nuevas_combinaciones

