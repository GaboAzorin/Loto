import datetime
import sqlite3

# Configuración de la base de datos
DB_NAME = 'loto.db'

def agregar_sorteo(sorteo_dict):
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


# Fecha del primer sorteo y su número
primer_sorteo = datetime.datetime(2016, 1, 3, 21, 0)  
primer_numero_sorteo = 3803

# Mostrar mensaje
mostrar_mensaje_bienvenida(primer_sorteo, primer_numero_sorteo)

sorteo = {
	'sorteo_id': 3803,
	'day': 3,
	'month': 1,
	'year': 2016,
    'week_day': 'domingo',
	'n1_loto': 7,
	'n2_loto': 14,
	'n3_loto': 16,
	'n4_loto': 19,
	'n5_loto': 24,
	'n6_loto': 35,
	'comodin': 5,
	'money_per_winner_loto': 0,
	'amount_of_winners_loto': 0,
	'money_per_winner_super_quina': 12380560,
	'amount_of_winners_super_quina': 3,
	'money_per_winner_quina': 342230,
	'amount_of_winners_quina': 20,
	'money_per_winner_super_cuaterna': 53470,
	'amount_of_winners_super_cuaterna': 128,
	'money_per_winner_cuaterna': 6250,
	'amount_of_winners_cuaterna': 1096,
	'money_per_winner_super_terna': 2460,
	'amount_of_winners_super_terna': 1278,
	'money_per_winner_terna': 1050,
	'amount_of_winners_terna': 10517,
	'money_per_winner_super_dupla': 1000,
	'amount_of_winners_super_dupla': 9919,
	'n1_recargado': 2,
	'n2_recargado': 17,
	'n3_recargado': 18,
	'n4_recargado': 28,
	'n5_recargado': 31,
	'n6_recargado': 41,
	'money_per_winner_recargado': 0,
	'amount_of_winners_recargado': 0,
	'n1_revancha': 1,
	'n2_revancha': 8,
	'n3_revancha': 9,
	'n4_revancha': 27,
	'n5_revancha': 30,
	'n6_revancha': 38,
	'money_per_winner_revancha': 0,
	'amount_of_winners_revancha': 0,
	'n1_desquite': 2,
	'n2_desquite': 17,
	'n3_desquite': 18,
	'n4_desquite': 28,
	'n5_desquite': 31,
	'n6_desquite': 41,
	'money_per_winner_desquite': 0,
	'amount_of_winners_desquite': 0,
}

agregar_sorteo(sorteo)