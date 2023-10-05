import datetime
import sqlite3

# Configuración de la base de datos
DB_NAME = 'loteria.db'

def crear_db():
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
	'Nº 1 Recargado': 2,
	'Nº 2 Recargado': 17,
	'Nº 3 Recargado': 18,
	'Nº 4 Recargado': 28,
	'Nº 5 Recargado': 31,
	'Nº 6 Recargado': 41,
	'Monto por ganador Recargado': 0,
	'Número de ganadores Recargado': 0,
	'Nº 1 Revancha': 1,
	'Nº 2 Revancha': 8,
	'Nº 3 Revancha': 9,
	'Nº 4 Revancha': 27,
	'Nº 5 Revancha': 30,
	'Nº 6 Revancha': 38,
	'Monto por ganador Revancha': 0,
	'Número de ganadores Revancha': 0,
	'Nº 1 Desquite': 2,
	'Nº 2 Desquite': 17,
	'Nº 3 Desquite': 18,
	'Nº 4 Desquite': 28,
	'Nº 5 Desquite': 31,
	'Nº 6 Desquite': 41,
	'Monto por ganador Desquite': 0,
	'Número de ganadores Desquite': 0,
    )
    ''')
    
    conn.commit()
    conn.close()

def agregar_sorteo(sorteo_dict):
    """Agrega un sorteo a la base de datos."""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    
    sorteo_id = sorteo_dict['Sorteo']
    day = sorteo_dict['día']
    month = sorteo_dict['month']
    year = sorteo_dict['año']

    # Verificar si el sorteo ya existe
    cursor.execute('SELECT * FROM sorteos WHERE sorteo_id=?', (sorteo_id,))
    if cursor.fetchone():
        print(f"El sorteo {sorteo_id} ya existe.")
        return False
    
    # Agregar el sorteo
    cursor.execute('INSERT INTO sorteos (sorteo_id, day, month, year) VALUES (?, ?, ?, ?)', 
                   (sorteo_id, day, month, year))
    
    conn.commit()
    conn.close()
    return True

def calcular_sorteos_faltantes(primer_sorteo, primer_numero_sorteo):
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

def mostrar_mensaje_bienvenida(primer_sorteo, primer_numero_sorteo):
    fecha_actual = datetime.datetime.now()
    proximo_sorteo, faltantes = calcular_sorteos_faltantes(primer_sorteo, primer_numero_sorteo)
    
    mensaje = f"Bienvenido. Hoy es {fecha_actual.strftime('%d/%m/%Y')}, y son las {fecha_actual.strftime('%H:%M')}. "
    if fecha_actual.weekday() in [1, 3, 6] and fecha_actual.hour < 21:
        mensaje += f"Hoy a las 21:00 se lanzará el sorteo número {proximo_sorteo}. "
    else:
        mensaje += f"El próximo sorteo será el número {proximo_sorteo}. "
    mensaje += f"A tu base de datos le faltan {faltantes} sorteos."
    
    print(mensaje)

# Ejemplo de uso:

# Crear la base de datos (solo es necesario hacer esto una vez)
crear_db()

# Fecha del primer sorteo y su número
primer_sorteo = datetime.datetime(2016, 1, 3, 21, 0)  
primer_numero_sorteo = 3803

# Mostrar mensaje
mostrar_mensaje_bienvenida(primer_sorteo, primer_numero_sorteo)
