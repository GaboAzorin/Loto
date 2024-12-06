import sqlite3
import time
import pyautogui as py
import datetime
import math
import pyperclip as pc
import re
from collections import Counter
from GAP_Utils.Utils import Play_end_mp3, click_button_on_screen, time_elapsed

def add_sorteos_varios(turns: int, DB_NAME):
    a = time.time()
    prepare_screen()
    all_text, list_of_sorteos = get_screen_info()
    if len(list_of_sorteos) == 10:
        py.moveTo(1150, 365)
    else:
        py.moveTo(1150, 418)

    for i2 in range(turns):
        c = time.time()
        for i, sorteo in enumerate(list_of_sorteos):
            if i <= (len(list_of_sorteos) - 1):
                time.sleep(2)
                if check_if_id_is_in_db(sorteo, DB_NAME):
                    agregar_sorteo(get_info_from_sorteo(), DB_NAME)
                py.moveRel(0, 53)
        click_button_on_screen('boton.png')
        time.sleep(2)
        py.scroll(2000)
        prepare_screen()
        all_text, list_of_sorteos = get_screen_info()
        if len(list_of_sorteos) == 10:
            py.moveTo(1150, 365)
        else:
            py.moveTo(1150, 418)
        d = time.time()
        print(f'Tiempo de esta página: {time_elapsed(c, d)}.')

    # Ordenar la base de datos después de la última actualización
    ordenar_tabla_por_sorteo_id(DB_NAME)

    b = time.time()
    print(f'Tiempo total de programa: {time_elapsed(a, b)}.')
    Play_end_mp3()

def agregar_sorteo(sorteo_dict, DB_NAME):
    """
    Inserta datos desde un diccionario en una tabla SQL, creando columnas adicionales si es necesario.
    DB_NAME: Ruta de la base de datos SQLite.
    data_dict: Diccionario con claves (nombres de columnas) y valores a insertar.
    """
    # Conexión a la base de datos
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    # Obtener las columnas de la tabla
    cursor.execute(f"PRAGMA table_info(sorteos)")
    columns_info = cursor.fetchall()
    columns_names = [column[1] for column in columns_info]

    # Verificar qué columnas no existen y agregarlas
    for key in sorteo_dict.keys():
        if key not in columns_names:
            alter_query = f"ALTER TABLE sorteos ADD COLUMN {key}"
            cursor.execute(alter_query)
            columns_names.append(key)  # Actualizar la lista de columnas

    # Preparar las claves y los valores para la sentencia SQL
    keys = ", ".join(columns_names)
    values = [sorteo_dict.get(col, None) for col in columns_names]
    placeholders = ", ".join(["?" for _ in columns_names])

    # Insertar datos
    insert_query = f"INSERT INTO sorteos ({keys}) VALUES ({placeholders})"
    cursor.execute(insert_query, values)

    # Actualizar índices para cada sufijo
    sufijos = ['loto', 'RECARGADO', 'REVANCHA', 'DESQUITE']
    for sufijo in sufijos:
        columnas = [f'n{i}_{sufijo}' for i in range(1, 7)]
        cursor.execute(f"SELECT {', '.join(columnas)} FROM sorteos WHERE sorteo_id = ?", (sorteo_dict['sorteo_id'],))
        numeros = cursor.fetchone()
        
        # Verificar si todos los valores son nulos
        if all(n is None for n in numeros):
            valor_insertar = None
        else:
            # Calcular el índice
            if None in numeros:
                valor_insertar = None
            else:
                valor_insertar = get_combination_index(numeros)
        
        cursor.execute(f"UPDATE sorteos SET {sufijo}_posicion_en_4_5 = ? WHERE sorteo_id = ?", (valor_insertar, sorteo_dict['sorteo_id']))

    # Guardar cambios y cerrar conexión
    conn.commit()
    conn.close()

def calcular_dia_siguiente():
    """
    Calcula el siguiente día de la semana
    en el que será un sorteo.
    """
    # Definir días de sorteo y hora de sorteo
    hora_sorteo = datetime.time(21, 0)

    # Obtener el día y hora actual
    ahora = datetime.datetime.now()
    dia_actual = ahora.strftime('%A').lower()  # esto devuelve el día de la semana en inglés
    hora_actual = ahora.time()

    # Diccionario para traducir los días al español
    traductor_dias = {
        'monday': 'lunes',
        'tuesday': 'martes',
        'wednesday': 'miércoles',
        'thursday': 'jueves',
        'friday': 'viernes',
        'saturday': 'sábado',
        'sunday': 'domingo'
    }

    dia_actual_espanol = traductor_dias[dia_actual]

    if dia_actual_espanol == "lunes":
        return "martes"
    elif dia_actual_espanol == "martes":
        if hora_actual < hora_sorteo:
            return "martes"
        else:
            return "jueves"
    elif dia_actual_espanol == "miércoles":
        return "jueves"
    elif dia_actual_espanol == "jueves":
        if hora_actual < hora_sorteo:
            return "jueves"
        else:
            return "domingo"
    elif dia_actual_espanol == "viernes":
        return "domingo"
    elif dia_actual_espanol == "sábado":
        return "domingo"
    elif dia_actual_espanol == "domingo":
        if hora_actual < hora_sorteo:
            return "domingo"
        else:
            return "martes"

def calcular_dia_siguiente_numerico():
    # Definir días de sorteo
    dias_sorteo = ['martes', 'jueves', 'domingo']

    # Hora del sorteo
    hora_sorteo = datetime.time(21, 0)

    # Obtener el día y hora actual
    ahora = datetime.datetime.now()
    dia_actual = ahora.strftime('%A').lower()  # esto devuelve el día de la semana en inglés
    hora_actual = ahora.time()

    # Diccionario para traducir los días al español
    traductor_dias = {
        'monday': 'lunes',
        'tuesday': 'martes',
        'wednesday': 'miércoles',
        'thursday': 'jueves',
        'friday': 'viernes',
        'saturday': 'sábado',
        'sunday': 'domingo'
    }

    dia_actual_espanol = traductor_dias[dia_actual]

    # Si hoy es día de sorteo y aún no ha llegado la hora del sorteo
    if dia_actual_espanol in dias_sorteo and hora_actual < hora_sorteo:
        return ahora.day  # Retorna el día actual en número

    # Si no, calculamos el siguiente día de sorteo
    un_dia = datetime.timedelta(days=1)  # Intervalo de un día
    siguiente_fecha = ahora + un_dia

    # Iteramos hasta encontrar el siguiente día de sorteo
    while traductor_dias[siguiente_fecha.strftime('%A').lower()] not in dias_sorteo:
        siguiente_fecha += un_dia

    return siguiente_fecha.day

def calcular_sorteos_faltantes(primer_sorteo, primer_numero_sorteo, DB_NAME):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    
    fecha_actual = datetime.datetime.now()
    diferencia = fecha_actual - primer_sorteo
    semanas = diferencia.days // 7
    total_sorteos = semanas * 3 + (diferencia.days % 7 >= 2) + (diferencia.days % 7 == 6 and fecha_actual.hour >= 21)

    cursor.execute('SELECT MAX(sorteo_id) FROM sorteos')
    ultimo_sorteo = cursor.fetchone()[0]
    sorteos_faltantes = total_sorteos - (ultimo_sorteo - primer_numero_sorteo + 1)

    conn.close()
    return total_sorteos + primer_numero_sorteo + 1, sorteos_faltantes

def compare_predictions(last_result:list, predicted_result:list):
    """
    Compara dos listas de resultados de lotería y calcula un porcentaje de proximidad.
    
    Parámetros:
        last_result (list): Lista de 6 números reales de la lotería.
        predicted_result (list): Lista de 6 números predichos.
    
    Retorna:
        float: Porcentaje de proximidad entre ambas listas.
        str: Explicación detallada del cálculo.
    """
    # Validar las entradas
    if len(last_result) != 6 or len(predicted_result) != 6:
        return None, "Ambas listas deben tener exactamente 6 elementos."
    if any(x < 1 or x > 41 for x in last_result + predicted_result):
        return None, "Los valores de ambas listas deben estar en el rango 1-41."

    # Coincidencias exactas (sin importar posición)
    coincidences = len(set(last_result) & set(predicted_result))
    coincidences_score = (coincidences / 6) * 100  # 100% si hay 6 coincidencias exactas

    # Distancia promedio entre pares (A con A, B con B, etc.)
    distances = [abs(last_result[i] - predicted_result[i]) for i in range(6)]
    avg_distance = sum(distances) / len(distances)
    penalty = (1 - avg_distance / 40) * 10  # Normalizar a 10%

    # Puntaje total
    final_score = min(100, coincidences_score + penalty)  # Máximo 100%

    # Generar explicación
    explanation = (
        f"Coincidencias exactas: {coincidences} de 6, aportando un {coincidences_score:.2f}%.\n"
        f"Distancia promedio entre pares: {avg_distance:.2f}, con una penalización ajustada de {penalty:.2f}%.\n"
        f"Porcentaje final de proximidad: {final_score:.2f}%."
    )

    return final_score, explanation

def cluster_mas_comun(db_path, day=None, week_day=None, month=None, year=None):
    # Conectarse a la base de datos
    conexion = sqlite3.connect(db_path)
    cursor = conexion.cursor()

    # Construir la consulta SQL con filtros opcionales
    query = "SELECT n1_loto, n2_loto, n3_loto, n4_loto, n5_loto, n6_loto FROM sorteos WHERE 1=1"
    params = []

    if day is not None:
        query += " AND day = ?"
        params.append(day)
    if week_day is not None:
        query += " AND week_day = ?"
        params.append(week_day.capitalize())  # Suponiendo que los días están capitalizados en la BD
    if month is not None:
        query += " AND month = ?"
        params.append(month)
    if year is not None:
        query += " AND year = ?"
        params.append(year)

    cursor.execute(query, params)
    sorteos = cursor.fetchall()

    # Calcular el índice de combinación y determinar el cluster
    total_combinaciones = 4496388  # Aproximadamente 4.5 millones
    num_clusters = 50
    tamano_cluster = total_combinaciones // num_clusters
    contadores = Counter()

    for sorteo in sorteos:
        # Calcular el índice de combinación
        if None in sorteo:
            continue
        indice = get_combination_index(sorteo)
        
        # Determinar el cluster correspondiente
        cluster = (indice - 1) // tamano_cluster + 1
        contadores[cluster] += 1

    # Encontrar el cluster más común
    cluster_mas_frecuente = contadores.most_common(1)[0] if contadores else None

    conexion.close()
    return cluster_mas_frecuente

def mostrar_mensaje_bienvenida(primer_sorteo, primer_numero_sorteo, DB_NAME):
    fecha_actual = datetime.datetime.now()
    proximo_sorteo, faltantes = calcular_sorteos_faltantes(primer_sorteo, primer_numero_sorteo, DB_NAME)
    
    mensaje = f"Bienvenido. Hoy es {fecha_actual.strftime('%d/%m/%Y')}, y son las {fecha_actual.strftime('%H:%M')}. "
    if fecha_actual.weekday() in [1, 3, 6] and fecha_actual.hour < 21:
        mensaje += f"Hoy a las 21:00 se lanzará el sorteo número {proximo_sorteo}. "
    else:
        mensaje += f"El próximo sorteo será el número {proximo_sorteo}. "
    mensaje += f"A tu base de datos le faltan {faltantes+1} sorteos."
    print('------ ----- ---- --- -- -    - -- --- ---- ----- ------\n')

    print(mensaje)
    print()

def check_if_id_is_in_db(id_a_verificar, DB_NAME):
    try:
        # Conecta a la base de datos SQLite
        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()

        # Consulta SQL para verificar el ID en la base de datos
        consulta_sql = "SELECT sorteo_id FROM sorteos WHERE sorteo_id = ?"

        # Ejecuta la consulta SQL con el ID como parámetro
        cursor.execute(consulta_sql, (id_a_verificar,))
        resultado = cursor.fetchone()

        # Cierra la conexión a la base de datos
        conn.close()

        if resultado:
            # El ID está en la base de datos, realiza la acción correspondiente
            print(f'El sorteo {id_a_verificar} sí está.')
            return False
        else:
            # El ID no está en la base de datos, realiza otra acción específica
            return True
    except Exception as e:
        # Manejo de errores en caso de problemas con la base de datos
        print(f"Error: {str(e)}")

def crear_db(DB_NAME):
    """Crea la base de datos y la tabla de sorteos si no existen."""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS sorteos (
        sorteo_id INTEGER PRIMARY KEY,
        day INTEGER,
        month INTEGER,
        year INTEGER,
        week_day TEXT,
        n1_loto INTEGER,
        n2_loto INTEGER,
        n3_loto INTEGER,
        n4_loto INTEGER,
        n5_loto INTEGER,
        n6_loto INTEGER,
        comodin INTEGER,
	    n1_RECARGADO INTEGER,
        n2_RECARGADO INTEGER,
        n3_RECARGADO INTEGER,
        n4_RECARGADO INTEGER,
        n5_RECARGADO INTEGER,
        n6_RECARGADO INTEGER,
        n1_REVANCHA INTEGER,
        n2_REVANCHA INTEGER,
        n3_REVANCHA INTEGER,
        n4_REVANCHA INTEGER,
        n5_REVANCHA INTEGER,
        n6_REVANCHA INTEGER,
        n1_DESQUITE INTEGER,
        n2_DESQUITE INTEGER,
        n3_DESQUITE INTEGER,
        n4_DESQUITE INTEGER,
        n5_DESQUITE INTEGER,
        n6_DESQUITE INTEGER
    )
    ''')
    
    conn.commit()
    conn.close()

def crear_dict_sorteo(data_list, other_list):
    # Iniciar el diccionario vacío
    sorteo = {}
    """try:
        other_list = other_list[:other_list.index('JUBILAZO')-1]
    except:
        other_list = other_list[:other_list.index('JUBILAZO 1000000')]"""

    # Extracción de la información
    sorteo['sorteo_id'] = data_list[0]
    sorteo['day'] = data_list[1]
    sorteo['month'] = data_list[2]
    sorteo['year'] = data_list[3]
    sorteo['week_day'] = data_list[4]
    def prepare_6_nums(pre_list):
        final_list = pre_list.split(' ')
        return final_list
    for i, num in enumerate(prepare_6_nums(data_list[5])):
        sorteo[f'n{i+1}_loto'] = num

    sorteo['comodin'] = data_list[7]

    for i, rest_of_data in enumerate(data_list[8:]):

        if rest_of_data.isalpha() or rest_of_data == 'JUBILAZO 50 AÑOS':
            if rest_of_data == 'JUBILAZO 50 AÑOS':
                clave_base == 'JUBILAZO_50_AÑOS'
            else:
                clave_base = rest_of_data
            sufijo = 1
        elif rest_of_data.isalpha() or rest_of_data == 'AHORA SI QUE SI':
            if rest_of_data == 'AHORA SI QUE SI':
                clave_base == 'AHORA_SI_QUE_SI'
            else:
                clave_base = rest_of_data
            sufijo = 1
        # Si el elemento es numérico
        else:
            numeros = rest_of_data.split(' ')
            for idx, num in enumerate(numeros, 1):
                if sufijo == 1:
                        sorteo[f"n{idx}_{clave_base}"] = int(num)
                else:
                        sorteo[f"n{idx}_{clave_base}_{sufijo}"] = int(num)
            sufijo += 1
        if sorteo == "MULTIPLICAR":
            break
    for i in range(0, len(other_list), 3):
        if isinstance(other_list[i], str):
            clave_base = other_list[i].replace(" ", "_")
            clave_base = clave_base.replace('+', 'y')
            sorteo[f"mpw_{clave_base}"] = other_list[i+1]
            sorteo[f"aow_{clave_base}"] = other_list[i+2]

    # Creación de los más comunes

    return sorteo

def extract_date_sublist(element):
    meses = ['enero', 'febrero', 'marzo', 'abril', 'mayo', 'junio', 'julio', 'agosto', 'septiembre', 'octubre', 'noviembre', 'diciembre']
    fecha_info = re.search(r'(\w+), (\d+) de (\w+) de (\d+)', element)
    mes = meses.index(fecha_info.group(3)) + 1
    return [int(fecha_info.group(2)), mes, int(fecha_info.group(4)), fecha_info.group(1)]

def get_combination_index(nums):
    nums = sorted(nums)  # Aseguramos que los números están ordenados
    indice = 0
    
    def combinaciones(n, r):
        return math.comb(n, r)

    for i, num in enumerate(nums):
        for prev_num in range(nums[i - 1] + 1 if i != 0 else 1, num):
            indice += combinaciones(41 - prev_num, 6 - i - 1)
            
    return indice + 1  # +1 para que comience desde 1 en vez de 0

def get_info_from_sorteo():
    py.click()
    time.sleep(1.5)
    py.hotkey('ctrl', 'a')
    py.hotkey('ctrl', 'c')
    time.sleep(1)
    py.click()
    all_text = str(pc.paste())
    sorteo_content_list = all_text[all_text.find('Resultados del sorteo')+len('Resultados del sorteo'):all_text.find('Siguiente página')]
    sorteo_content_list = sorteo_content_list.replace('\r', '')
    sorteo_content_list = sorteo_content_list.replace('\t', '')
    sorteo_content_list = sorteo_content_list.replace('$', '')
    sorteo_content_list = sorteo_content_list.replace('.', '')
    sorteo_content_list = sorteo_content_list.replace('Sorteo # ', '')
    sorteo_content_list = sorteo_content_list.split('\n')
    sorteo_content_list.pop(-1)
    try:
        index_primer_loto = sorteo_content_list.index('LOTO')
        del sorteo_content_list[index_primer_loto:]
    except:
        pass
    for i, element in enumerate(sorteo_content_list):
        if 'Números ganadoresComodin' in element:
            sorteo_content_list[i] = 'Comodin'
        elif 'Números ganadores' in element:
            sorteo_content_list.remove(element)
    # Eliminar varios elementos de la lista que no se ocuparán
    sorteo_content_list.pop(0)
    comodin = sorteo_content_list.pop(2)
    sorteo_content_list.insert(3, comodin)
    date_elements = extract_date_sublist(sorteo_content_list[1])
    del sorteo_content_list[1]
    sorteo_content_list[1:1] = date_elements
    # Ahora se separa todo en dos listas
    results = sorteo_content_list[:sorteo_content_list.index('DivisiónMontoGanadores')]
    winners_and_amounts = sorteo_content_list[sorteo_content_list.index('DivisiónMontoGanadores')+1:]
    dict_final = crear_dict_sorteo(results, winners_and_amounts)
    return dict_final

def ordenar_tabla_por_sorteo_id(DB_NAME):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    # Crear una tabla temporal ordenada por sorteo_id
    cursor.execute('''
        CREATE TABLE sorteos_ordenados AS
        SELECT * FROM sorteos
        ORDER BY sorteo_id ASC
    ''')

    # Eliminar la tabla original
    cursor.execute('DROP TABLE sorteos')

    # Renombrar la tabla ordenada a la original
    cursor.execute('ALTER TABLE sorteos_ordenados RENAME TO sorteos')

    conn.commit()
    conn.close()

def prepare_screen():
    py.moveTo(1380, 540)
    py.click()
    py.scroll(-500)

def get_screen_info():
    py.hotkey('ctrl', 'a')
    py.hotkey('ctrl', 'c')

    all_text = str(pc.paste())
    text_in_the_middle = all_text[all_text.find('Números Ganadores')+len('Números Ganadores'):all_text.find('Siguiente página')]
    text_in_the_middle = text_in_the_middle.replace('\r', '')
    text_in_the_middle = text_in_the_middle.split('\n')

    #Determinar si la pantalla que se ve es la más actual o no (para hacer clic o no en el primer resultado)
    list_of_sorteos_in_screen = []
    if 'Resultados no disponible' in text_in_the_middle:
        text_in_the_middle.pop(-1)
        text_in_the_middle.pop(0)
        text_in_the_middle.pop(0)
        text_in_the_middle.pop(0)
        text_in_the_middle.pop(0)
        text_in_the_middle.pop(0)
    else:
        text_in_the_middle.pop(-1)
        text_in_the_middle.pop(0)

    for element in text_in_the_middle:
        if 'LOTO' in element:
            text_in_the_middle.remove(element)

    for element in text_in_the_middle:
        if element.isdigit():
            list_of_sorteos_in_screen.append(element)
    return text_in_the_middle, list_of_sorteos_in_screen