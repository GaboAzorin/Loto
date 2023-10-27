import sqlite3

def numeros_comunes_por_criterios(db_path, **kwargs):
    """
    Encuentra los números más comunes por un número variable de criterios.
    
    Args:
        db_path (str): Ruta al archivo de la base de datos.
        **kwargs: Pares de criterio y valor. Ejemplo: day='05', month='01'
        
    Returns:
        tuple: Una lista de números comunes, un diccionario con cantidad de repeticiones, y un booleano si ha salido esa combinación.
    """

    # Conectarnos a la base de datos
    conexion = sqlite3.connect(db_path)
    cursor = conexion.cursor()

    # Lista de columnas de números
    columnas_numeros = ['n1_loto', 'n2_loto', 'n3_loto', 'n4_loto', 'n5_loto', 'n6_loto']

    numeros_comunes = []
    repeticiones = {}  # Diccionario para almacenar las repeticiones

    # Generamos la cadena de criterios para la consulta SQL
    criterios_sql = ' AND '.join([f"{criterio} = ?" for criterio in kwargs.keys()])
    valores_criterios = tuple(kwargs.values())

    # Iteramos sobre cada columna de números
    for columna in columnas_numeros:
        cursor.execute(f"""
            SELECT 
                {columna}, 
                COUNT({columna}) as cantidad 
            FROM 
                sorteos 
            WHERE 
                {criterios_sql}
            GROUP BY 
                {columna} 
            ORDER BY 
                cantidad DESC 
            LIMIT 1;
        """, valores_criterios)

        fila = cursor.fetchone()
        if fila:
            numero, cantidad = fila
            numeros_comunes.append(numero)
            repeticiones[numero] = cantidad
        else:
            numeros_comunes.append(None)

    # Verificar si la combinación ha salido alguna vez
    combinacion_existe = False
    cursor.execute(f"""
        SELECT COUNT(*) 
        FROM sorteos 
        WHERE 
            n1_loto = ? AND n2_loto = ? AND n3_loto = ? AND 
            n4_loto = ? AND n5_loto = ? AND n6_loto = ?;
    """, tuple(numeros_comunes))
    if cursor.fetchone()[0] > 0:
        combinacion_existe = True

    # Cerramos la conexión
    cursor.close()
    conexion.close()

    return numeros_comunes, repeticiones, combinacion_existe

