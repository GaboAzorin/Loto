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

print('\nAlgunas estadísticas:')
print('¿Se ha repetido algún resultado?')
print(f'    - {resultados_repetidos(DB_NAME)}')
print(f'Números más comunes en el día que sigue ({calcular_dia_siguiente()}):')
numeros_más_comunes, booleano = numeros_comunes_y_repetidos_por_dia(DB_NAME, calcular_dia_siguiente())
if booleano:
    print(f'    {numeros_más_comunes}. Este conjunto como tal SÍ se ha dado en un resultado.')
else:
    print(f'    {numeros_más_comunes}. Este conjunto como tal nunca se ha dado en un resultado.')

print(f'Números más comunes en el día numérico que sigue ({calcular_dia_siguiente_numerico()}):')
print(f'    {numeros_comunes_por_dia_numerico(DB_NAME, calcular_dia_siguiente_numerico())}')

time.sleep(1)

