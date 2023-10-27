import sqlite3
from methods import get_combination_index

def agregar_columna(db_path, tabla, nombre_columna, tipo_dato="INTEGER"):
    # Conectarse a la base de datos
    conexion = sqlite3.connect(db_path)
    cursor = conexion.cursor()

    # Agregar nueva columna a la tabla
    cursor.execute(f"ALTER TABLE {tabla} ADD COLUMN {nombre_columna} {tipo_dato}")

    # Confirmar cambios y cerrar conexión
    conexion.commit()
    cursor.close()
    conexion.close()

def agrupar_y_contar(db_path, num_divisiones, columna):
    # Calcula el tamaño de cada bloque de división
    total_valores = 4496388
    tamano_bloque = total_valores // num_divisiones
    
    # Conectarse a la base de datos
    conexion = sqlite3.connect(db_path)
    cursor = conexion.cursor()

    # Obtener la cantidad total de registros en la columna dada
    cursor.execute(f"SELECT COUNT(*) FROM tabla_4_5_millones WHERE {columna} IS NOT NULL")
    total_registros = cursor.fetchone()[0]

    # Iniciar lista para guardar resultados
    resultados = []

    for i in range(num_divisiones):
        inicio = i * tamano_bloque + 1
        fin = (i + 1) * tamano_bloque
        
        # Si es la última división, ajusta el fin al total de valores
        if i == num_divisiones - 1: 
            fin = total_valores
        
        # Contar cuántos elementos están en el rango actual
        cursor.execute(f"SELECT COUNT(*) FROM tabla_4_5_millones WHERE {columna} BETWEEN ? AND ?", (inicio, fin))
        count = cursor.fetchone()[0]
        
        porcentaje_del_total_registros = (count / total_registros) * 100
        resultados.append((
            f"{i+1}: {inicio}-{fin}", 
            count, 
            f"{porcentaje_del_total_registros:.2f}%"
        ))

    # Cerrar conexión
    cursor.close()
    conexion.close()

    # Ordenar resultados por cantidad de registros en orden descendente
    resultados_ordenados = sorted(resultados, key=lambda x: x[1], reverse=True)

    return resultados_ordenados


def crear_table(db_path):

    # Conectarse a la base de datos
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # Asegurarte de que SQLite respete las claves foráneas
    cursor.execute("PRAGMA foreign_keys = ON")
    conn.commit()

    # Crear la tabla jugadas
    cursor.execute('''
    CREATE TABLE tabla_4_5_millones (
        id INTEGER PRIMARY KEY,
        sorteo_id INTEGER,
        normal_ordenada_loto INTEGER,
        FOREIGN KEY(sorteo_id) REFERENCES sorteos(sorteo_id)
    )
    ''')

    conn.commit()
    conn.close()

def guardar_indices_en_db(db_path, sufijo):
    conexion = sqlite3.connect(db_path)
    cursor = conexion.cursor()

    columnas = [f'n{i}_{sufijo}' for i in range(1, 7)]
    
    cursor.execute(f"SELECT sorteo_id, {', '.join(columnas)} FROM sorteos")
    sorteos = cursor.fetchall()

    for sorteo in sorteos:
        sorteo_id = sorteo[0]  # Obtener el ID del sorteo
        numeros = sorteo[1:]   # Obtener los números del sorteo

        if None in numeros:  # Si hay algún valor nulo en el conjunto
            valor_insertar = None
        else:
            valor_insertar = get_combination_index(numeros)
        
        cursor.execute(f"UPDATE tabla_4_5_millones SET normal_ordenada_{sufijo} = ? WHERE sorteo_id = ?", (valor_insertar, sorteo_id))

    conexion.commit()
    cursor.close()
    conexion.close()


def numeros_comunes_por_criterios(db_path, **kwargs):
    """
    Encuentra los números más comunes por un número variable de criterios en dos modalidades.
    
    Args:
        db_path (str): Ruta al archivo de la base de datos.
        **kwargs: Pares de criterio y valor. Ejemplo: day='05', month='01'
        
    Returns:
        tuple: Dos listas de números comunes (por posición y general), dos diccionarios con cantidad de repeticiones, y dos booleanos si alguna de las combinaciones ha salido alguna vez.
    """

    # Conectarnos a la base de datos
    conexion = sqlite3.connect(db_path)
    cursor = conexion.cursor()

    # Generamos la cadena de criterios para la consulta SQL
    criterios_sql = ' AND '.join([f"{criterio} = ?" for criterio in kwargs.keys()])
    valores_criterios = tuple(kwargs.values())

    # Números más repetidos por posición
    numeros_comunes_por_posicion = []
    repeticiones_por_posicion = {}
    columnas_numeros = ['n1_loto', 'n2_loto', 'n3_loto', 'n4_loto', 'n5_loto', 'n6_loto']
    for columna in columnas_numeros:
        cursor.execute(f"""
            SELECT {columna}, COUNT({columna}) as cantidad 
            FROM sorteos 
            WHERE {criterios_sql} 
            GROUP BY {columna} 
            ORDER BY cantidad DESC 
            LIMIT 1;
        """, valores_criterios)
        
        fila = cursor.fetchone()
        if fila:
            numero, cantidad = fila
            numeros_comunes_por_posicion.append(numero)
            repeticiones_por_posicion[numero] = cantidad

    # Números más repetidos en general
    cursor.execute(f"""
        SELECT 
            numero, 
            COUNT(numero) as cantidad 
        FROM (
            SELECT n1_loto as numero FROM sorteos WHERE {criterios_sql}
            UNION ALL
            SELECT n2_loto as numero FROM sorteos WHERE {criterios_sql}
            UNION ALL
            SELECT n3_loto as numero FROM sorteos WHERE {criterios_sql}
            UNION ALL
            SELECT n4_loto as numero FROM sorteos WHERE {criterios_sql}
            UNION ALL
            SELECT n5_loto as numero FROM sorteos WHERE {criterios_sql}
            UNION ALL
            SELECT n6_loto as numero FROM sorteos WHERE {criterios_sql}
        ) 
        GROUP BY 
            numero
        ORDER BY 
            cantidad DESC 
        LIMIT 6;
    """, valores_criterios * 6)

    resultados = cursor.fetchall()
    numeros_comunes_general = [fila[0] for fila in resultados]
    repeticiones_general = {fila[0]: fila[1] for fila in resultados}

    # Verificar si alguna de las combinaciones ha salido alguna vez
    combinacion_por_posicion_existe = False
    combinacion_general_existe = False

    cursor.execute(f"""
        SELECT COUNT(*) 
        FROM sorteos 
        WHERE 
            n1_loto = ? AND n2_loto = ? AND n3_loto = ? AND 
            n4_loto = ? AND n5_loto = ? AND n6_loto = ?;
    """, tuple(numeros_comunes_por_posicion))
    if cursor.fetchone()[0] > 0:
        combinacion_por_posicion_existe = True

    cursor.execute(f"""
        SELECT COUNT(*) 
        FROM sorteos 
        WHERE 
            n1_loto = ? AND n2_loto = ? AND n3_loto = ? AND 
            n4_loto = ? AND n5_loto = ? AND n6_loto = ?;
    """, tuple(numeros_comunes_general))
    if cursor.fetchone()[0] > 0:
        combinacion_general_existe = True

    # Cerramos la conexión
    cursor.close()
    conexion.close()

    return (numeros_comunes_por_posicion, combinacion_por_posicion_existe, repeticiones_por_posicion), (numeros_comunes_general, combinacion_general_existe, repeticiones_general)


