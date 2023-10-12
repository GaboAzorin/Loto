import datetime
import time
from methods import *
import pyautogui as py
from GAP_Utils.Utils import Play_end_mp3

# Configuración de la base de datos
DB_NAME = 'loto.db'


# Fecha del primer sorteo y su número
primer_sorteo = datetime.datetime(2016, 1, 3, 21, 0)  
primer_numero_sorteo = 3803

# Mostrar mensaje
mostrar_mensaje_bienvenida(primer_sorteo, primer_numero_sorteo, DB_NAME)

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

time.sleep(1)

prepare_screen()
all_text, list_of_sorteos = get_screen_info()
if len(list_of_sorteos) == 10:
	py.moveTo(990, 365)
else:
	py.moveTo(990, 418)

for i, sorteo in enumerate(list_of_sorteos):
	#if i <= (len(list_of_sorteos)-1):
	if i <= 1:
		time.sleep(0.5)
		if check_if_id_is_in_db(sorteo, DB_NAME):
			#agregar_sorteo(get_info_from_sorteo())
			print(get_info_from_sorteo())
		py.moveRel(0,53)

#agregar_sorteo(sorteo, DB_NAME)
Play_end_mp3()