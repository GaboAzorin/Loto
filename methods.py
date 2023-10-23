import sqlite3
import time
import pyautogui as py
import datetime
import pyperclip as pc
import re
from GAP_Utils.Utils import Play_end_mp3, click_button_on_screen, time_elapsed

def add_sorteos_varios(turns: int, DB_NAME):
    a = time.time()
    prepare_screen()
    all_text, list_of_sorteos = get_screen_info()
    if len(list_of_sorteos) == 10:
        py.moveTo(990, 365)
    else:
        py.moveTo(990, 418)

    for i2 in range(turns):
        c = time.time()
        for i, sorteo in enumerate(list_of_sorteos):
            if i <= (len(list_of_sorteos)-1):
                time.sleep(2)
                if check_if_id_is_in_db(sorteo, DB_NAME):
                    agregar_sorteo(get_info_from_sorteo(), DB_NAME)
                    #print(get_info_from_sorteo())
                py.moveRel(0,53)
        click_button_on_screen('boton.png')
        time.sleep(2)
        py.scroll(2000)
        prepare_screen()
        all_text, list_of_sorteos = get_screen_info()
        if len(list_of_sorteos) == 10:
            py.moveTo(990, 365)
        else:
            py.moveTo(990, 418)
        d = time.time()
        print(f'Tiempo de esta página: {time_elapsed(c, d)}.')

    b = time.time()
    print(f'Tiempo total de programa: {time_elapsed(a, b)}.')
    Play_end_mp3()

def agregar_sorteo(sorteo_dict, DB_NAME):
    """
    Inserta datos desde un diccionario en una tabla SQL, creando columnas adicionales si es necesario.

    DB_NAME: Ruta de la base de datos SQLite.
    table_name: Nombre de la tabla donde insertar los datos.
    data_dict: Diccionario con claves (nombres de columnas) y valores a insertar.
    """
    # Conexión a la base de datos
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    # Obtener las columnas de la tabla
    cursor.execute(f"PRAGMA table_info({'sorteos'})")
    columns_info = cursor.fetchall()
    columns_names = [column[1] for column in columns_info]

    # Verificar qué columnas no existen y agregarlas
    for key in sorteo_dict.keys():
        if key not in columns_names:
            alter_query = f"ALTER TABLE {'sorteos'} ADD COLUMN {key}"
            cursor.execute(alter_query)
            columns_names.append(key)  # Actualizar la lista de columnas

    # Preparar las claves y los valores para la sentencia SQL
    keys = ", ".join(columns_names)
    values = [sorteo_dict.get(col, None) for col in columns_names]
    placeholders = ", ".join(["?" for _ in columns_names])

    # Insertar datos
    insert_query = f"INSERT INTO {'sorteos'} ({keys}) VALUES ({placeholders})"
    cursor.execute(insert_query, values)

    # Guardar cambios y cerrar conexión
    conn.commit()
    conn.close()

def calcular_dia_siguiente():
    # Definir días de sorteo y hora de sorteo
    dias_sorteo = ['martes', 'jueves', 'domingo']
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
        return dia_actual_espanol

    # Si no, buscamos el siguiente día de sorteo
    idx_actual = dias_sorteo.index(dia_actual_espanol) if dia_actual_espanol in dias_sorteo else -1
    for i in range(1, len(dias_sorteo) + 1):
        siguiente_idx = (idx_actual + i) % len(dias_sorteo)
        if dias_sorteo[siguiente_idx] != dia_actual_espanol:
            return dias_sorteo[siguiente_idx]

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
    return total_sorteos + primer_numero_sorteo, sorteos_faltantes

def mostrar_mensaje_bienvenida(primer_sorteo, primer_numero_sorteo, DB_NAME):
    fecha_actual = datetime.datetime.now()
    proximo_sorteo, faltantes = calcular_sorteos_faltantes(primer_sorteo, primer_numero_sorteo, DB_NAME)
    
    mensaje = f"Bienvenido. Hoy es {fecha_actual.strftime('%d/%m/%Y')}, y son las {fecha_actual.strftime('%H:%M')}. "
    if fecha_actual.weekday() in [1, 3, 6] and fecha_actual.hour < 21:
        mensaje += f"Hoy a las 21:00 se lanzará el sorteo número {proximo_sorteo}. "
    else:
        mensaje += f"El próximo sorteo será el número {proximo_sorteo}. "
    mensaje += f"A tu base de datos le faltan {faltantes} sorteos."
    print('------ ----- ---- --- -- -    - -- --- ---- ----- ------\n')
    
    print(mensaje)

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
            print(f'El sorteo {id_a_verificar} ya está.')
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
        mpw_loto INTEGER,
        aow_loto INTEGER,
	    mpw_super_quina INTEGER,
	    aow_super_quina INTEGER,
	    mpw_quina INTEGER,
	    aow_quina INTEGER,
	    mpw_super_cuaterna INTEGER,
	    aow_super_cuaterna INTEGER,
	    mpw_cuaterna INTEGER,
	    aow_cuaterna INTEGER,
	    mpw_super_terna INTEGER,
	    aow_super_terna INTEGER,
	    mpw_terna INTEGER,
	    aow_terna INTEGER,
	    mpw_super_dupla INTEGER,
	    aow_super_dupla INTEGER,
	    n1_RECARGADO INTEGER,
        n2_RECARGADO INTEGER,
        n3_RECARGADO INTEGER,
        n4_RECARGADO INTEGER,
        n5_RECARGADO INTEGER,
        n6_RECARGADO INTEGER,
    	mpw_RECARGADO INTEGER,
	    aow_RECARGADO INTEGER,
        n1_REVANCHA INTEGER,
        n2_REVANCHA INTEGER,
        n3_REVANCHA INTEGER,
        n4_REVANCHA INTEGER,
        n5_REVANCHA INTEGER,
        n6_REVANCHA INTEGER,
    	mpw_REVANCHA INTEGER,
	    aow_REVANCHA INTEGER,
        n1_DESQUITE INTEGER,
        n2_DESQUITE INTEGER,
        n3_DESQUITE INTEGER,
        n4_DESQUITE INTEGER,
        n5_DESQUITE INTEGER,
        n6_DESQUITE INTEGER,
    	mpw_DESQUITE INTEGER,
	    aow_DESQUITE INTEGER
    )
    ''')
    
    conn.commit()
    conn.close()

def crear_dict_sorteo(data_list, other_list):
    diccionario = {}
    clave_base = None
    sufijo = 1

    for elemento in data_list:
        # Si el elemento es alfabético
        if elemento.isalpha():
            clave_base = elemento
            sufijo = 1
        # Si el elemento es numérico
        else:
            numeros = elemento.split(' ')
            for idx, num in enumerate(numeros, 1):
                if sufijo == 1:
                    diccionario[f"n{idx}_{clave_base}"] = int(num)
                else:
                    diccionario[f"n{idx}_{clave_base}_{sufijo}"] = int(num)
            sufijo += 1
        if elemento == "MULTIPLICAR":
            break
    #2da parte
    clave_base = None

    for i in range(0, len(other_list), 3):
        if isinstance(other_list[i], str):
            clave_base = other_list[i].replace(" ", "_")
            diccionario[f"mpw_{clave_base}"] = lista[i+1]
            diccionario[f"aow_{clave_base}"] = lista[i+2]

    return diccionario

def extract_date_sublist(element):
    meses = ['enero', 'febrero', 'marzo', 'abril', 'mayo', 'junio', 'julio', 'agosto', 'septiembre', 'octubre', 'noviembre', 'diciembre']
    fecha_info = re.search(r'(\w+), (\d+) de (\w+) de (\d+)', element)
    mes = meses.index(fecha_info.group(3)) + 1
    return [int(fecha_info.group(2)), mes, int(fecha_info.group(4)), fecha_info.group(1)]

def get_info_from_sorteo():
    py.click()
    time.sleep(1)
    py.hotkey('ctrl', 'a')
    py.hotkey('ctrl', 'c')
    time.sleep(0.5)
    py.click()
    all_text = str(pc.paste())
    sorteo_content_list = all_text[all_text.find('Resultados del sorteo')+len('Resultados del sorteo'):all_text.find('Siguiente página')]
    sorteo_content_list = sorteo_content_list.replace('\r', '')
    sorteo_content_list = sorteo_content_list.replace('\t', '')
    sorteo_content_list = sorteo_content_list.replace('$', '')
    sorteo_content_list = sorteo_content_list.replace('.', '')
    sorteo_content_list = sorteo_content_list.replace('Sorteo # ', '')
    sorteo_content_list = sorteo_content_list.split('\n')
    index_primer_loto = sorteo_content_list.index('LOTO')
    del sorteo_content_list[index_primer_loto:]
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
    exit()

def prepare_screen():
    py.moveTo(990, 540)
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