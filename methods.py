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
    """Agrega un sorteo a la base de datos."""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    
    # Verificar si el sorteo ya existe
    cursor.execute('SELECT * FROM sorteos WHERE sorteo_id=?', (sorteo_dict['sorteo_id'],))
    if cursor.fetchone():
        print(f"El sorteo {sorteo_dict['sorteo_id']} ya existe.")
        return False
    
    # Agregar el sorteo
    campos = ['sorteo_id', 'day', 'month', 'year', 'week_day', 'n1_loto', 'n2_loto', 'n3_loto', 'n4_loto', 'n5_loto', 'n6_loto',
              'comodin', 'money_per_winner_loto', 'amount_of_winners_loto', 'money_per_winner_super_quina', 'amount_of_winners_super_quina',
              'money_per_winner_quina', 'amount_of_winners_quina', 'money_per_winner_super_cuaterna', 'amount_of_winners_super_cuaterna',
              'money_per_winner_cuaterna', 'amount_of_winners_cuaterna', 'money_per_winner_super_terna', 'amount_of_winners_super_terna',
              'money_per_winner_terna', 'amount_of_winners_terna', 'money_per_winner_super_dupla', 'amount_of_winners_super_dupla',
              'n1_recargado', 'n2_recargado', 'n3_recargado', 'n4_recargado', 'n5_recargado', 'n6_recargado', 'money_per_winner_recargado',
              'amount_of_winners_recargado', 'n1_revancha', 'n2_revancha', 'n3_revancha', 'n4_revancha', 'n5_revancha', 'n6_revancha',
              'money_per_winner_revancha', 'amount_of_winners_revancha', 'n1_desquite', 'n2_desquite', 'n3_desquite', 'n4_desquite',
              'n5_desquite', 'n6_desquite', 'money_per_winner_desquite', 'amount_of_winners_desquite']
    valores = [sorteo_dict[campo] for campo in campos]
    
    consulta = f"INSERT INTO sorteos ({', '.join(campos)}) VALUES ({', '.join(['?']*len(campos))})"
    
    try:
        cursor.execute(consulta, valores)
        conn.commit()
    except sqlite3.Error as e:
        print(f"Error al agregar sorteo: {e}")
        return False
    finally:
        conn.close()

    return True

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
        money_per_winner_loto INTEGER,
        amount_of_winners_loto INTEGER,
	    money_per_winner_super_quina INTEGER,
	    amount_of_winners_super_quina INTEGER,
	    money_per_winner_quina INTEGER,
	    amount_of_winners_quina INTEGER,
	    money_per_winner_super_cuaterna INTEGER,
	    amount_of_winners_super_cuaterna INTEGER,
	    money_per_winner_cuaterna INTEGER,
	    amount_of_winners_cuaterna INTEGER,
	    money_per_winner_super_terna INTEGER,
	    amount_of_winners_super_terna INTEGER,
	    money_per_winner_terna INTEGER,
	    amount_of_winners_terna INTEGER,
	    money_per_winner_super_dupla INTEGER,
	    amount_of_winners_super_dupla INTEGER,
	    n1_recargado INTEGER,
        n2_recargado INTEGER,
        n3_recargado INTEGER,
        n4_recargado INTEGER,
        n5_recargado INTEGER,
        n6_recargado INTEGER,
    	money_per_winner_recargado INTEGER,
	    amount_of_winners_recargado INTEGER,
        n1_revancha INTEGER,
        n2_revancha INTEGER,
        n3_revancha INTEGER,
        n4_revancha INTEGER,
        n5_revancha INTEGER,
        n6_revancha INTEGER,
    	money_per_winner_revancha INTEGER,
	    amount_of_winners_revancha INTEGER,
        n1_desquite INTEGER,
        n2_desquite INTEGER,
        n3_desquite INTEGER,
        n4_desquite INTEGER,
        n5_desquite INTEGER,
        n6_desquite INTEGER,
    	money_per_winner_desquite INTEGER,
	    amount_of_winners_desquite INTEGER
    )
    ''')
    
    conn.commit()
    conn.close()

def crear_dict_sorteo(data_list):
    # Iniciar el diccionario vacío
    sorteo = {}

    # Extracción de la información
    sorteo['sorteo_id'] = data_list[0]
    sorteo['day'] = data_list[1][0]
    sorteo['month'] = data_list[1][1]
    sorteo['year'] = data_list[1][2]
    sorteo['week_day'] = data_list[1][3]

    for i, num in enumerate(data_list[2]):
        sorteo[f'n{i+1}_loto'] = num

    sorteo['comodin'] = data_list[3]

    def extract_numbers(game_name, start_index):
        for i, num in enumerate(data_list[start_index]):
            sorteo[f'n{i+1}_{game_name}'] = num

    extract_numbers('recargado', 5)
    extract_numbers('revancha', 7)
    extract_numbers('desquite', 9)

    # Extracción de información de premios
    prizes = {
        'LOTO 6 aciertos': ['money_per_winner_loto', 'amount_of_winners_loto'],
        'Súper Quina 5 aciertos + comodín': ['money_per_winner_super_quina', 'amount_of_winners_super_quina'],
        'Quina 5 aciertos': ['money_per_winner_quina', 'amount_of_winners_quina'],
        'Súper Cuaterna 4 aciertos + comodín': ['money_per_winner_super_cuaterna', 'amount_of_winners_super_cuaterna'],
        'Cuaterna 4 aciertos': ['money_per_winner_cuaterna', 'amount_of_winners_cuaterna'],
        'Súper Terna 3 aciertos + comodín': ['money_per_winner_super_terna', 'amount_of_winners_super_terna'],
        'Terna 3 aciertos': ['money_per_winner_terna', 'amount_of_winners_terna'],
        'Súper Dupla 2 aciertos + comodín': ['money_per_winner_super_dupla', 'amount_of_winners_super_dupla'],
        'RECARGADO 6 aciertos': ['money_per_winner_recargado', 'amount_of_winners_recargado'],
        'REVANCHA': ['money_per_winner_revancha', 'amount_of_winners_revancha'],
        'DESQUITE': ['money_per_winner_desquite', 'amount_of_winners_desquite'],
    }

    for idx, item in enumerate(data_list):
        if not isinstance(item, list):
            if item in prizes:
                sorteo[prizes[item][0]] = data_list[idx + 1]
                sorteo[prizes[item][1]] = data_list[idx + 2]

    return sorteo

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
    for element in sorteo_content_list:
        if 'Números ganadores' in element:
            sorteo_content_list.remove(element)
    # Eliminar varios elementos de la lista que no se ocuparán
    sorteo_content_list.pop(0)
    # Eliminamos todos los elementos desde el segundo elemento después de 'DESQUITE' hasta el final de la lista
    index_primero_desquite = sorteo_content_list.index('DESQUITE')
    index_segundo_desquite = sorteo_content_list.index('DESQUITE', index_primero_desquite + 1)
    del sorteo_content_list[index_segundo_desquite + 3:]

    inicio = sorteo_content_list.index('JUBILAZO')
    fin = sorteo_content_list.index('DivisiónMontoGanadores')
    del sorteo_content_list[inicio:fin]

    def is_number_sequence(s):
        parts = s.split()
        return len(parts) > 1 and all(x.isdigit() for x in parts)

    # Recorrer la lista y hacer las transformaciones requeridas
    nueva_lista = []
    for item in sorteo_content_list:
        if is_number_sequence(item):
            nueva_lista.append(list(map(int, item.split())))
        elif item.isdigit():
            nueva_lista.append(int(item))
        else:
            nueva_lista.append(item)

    sorteo_content_list = list(nueva_lista)
    sorteo_content_list[1] = extract_date_sublist(sorteo_content_list[1])

    sorteo_content_dict = crear_dict_sorteo(sorteo_content_list)

    return sorteo_content_dict

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