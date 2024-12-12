import streamlit as st
from new_app_methods import get_sorteo, get_full_date, welcome_phrase

#ChatGPT que me está ayudando:
#https://chatgpt.com/c/6758e7f1-bbbc-8003-863e-5c80182ae5b5

st.header("Predictor")

day, month, year, week_day, month_str, hour = get_full_date()

welcome, dayToCheck, monthToCheck = welcome_phrase(day, month, year, week_day, month_str, hour)

str_day = f'El día a revisar es el {dayToCheck} del mes {monthToCheck}.'
str_hour = f'La hora que se consideró es {hour}.'
st.write(str_day)
st.write(str_hour)
st.write(welcome)

st.write(get_sorteo(dayToCheck, monthToCheck, 2024))