from collections import Counter
from methods import get_combination_index
import sqlite3
import pandas as pd
from openpyxl import load_workbook


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
    cursor.execute(f"SELECT COUNT(*) FROM sorteos WHERE {columna} IS NOT NULL")
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
        cursor.execute(f"SELECT COUNT(*) FROM sorteos WHERE {columna} BETWEEN ? AND ?", (inicio, fin))
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

def cambiar_nombre_columna(db_path, table_name, old_column_name, new_column_name):
    # Conectarse a la base de datos
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # Obtener la lista de columnas de la tabla
    cursor.execute(f"PRAGMA table_info({table_name})")
    columns_info = cursor.fetchall()

    # Crear una lista para la definición de la nueva tabla con la columna renombrada
    columns_definition = []
    for col in columns_info:
        col_def = f"{new_column_name} {col[2]}" if col[1] == old_column_name else f"{col[1]} {col[2]}"
        columns_definition.append(col_def)
    columns_definition_str = ", ".join(columns_definition)

    # Crear una lista para la selección de la tabla antigua con el nombre correcto de las columnas
    columns_selection = [new_column_name if col[1] == old_column_name else col[1] for col in columns_info]
    columns_selection_str = ", ".join(columns_selection)

    # Crear una nueva tabla con la columna renombrada
    cursor.execute(f"ALTER TABLE {table_name} RENAME TO {table_name}_old;")
    cursor.execute(f"CREATE TABLE {table_name} ({columns_definition_str});")

    # Copiar los datos de la tabla antigua a la nueva tabla
    cursor.execute(f"INSERT INTO {table_name} ({columns_selection_str}) SELECT {columns_selection_str} FROM {table_name}_old;")

    # Eliminar la tabla antigua
    cursor.execute(f"DROP TABLE {table_name}_old;")

    # Confirmar los cambios
    conn.commit()

    # Cerrar la conexión
    cursor.close()
    conn.close()

    print(f"La columna '{old_column_name}' ha sido renombrada a '{new_column_name}' en la tabla '{table_name}' con éxito.")

def convertir_db_a_excel(db_path, excel_path):
    # Conectar a la base de datos
    conexion = sqlite3.connect(db_path)
    
    # Leer la tabla "sorteos" en un DataFrame de pandas
    df = pd.read_sql_query("SELECT * FROM sorteos", conexion)
    
    # Cerrar la conexión
    conexion.close()
    
    # Guardar el DataFrame en un archivo Excel
    df.to_excel(excel_path, index=False)
    
    # Cargar el archivo Excel y inmovilizar la primera columna
    workbook = load_workbook(excel_path)
    worksheet = workbook.active
    worksheet.freeze_panes = 'B2'  # Inmovilizar la primera columna (A) y la primera fila (1)
    
    # Guardar el archivo Excel modificado
    workbook.save(excel_path)
    print(f"Base de datos exportada a {excel_path} con la primera columna inmovilizada.")

def crear_table(db_path):

    # Conectarse a la base de datos
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # Asegurarte de que SQLite respete las claves foráneas
    cursor.execute("PRAGMA foreign_keys = ON")
    conn.commit()

    # Crear la tabla jugadas
    cursor.execute('''
    CREATE TABLE posibilidades (
        id INTEGER PRIMARY KEY,
        sorteo_id INTEGER,
        n1_loto INTEGER,
        n2_loto INTEGER,
        n3_loto INTEGER,
        n4_loto INTEGER,
        n5_loto INTEGER,
        n6_loto INTEGER,
        FOREIGN KEY(sorteo_id) REFERENCES sorteos(sorteo_id)
    )
    ''')

    conn.commit()
    conn.close()

def eliminar_columna_en_sqlite(db_path, table_name, column_name):
    # Conectarse a la base de datos
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # Obtener la lista de columnas de la tabla
    cursor.execute(f"PRAGMA table_info({table_name})")
    columns = cursor.fetchall()
    
    # Filtrar el nombre de la columna que queremos eliminar
    columns_to_copy = [col[1] for col in columns if col[1] != column_name]

    # Si la columna a eliminar no está en la tabla, terminar la función
    if column_name not in [col[1] for col in columns]:
        print(f"La columna '{column_name}' no existe en la tabla '{table_name}'.")
        cursor.close()
        conn.close()
        return

    # Crear una nueva lista de columnas para la consulta, excluyendo la columna a eliminar
    columns_str = ", ".join(columns_to_copy)

    # Comenzar la transacción
    cursor.execute("BEGIN TRANSACTION;")

    # Crear una nueva tabla que es una copia de la vieja sin la columna no deseada
    new_table_name = f"{table_name}_new"
    cursor.execute(f"CREATE TABLE {new_table_name} AS SELECT {columns_str} FROM {table_name};")

    # Eliminar la tabla antigua
    cursor.execute(f"DROP TABLE {table_name};")

    # Renombrar la nueva tabla con el nombre de la tabla original
    cursor.execute(f"ALTER TABLE {new_table_name} RENAME TO {table_name};")

    # Hacer commit de la transacción
    conn.commit()

    # Cerrar la conexión
    cursor.close()
    conn.close()

    print(f"La columna '{column_name}' ha sido eliminada de la tabla '{table_name}' con éxito.")

def guardar_indices_en_db(db_path, sufijo):
    conexion = sqlite3.connect(db_path)
    cursor = conexion.cursor()

    # Obtener todos los sorteo_id de la tabla 'sorteos'
    cursor.execute("SELECT sorteo_id FROM sorteos")
    sorteos_ids = cursor.fetchall()
    sorteos_ids = [id[0] for id in sorteos_ids]

    # Obtener todos los sorteo_id de la tabla 'tabla_4_5_millones'
    cursor.execute("SELECT sorteo_id FROM tabla_4_5_millones")
    tabla_ids = cursor.fetchall()
    tabla_ids = [id[0] for id in tabla_ids]

    # Identificar los sorteo_id faltantes en 'tabla_4_5_millones'
    faltantes_ids = list(set(sorteos_ids) - set(tabla_ids))

    # Agregar los sorteos faltantes a 'tabla_4_5_millones'
    for sorteo_id in faltantes_ids:
        cursor.execute("SELECT * FROM sorteos WHERE sorteo_id = ?", (sorteo_id,))
        sorteo = cursor.fetchone()
        numeros = sorteo[5:11]  # Suponiendo que los números del sorteo están en las columnas 5 a 10
        
        # Insertar el sorteo en 'tabla_4_5_millones'
        cursor.execute("INSERT INTO tabla_4_5_millones (sorteo_id) VALUES (?)", (sorteo_id,))
        
        # Calcular el índice y actualizar la columna correspondiente
        if None in numeros:
            valor_insertar = None
        else:
            valor_insertar = get_combination_index(numeros)
        
        cursor.execute(f"UPDATE tabla_4_5_millones SET normal_ordenada_{sufijo} = ? WHERE sorteo_id = ?", (valor_insertar, sorteo_id))
    
    # Obtener y mostrar los primeros registros de la tabla 'tabla_4_5_millones' después de la actualización
    cursor.execute(f"SELECT * FROM tabla_4_5_millones LIMIT 10")
    registros_actualizados = cursor.fetchall()
    columnas_tabla = [description[0] for description in cursor.description]
    
    cursor.close()
    conexion.close()
    
    # Mostrar los registros actualizados en un dataframe
    df_registros_actualizados = pd.DataFrame(registros_actualizados, columns=columnas_tabla)
    print(df_registros_actualizados)

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

def numeros_frecuentes_por_sorteo(db_path, tipo_sorteo):
    # Conectarse a la base de datos
    conexion = sqlite3.connect(db_path)
    cursor = conexion.cursor()

    # Crear una lista de nombres de columnas basándose en el tipo de sorteo
    columnas = [f'n{i}_{tipo_sorteo}' for i in range(1, 7)]
    contadores = [Counter() for _ in columnas]

    # Consultar la tabla 'sorteos'
    query = f"SELECT sorteo_id, {', '.join(columnas)} FROM sorteos"
    cursor.execute(query)
    sorteos = cursor.fetchall()

    # Iniciar la transacción
    conexion.execute('BEGIN TRANSACTION')

    # Definir la cadena de actualización de columnas para los números más comunes
    cols_actualizar_mas_comun = ", ".join(
        [f'n{i}_{tipo_sorteo}_mas_comun = ?' for i in range(1, 7)]
    )

    for index, sorteo in enumerate(sorteos):
        sorteo_id = sorteo[0]
        numeros_sorteo = sorteo[1:]

        mas_frecuentes = []
        for i, num in enumerate(numeros_sorteo):
            contadores[i].update([num])
            mas_frecuente = contadores[i].most_common(1)[0][0]
            mas_frecuentes.append(mas_frecuente)

        if index == 0:
            diferencias = [0] * 6
        else:
            diferencias = [numeros_sorteo[i] - mas_frecuentes[i] for i in range(6)]

        # Preparar la consulta de actualización con los valores de dispersión y los más comunes
        cols_actualizar_dispersion = ", ".join(
            [f'n{i}_{tipo_sorteo}_mas_comun_dispersion = ?' for i in range(1, 7)]
        )
        query_update = f"UPDATE sorteos SET {cols_actualizar_dispersion}, {cols_actualizar_mas_comun} WHERE sorteo_id = ?"

        # Ejecutar la consulta de actualización
        cursor.execute(query_update, (*diferencias, *mas_frecuentes, sorteo_id))

    # Confirmar la transacción y cerrar la conexión
    conexion.commit()
    cursor.close()
    conexion.close()

    print("Datos guardados correctamente en la base de datos.")

