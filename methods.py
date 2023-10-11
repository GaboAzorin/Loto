import sqlite3
import time
import pyautogui as py
import datetime
import pyperclip as pc
from GAP_Utils.Utils import time_elapsed

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

def get_info_from_sorteo():
    py.click()
    py.hotkey('ctrl', 'a')
    py.hotkey('ctrl', 'c')
    time.sleep(0.5)
    py.click()
    all_text = str(pc.paste())
    text_in_the_middle = all_text[all_text.find('Resultados del sorteo')+len('Resultados del sorteo'):all_text.find('Jubilazo')]
    text_in_the_middle = text_in_the_middle.replace('\r', '')
    text_in_the_middle = text_in_the_middle.split('\n')
    print(text_in_the_middle)

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
