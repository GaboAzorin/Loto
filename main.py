import datetime
import time
from methods import *
from sql_methods import *
import pyautogui as py
import time


# Configuración de la base de datos
DB_NAME = 'loto.db'
numeros_frecuentes_por_sorteo(DB_NAME, 'loto')
#exit()
#crear_table(DB_NAME)

#agregar_columna(DB_NAME, 'sorteos', 'n6_loto_mas_comun')
#guardar_indices_en_db(DB_NAME, 'DESQUITE')
exit()


# Fecha del primer sorteo y su número
primer_sorteo = datetime.datetime(2016, 1, 3, 21, 0)  
primer_numero_sorteo = 3803

# Mostrar mensaje
#mostrar_mensaje_bienvenida(primer_sorteo, primer_numero_sorteo, DB_NAME)

"""print(agrupar_y_contar(DB_NAME, 2, 'normal_ordenada_loto'))
print()
print(agrupar_y_contar(DB_NAME, 3, 'normal_ordenada_loto'))
print()
print(agrupar_y_contar(DB_NAME, 4, 'normal_ordenada_loto'))
print()
print(agrupar_y_contar(DB_NAME, 5, 'normal_ordenada_loto'))
print()
print(agrupar_y_contar(DB_NAME, 6, 'normal_ordenada_loto'))
print()
print(agrupar_y_contar(DB_NAME, 7, 'normal_ordenada_loto'))
print()
print(agrupar_y_contar(DB_NAME, 8, 'normal_ordenada_loto'))
print()
print(agrupar_y_contar(DB_NAME, 9, 'normal_ordenada_loto'))
print()"""
print(agrupar_y_contar(DB_NAME, 100, 'normal_ordenada_loto'))


#add_sorteos_varios(1, DB_NAME)

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
print()

actual_year = datetime.datetime.now().year
print(f'Números más comunes en este año ({actual_year}):')
n_tuple, all_tuple = numeros_comunes_por_criterios(DB_NAME, year=actual_year)
print(f'    En cada "n": {n_tuple[0]} | ¿Se ha repetido?: {n_tuple[1]}')
print(f'        ¿Cuántas veces cada uno?: {n_tuple[2]}')
print(f'    En todas las letras o posiciones: {all_tuple[0]} | ¿Se ha repetido?: {all_tuple[1]}')
print(f'        ¿Cuántas veces cada uno?: {all_tuple[2]}')

time.sleep(1)

