import sqlite3

def numeros_comunes_por_dia_numerico(db_path, dia_especifico: str):
    # Conectarnos a la base de datos
    conexion = sqlite3.connect(db_path)
    cursor = conexion.cursor()
    
    # Lista de columnas de números
    columnas_numeros = ['n1_loto', 'n2_loto', 'n3_loto', 'n4_loto', 'n5_loto', 'n6_loto']
    
    numeros_comunes = []
    
    # Iteramos sobre cada columna de números
    for columna in columnas_numeros:
        cursor.execute(f"""
            SELECT 
                {columna}, 
                COUNT({columna}) as cantidad 
            FROM 
                sorteos 
            WHERE 
                day = ? 
            GROUP BY 
                {columna} 
            ORDER BY 
                cantidad DESC 
            LIMIT 1;
        """, (dia_especifico,))
        
        fila = cursor.fetchone()
        if fila:
            numero, cantidad = fila
            numeros_comunes.append(numero)
        else:
            numeros_comunes.append(None)  # o puedes añadir un valor por defecto como -1 o 0

    # Cerramos la conexión
    cursor.close()
    conexion.close()
    
    return numeros_comunes

def numeros_comunes_por_dia_semana(db_path, dia_especifico: str):
    # Conectarnos a la base de datos
    conexion = sqlite3.connect(db_path)
    cursor = conexion.cursor()
    
    # Lista de columnas de números
    columnas_numeros = ['n1_loto', 'n2_loto', 'n3_loto', 'n4_loto', 'n5_loto', 'n6_loto']
    
    numeros_comunes = []
    
    # Iteramos sobre cada columna de números
    for columna in columnas_numeros:
        cursor.execute(f"""
            SELECT 
                {columna}, 
                COUNT({columna}) as cantidad 
            FROM 
                sorteos 
            WHERE 
                week_day = ? 
            GROUP BY 
                {columna} 
            ORDER BY 
                cantidad DESC 
            LIMIT 1;
        """, (dia_especifico,))
        
        fila = cursor.fetchone()
        if fila:
            numero, cantidad = fila
            numeros_comunes.append(numero)
        else:
            numeros_comunes.append(None)  # o puedes añadir un valor por defecto como -1 o 0

    # Cerramos la conexión
    cursor.close()
    conexion.close()
    
    return numeros_comunes

def resultados_repetidos(db_path):
    # Conectarnos a la base de datos
    conexion = sqlite3.connect(db_path)
    cursor = conexion.cursor()
    
    # Ejecutamos la consulta
    cursor.execute("""
        SELECT 
            n1_loto, n2_loto, n3_loto, n4_loto, n5_loto, n6_loto, 
            COUNT(*) as cantidad_repeticiones 
        FROM 
            sorteos 
        GROUP BY 
            n1_loto, n2_loto, n3_loto, n4_loto, n5_loto, n6_loto 
        HAVING 
            cantidad_repeticiones > 1;
    """)
    
    # Recogemos los resultados
    resultados = cursor.fetchall()

    # Cerramos la conexión
    cursor.close()
    conexion.close()
    
    # Procesamos y mostramos los resultados
    if not resultados:
        return "No se encontraron resultados repetidos."
    
    output = "Se encontraron los siguientes resultados repetidos:\n"
    for fila in resultados:
        numeros = fila[:6]
        repeticiones = fila[6]
        output += f"{numeros} se repitió {repeticiones} veces.\n"
    
    return output

def numeros_comunes_y_repetidos_por_dia(db_path, dia_especifico):
    # Conectarnos a la base de datos
    conexion = sqlite3.connect(db_path)
    cursor = conexion.cursor()
    
    # Lista de columnas de números
    columnas_numeros = ['n1_loto', 'n2_loto', 'n3_loto', 'n4_loto', 'n5_loto', 'n6_loto']
    
    numeros_comunes = []
    
    # Iteramos sobre cada columna de números
    for columna in columnas_numeros:
        cursor.execute(f"""
            SELECT 
                {columna}, 
                COUNT({columna}) as cantidad 
            FROM 
                sorteos 
            WHERE 
                week_day = ? 
            GROUP BY 
                {columna} 
            ORDER BY 
                cantidad DESC 
            LIMIT 1;
        """, (dia_especifico,))
        
        fila = cursor.fetchone()
        if fila:
            numero, cantidad = fila
            numeros_comunes.append(numero)
        else:
            numeros_comunes.append(None)  # o puedes añadir un valor por defecto como -1 o 0

    # Verificar si el conjunto de números ha sido sorteado anteriormente
    cursor.execute(f"""
        SELECT 
            COUNT(*) 
        FROM 
            sorteos 
        WHERE 
            week_day = ? AND 
            n1_loto = ? AND 
            n2_loto = ? AND 
            n3_loto = ? AND 
            n4_loto = ? AND 
            n5_loto = ? AND 
            n6_loto = ?
    """, (dia_especifico, *numeros_comunes))
    
    conteo = cursor.fetchone()[0]
    es_repetido = conteo > 1  # Si aparece más de una vez, entonces es repetido

    # Cerramos la conexión
    cursor.close()
    conexion.close()
    
    return numeros_comunes, es_repetido