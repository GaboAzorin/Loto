import requests
from bs4 import BeautifulSoup
from datetime import datetime, timedelta, date
import math
import pytz

def calcular_sorteo_id_y_fecha(day, month, year):
    """
    Ajusta la fecha al siguiente día de sorteo (si no es martes/jueves/domingo)
    y retorna (adjusted_day, adjusted_month, adjusted_year, sorteo_id).
    """

    # Fecha base y su ID
    base_date = date(2016, 1, 3)  # domingo, sorteo 3803
    base_id = 3803

    # Construir el objeto date con la fecha ingresada
    target_date = date(year, month, day)

    # Si la fecha es anterior a la base...
    if target_date < base_date:
        target_date = base_date

    # Ajustar al siguiente martes (1), jueves (3) o domingo (6) si no coincide
    dias_sorteo = [1, 3, 6]  # martes=1, jueves=3, domingo=6
    while target_date.weekday() not in dias_sorteo:
        target_date += timedelta(days=1)

    # En este punto, target_date es la fecha "ajustada"
    final_date = target_date

    # Calcular días desde la base
    delta_dias = (final_date - base_date).days

    # Cuántas semanas completas
    semanas_completas = delta_dias // 7
    dias_sobrantes = delta_dias % 7

    # Sorteos en semanas completas
    sorteos_en_semanas = semanas_completas * 3

    # Sorteos en los días sobrantes (máximo 6 días)
    fecha_inicial_sobrantes = base_date + timedelta(days=semanas_completas * 7)
    dias_sorteo_sobrantes = 0

    for i in range(dias_sobrantes + 1):
        fecha_iter = fecha_inicial_sobrantes + timedelta(days=i)
        if fecha_iter.weekday() in dias_sorteo:
            dias_sorteo_sobrantes += 1

    # Total de sorteos “nuevos” desde 3/1/2016 (excluyendo el propio 3/1/2016)
    sorteos_totales = sorteos_en_semanas + dias_sorteo_sobrantes - 1

    # sorteo_id final
    sorteo_id = base_id + sorteos_totales

    # Extraer la fecha ajustada
    adjusted_day = final_date.day
    adjusted_month = final_date.month
    adjusted_year = final_date.year

    return adjusted_day, adjusted_month, adjusted_year, sorteo_id

def get_full_date():
    # Configurar la zona horaria para Santiago de Chile
    chile_tz = pytz.timezone('America/Santiago')
    today_date = datetime.now(chile_tz)
    
    day = today_date.strftime("%d")
    month = today_date.strftime("%m")
    year = today_date.strftime("%Y")
    week_day = today_date.strftime("%A")
    hour = today_date.strftime("%H")

    if week_day == 'Monday':
        week_day = 'lunes'
    elif week_day == 'Tuesday':
        week_day = 'martes'
    elif week_day == 'Wednesday':
        week_day = 'miércoles'
    elif week_day == 'Thursday':
        week_day = 'jueves'
    elif week_day == 'Friday':
        week_day = 'viernes'
    elif week_day == 'Saturday':
        week_day = 'sábado'
    else:
        week_day = 'domingo'

    month_str = ''
    if month == '1':
        month_str = 'enero'
    elif month == '2':
        month_str = 'febrero'
    elif month == '3':
        month_str = 'marzo'
    elif month == '4':
        month_str = 'abril'
    elif month == '5':
        month_str = 'mayo'
    elif month == '6':
        month_str = 'junio'
    elif month == '7':
        month_str = 'julio'
    elif month == '8':
        month_str = 'agosto'
    elif month == '9':
        month_str = 'septiembre'
    elif month == '10':
        month_str = 'octubre'
    elif month == '11':
        month_str = 'noviembre'
    else:
        month_str = 'diciembre'
    
    return day, month, year, week_day, month_str, hour

def get_nums_from_index(index):
    if index < 1 or index > math.comb(41, 6):
        raise ValueError("Índice fuera de [1..4496388].")
    
    r = 6
    n_max = 41
    combination = []
    current = 1  # el menor valor que podemos colocar en la siguiente posición

    for i in range(r):
        for num in range(current, n_max - (r - i) + 2):
            c = math.comb(n_max - num, r - i - 1)
            if index <= c:
                combination.append(num)
                current = num + 1
                break
            else:
                index -= c

    return combination

def get_next_sorteo_date_chile():
    """
    Retorna (day, month, year) en enteros, correspondiente al próximo sorteo
    en Chile (Martes, Jueves o Domingo a las 21:00 hora local).
    """
    chile_tz = pytz.timezone('America/Santiago')
    now_chile = datetime.now(chile_tz)  # fecha/hora actual en Chile

    dias_sorteo = [1, 3, 6]  # martes=1, jueves=3, domingo=6
    hoy_weekday = now_chile.weekday()
    hora = now_chile.hour

    # Verifica si hoy es día de sorteo
    if hoy_weekday in dias_sorteo:
        if hora < 21:
            # Sugerimos HOY
            return now_chile.day, now_chile.month, now_chile.year
        else:
            # Ya pasó el sorteo de hoy (son >= 21h)
            fecha = now_chile + timedelta(days=1)
            while fecha.weekday() not in dias_sorteo:
                fecha += timedelta(days=1)
            return fecha.day, fecha.month, fecha.year
    else:
        # Hoy no es día de sorteo, buscar la próxima
        fecha = now_chile
        while fecha.weekday() not in dias_sorteo:
            fecha += timedelta(days=1)
        return fecha.day, fecha.month, fecha.year

def get_sorteo(day, month, year):
    url = (
        'https://resultados-de-loteria.com/loto-chile/resultados/'
        + str(day) + '-' + str(month) + '-' + str(year)
    )

    response = requests.get(url)

    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')
        numbers = soup.find_all('ul', class_='balls')
        numbers_str = [ul.text.strip() for ul in numbers]
        
        # Encontrar si alguien se ganó el premio
        winner = soup.find('table', class_='resultsTable noHover mobFormat')
        winner = winner.find_all('td', class_='nowrap')
        final_winners = str(winner[2].text)
        if final_winners.find('Acumulado') == 1:
            winner = False
        else:
            winner = True
        numbers_str.insert(0, winner)
        
    else:
        numbers_str = 'No pudimos meternos 😓: ' + str(response.status_code)
    
    return numbers_str

def welcome_phrase(day, month, year, week_day, month_str, hour):
    """
    Calcula la frase inicial a mostrar en la app, considerando la fecha/hora actual.
    """
    phrase = f'¡Hola, Gabriel! Hoy es {week_day} {day} de {month_str} del {year}.\n\n'
    day_to_return = ''
    month_to_return = month

    # Reglas para decidir día "pasado"
    if week_day == 'lunes' or week_day == 'martes':
        past_day = 'domingo'
    elif week_day == 'miércoles' or week_day == 'jueves':
        past_day = 'martes'
    elif week_day == 'viernes' or week_day == 'sábado' or week_day == 'domingo':
        past_day = 'jueves'

    # Si hoy es el día de sorteo
    if week_day == 'martes' or week_day == 'jueves' or week_day == 'domingo':
        if int(hour) <= 20:
            phrase_to_add = (
                f'Aún no se ha tirado el sorteo de hoy, así que te muestro el sorteo del {past_day} pasado:'
            )
            # Ajustar el día a mostrar
            if week_day == 'martes' or week_day == 'jueves':
                day_to_return = int(day) - 2
            else:  # si es 'domingo'
                day_to_return = int(day) - 3

            if int(day) <= 2:
                month_to_return = str(int(month) - 1)
        else:
            phrase_to_add = f'El sorteo se tiró hace poquito, aquí está:'
            day_to_return = day
        phrase += phrase_to_add
    else:
        # Hoy no hay sorteo
        phrase_to_add = (
            f'Hoy no corresponde sorteo, así que te muestro el sorteo del {past_day} pasado:'
        )
        phrase += phrase_to_add
        if week_day == 'lunes' or week_day == 'miércoles' or week_day == 'viernes':
            day_to_return = int(day) - 1
        elif week_day == 'sábado':
            day_to_return = int(day) - 2
    
    return phrase, day_to_return, month_to_return
