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

# _ _ _ _ _ _ _Guarda los índices del sorteo en la tabla de los 4.5 millones (DEPRECADO)
#guardar_indices_en_db(DB_NAME, 'loto')

# _ _ _ _ _ _ _ AGREGAR SORTEOS.
#add_sorteos_varios(1, DB_NAME)
#numeros_frecuentes_por_sorteo(DB_NAME, 'loto')
# _ _ _ _ _ _ _Convertir la base de datos en un excel
convertir_db_a_excel(DB_NAME, 'excel.xlsx')

# Fecha del primer sorteo y su número
primer_sorteo = datetime.datetime(2016, 1, 3, 21, 0)  
primer_numero_sorteo = 3803

# Mostrar mensaje
# mostrar_mensaje_bienvenida(primer_sorteo, primer_numero_sorteo, DB_NAME)

# _ _ _ _ _ _ _ Imprimir los 100 clusters más comunes en esta fecha
n_de_clusters = 100
#print(f'A continuación se muestran los {n_de_clusters} clusters, ordenados por los clusters que más resultados han aportado.')
#print("Se verán así:\n('Nº de cluster: resultado menor-resultado mayor del cluster', nº de sorteos que vinieron de este cluster, '% de participación del cluster')\n")
#print(agrupar_y_contar(DB_NAME, n_de_clusters, 'loto_posicion_en_4_5'))




print('\nAlgunas estadísticas:')
#print('¿Se ha repetido algún resultado?')
#print(f'    - {resultados_repetidos(DB_NAME)}')
# Mostrar el cluster más común
cluster_frecuente = cluster_mas_comun(DB_NAME)
if cluster_frecuente:
    print(f'Cluster más común (general): {cluster_frecuente[0]} con {cluster_frecuente[1]} ocurrencias')
else:
    print('Cluster más común (general): No se encontraron resultados para el cluster más común (general).')
print()
print(f'Números más comunes en el día que sigue ({calcular_dia_siguiente()}):')
n_tuple, all_tuple = numeros_comunes_por_criterios(DB_NAME, week_day=calcular_dia_siguiente())
print(f'    En cada "n": {n_tuple[0]} | ¿Se ha repetido?: {n_tuple[1]}')
print(f'        ¿Cuántas veces cada uno?: {n_tuple[2]}')
print(f'    En todas las letras o posiciones: {all_tuple[0]} | ¿Se ha repetido?: {all_tuple[1]}')
print(f'        ¿Cuántas veces cada uno?: {all_tuple[2]}')
print()
# Mostrar el cluster más común para el día que sigue
next_week_day = calcular_dia_siguiente()
cluster_frecuente = cluster_mas_comun(DB_NAME, week_day=next_week_day)
if cluster_frecuente:
    print(f'    Cluster más común en el día que sigue ({next_week_day}): {cluster_frecuente[0]} con {cluster_frecuente[1]} ocurrencias')
else:
    print(f'    Cluster más común en el día que sigue ({next_week_day}): No se encontraron resultados para el cluster más común en el día que sigue ({next_week_day}).')
print()

print(f'Números más comunes en el día que sigue ({calcular_dia_siguiente_numerico()}):')
n_tuple, all_tuple = numeros_comunes_por_criterios(DB_NAME, day=calcular_dia_siguiente_numerico())
print(f'    En cada "n": {n_tuple[0]} | ¿Se ha repetido?: {n_tuple[1]}')
print(f'        ¿Cuántas veces cada uno?: {n_tuple[2]}')
print(f'    En todas las letras o posiciones: {all_tuple[0]} | ¿Se ha repetido?: {all_tuple[1]}')
print(f'        ¿Cuántas veces cada uno?: {all_tuple[2]}')
next_day_numeric = calcular_dia_siguiente_numerico()
cluster_frecuente = cluster_mas_comun(DB_NAME, day=next_day_numeric)
if cluster_frecuente:
    print(f'    Cluster más común en el día {next_day_numeric}: {cluster_frecuente[0]} con {cluster_frecuente[1]} ocurrencias')
else:
    print(f'    Cluster más común en el día {next_day_numeric}: No se encontraron resultados para el cluster más común en el día {next_day_numeric}.')
print()

print(f'Números más comunes en el día que sigue ({calcular_dia_siguiente()} {calcular_dia_siguiente_numerico()}):')
n_tuple, all_tuple = numeros_comunes_por_criterios(DB_NAME, day=calcular_dia_siguiente_numerico(), week_day=calcular_dia_siguiente())
print(f'    En cada "n": {n_tuple[0]} | ¿Se ha repetido?: {n_tuple[1]}')
print(f'        ¿Cuántas veces cada uno?: {n_tuple[2]}')
print(f'    En todas las letras o posiciones: {all_tuple[0]} | ¿Se ha repetido?: {all_tuple[1]}')
print(f'        ¿Cuántas veces cada uno?: {all_tuple[2]}')
print()

cluster_frecuente = cluster_mas_comun(DB_NAME, day=next_day_numeric, week_day=next_week_day)
if cluster_frecuente:
    print(f'    Cluster más común en el día que sigue ({next_week_day} {next_day_numeric}): {cluster_frecuente[0]} con {cluster_frecuente[1]} ocurrencias')
else:
    print(f'    Cluster más común en el día que sigue ({next_week_day} {next_day_numeric}): No se encontraron resultados para el cluster más común en el día que sigue ({next_week_day} {next_day_numeric}).')
print()

actual_year = datetime.datetime.now().year
print(f'Números más comunes en este año ({actual_year}):')
n_tuple, all_tuple = numeros_comunes_por_criterios(DB_NAME, year=actual_year)
print(f'    En cada "n": {n_tuple[0]} | ¿Se ha repetido?: {n_tuple[1]}')
print(f'        ¿Cuántas veces cada uno?: {n_tuple[2]}')
print(f'    En todas las letras o posiciones: {all_tuple[0]} | ¿Se ha repetido?: {all_tuple[1]}')
print(f'        ¿Cuántas veces cada uno?: {all_tuple[2]}')
actual_year = datetime.datetime.now().year
cluster_frecuente = cluster_mas_comun(DB_NAME, year=actual_year)
if cluster_frecuente:
    print(f'    Cluster más común en este año ({actual_year}): {cluster_frecuente[0]} con {cluster_frecuente[1]} ocurrencias')
else:
    print(f'    Cluster más común en este año ({actual_year}): No se encontraron resultados para el cluster más común en este año ({actual_year}).')

print('\n\n¿Se han repetido resultados?\n')

repetidos = resultados_repetidos_adaptable(DB_NAME, 'loto', 'loto')
if repetidos:
    print(f"- Se han encontrado combinaciones repetidas en el loto:")
    for comb, count in repetidos:
        print(f"Combinación {comb} se ha repetido {count} veces")
else:
    print(f"- No se encontraron combinaciones repetidas en el loto.")

repetidos = resultados_repetidos_adaptable(DB_NAME, 'loto', 'RECARGADO')
if repetidos:
    print(f"- Se han encontrado combinaciones repetidas entre el loto y el recargado:")
    for comb, count in repetidos:
        print(f"Combinación {comb} se ha repetido {count} veces")
else:
    print(f"- No se encontraron combinaciones repetidas entre el loto y el recargado.")

repetidos = resultados_repetidos_adaptable(DB_NAME, 'loto', 'REVANCHA')
if repetidos:
    print(f"- Se han encontrado combinaciones repetidas entre el loto y el revancha:")
    for comb, count in repetidos:
        print(f"Combinación {comb} se ha repetido {count} veces")
else:
    print(f"- No se encontraron combinaciones repetidas entre el loto y el revancha.")

repetidos = resultados_repetidos_adaptable(DB_NAME, 'loto', 'DESQUITE')
if repetidos:
    print(f"- Se han encontrado combinaciones repetidas entre el loto y el desquite:")
    for comb, count in repetidos:
        print(f"Combinación {comb} se ha repetido {count} veces")
else:
    print(f"- No se encontraron combinaciones repetidas entre el loto y el desquite.")