import datetime
import time
from methods import *
from sql_methods import *
import pyautogui as py
import time


# Configuración de la base de datos
DB_NAME = 'loto.db'
"""crear_db(DB_NAME)
exit()"""

# Fecha del primer sorteo y su número
primer_sorteo = datetime.datetime(2016, 1, 3, 21, 0)  
primer_numero_sorteo = 3803

# Mostrar mensaje
#mostrar_mensaje_bienvenida(primer_sorteo, primer_numero_sorteo, DB_NAME)

#add_sorteos_varios(1, DB_NAME)

ult = [7, 13, 16, 23, 29, 32]
print(f'Último sorteo: 7, 13, 16, 23, 29, 32')
print(get_combination_index(ult))

print('\nAlgunas estadísticas:')
#print('¿Se ha repetido algún resultado?')
#print(f'    - {resultados_repetidos(DB_NAME)}')
print(f'Números más comunes en el día que sigue ({calcular_dia_siguiente()}):')
n_tuple, all_tuple = numeros_comunes_por_criterios(DB_NAME, week_day=calcular_dia_siguiente())
print(f'    En cada "n": {n_tuple[0]} | ¿Se ha repetido?: {n_tuple[1]}')
print(f'        ¿Cuántas veces cada uno?: {n_tuple[2]}')
print(f'    En todas las letras o posiciones: {all_tuple[0]} | ¿Se ha repetido?: {all_tuple[1]}')
print(f'        ¿Cuántas veces cada uno?: {all_tuple[2]}')
print()

print(f'Números más comunes en el día que sigue ({calcular_dia_siguiente_numerico()}):')
n_tuple, all_tuple = numeros_comunes_por_criterios(DB_NAME, day=calcular_dia_siguiente_numerico())
print(f'    En cada "n": {n_tuple[0]} | ¿Se ha repetido?: {n_tuple[1]}')
print(f'        ¿Cuántas veces cada uno?: {n_tuple[2]}')
print(f'    En todas las letras o posiciones: {all_tuple[0]} | ¿Se ha repetido?: {all_tuple[1]}')
print(f'        ¿Cuántas veces cada uno?: {all_tuple[2]}')
print()

print(f'Números más comunes en el día que sigue ({calcular_dia_siguiente()} {calcular_dia_siguiente_numerico()}):')
n_tuple, all_tuple = numeros_comunes_por_criterios(DB_NAME, day=calcular_dia_siguiente_numerico(), week_day=calcular_dia_siguiente())
print(f'    En cada "n": {n_tuple[0]} | ¿Se ha repetido?: {n_tuple[1]}')
print(f'        ¿Cuántas veces cada uno?: {n_tuple[2]}')
print(f'    En todas las letras o posiciones: {all_tuple[0]} | ¿Se ha repetido?: {all_tuple[1]}')
print(f'        ¿Cuántas veces cada uno?: {all_tuple[2]}')

time.sleep(1)

