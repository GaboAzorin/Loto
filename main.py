import datetime
import time
from methods import *
from sql_methods import *
import pyautogui as py
import time


# Configuración de la base de datos
DB_NAME = 'loto.db'
#crear_table(DB_NAME)

#agregar_columna(DB_NAME, 'sorteos', 'DESQUITE_posicion_en_4_5')

# _ _ _ _ _ _ _Convertir la base de datos en un excel
convertir_db_a_excel(DB_NAME, 'excel.xlsx')

# _ _ _ _ _ _ _Guarda los índices del sorteo en la tabla de los 4.5 millones
#guardar_indices_en_db(DB_NAME, 'loto')


# Fecha del primer sorteo y su número
primer_sorteo = datetime.datetime(2016, 1, 3, 21, 0)  
primer_numero_sorteo = 3803

# Mostrar mensaje
mostrar_mensaje_bienvenida(primer_sorteo, primer_numero_sorteo, DB_NAME)

# _ _ _ _ _ _ _ Imprimir los 100 clusters más comunes en esta fecha
n_de_clusters = 100
print(f'A continuación se muestran los {n_de_clusters} clusters, ordenados por los clusters que más resultados han aportado.')
print("Se verán así:\n('Nº de cluster: resultado menor-resultado mayor del cluster', nº de sorteos que vinieron de este cluster, '% de participación del cluster')\n")
print(agrupar_y_contar(DB_NAME, n_de_clusters, 'loto_posicion_en_4_5'))

# _ _ _ _ _ _ _ AGREGAR SORTEOS.
#add_sorteos_varios(1, DB_NAME)
#numeros_frecuentes_por_sorteo(DB_NAME, 'loto')


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

