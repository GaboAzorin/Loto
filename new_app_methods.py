import requests
from bs4 import BeautifulSoup
from datetime import datetime

def get_full_date():
    today_date = datetime.now()
    
    day = today_date.strftime("%d")  # Día en formato de dos dígitos
    month = today_date.strftime("%m")  # Mes en formato de dos dígitos
    year = today_date.strftime("%Y")  # Año en formato de cuatro dígitos
    week_day = today_date.strftime("%A")  # Día de la semana en texto completo (ej: Monday)
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
        month_str = ' mayo'
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

def get_sorteo(day, month, year):
    url = 'https://resultados-de-loteria.com/loto-chile/resultados/' + str(day) + '-' + str(month) + '-' + str(year)

    response = requests.get(url)

    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')
        numbers = soup.find_all('ul', class_='balls')
        numbers_str = [ul.text.strip() for ul in numbers]
        
    else:
        numbers_str = 'No pudimos meternos 😓: ' + str(response.status_code)
    
    return numbers_str

def welcome_phrase(day, month, year, week_day, month_str, hour):
    """
    Función que devuelve la frase inicial que se mostrará en la app.
    Calcula el día y la hora, de manera de decir, también, qué sorteo se muestra
    """

    phrase = f'¡Hola, Gabriel! Hoy es {week_day} {day} de {month_str} del {year}.\n\n'
    day_to_return = ''
    month_to_return = month

    # Reglas para decidir día
    ## Decidir día pasado
    if week_day == 'lunes' or week_day == 'martes':
        past_day = 'domingo'
    elif week_day == 'miércoles' or week_day == 'jueves':
        past_day = 'martes'
    elif week_day == 'viernes' or week_day == 'sábado' or week_day == 'domingo':
        past_day = 'jueves'

    # Si es que es el día que corresponde
    if week_day == 'martes' or week_day == 'jueves' or week_day == 'domingo':
        if int(hour) <= 20:
            phrase_to_add = f'Aún no se ha tirado el sorteo de hoy, así que te muestro el sorteo del {past_day} pasado:'
            if week_day == 'martes' or week_day == 'jueves': day_to_return = int(day)-2
            else: day_to_return = int(day)-3

            if int(day) <= 2: month_to_return = str(int(month)-1)
        else:
            phrase_to_add = f'El sorteo se tiró hace poquito, aquí está:'
            day_to_return = day
        phrase += phrase_to_add
    else: # Si hoy no hay sorteo
        phrase_to_add = f'Hoy no corresponde sorteo, así que te muestro el sorteo del {past_day} pasado:'
        phrase += phrase_to_add
        if week_day == 'lunes' or week_day == 'miércoles' or week_day == 'viernes':
            day_to_return = int(day)-1
        elif week_day == 'sábado':
            day_to_return = int(day)-2
    
    return phrase, day_to_return, month_to_return