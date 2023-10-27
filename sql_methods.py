import sqlite3

import sqlite3

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


