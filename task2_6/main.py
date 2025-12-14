# -*- coding: utf-8 -*-
"""
Created on Sun Dec 14 14:27:39 2025

@author: maalv
"""

import zip_util
import math
import sys

zip_to_details = {}
city_state_to_zips = {}
# Используем радиус Земли (in km = 6371.0)
EARTH_RADIUS = 3958.8 #я не знаю почему возникло расхождение в долях мили с примером из задания. Округлённое значение (3959) также даёт немного отличающийся (на сотую) результат

def load_data():
    print("Загрузка данных о почтовых индексах...")
    # Получаем данные через функцию из нашего модуля
    zip_codes_list = zip_util.read_zip_all() 
    for record in zip_codes_list:
        # Структура: [zip_code(0), latitude(1), longitude(2), city(3), state(4), county(5)]
        zip_code = record[0]
        zip_to_details[zip_code] = {
            'lat': record[1],
            'lon': record[2],
            'city': record[3],
            'state': record[4],
            'county': record[5]
        }
        city_state_key = (record[3].upper(), record[4].upper())
        if city_state_key not in city_state_to_zips: #Уникальность пар Город/Штат
            city_state_to_zips[city_state_key] = []
        city_state_to_zips[city_state_key].append(zip_code)
    print(f"Загружено {len(zip_to_details)} уникальных почтовых индексов.")

def calculate_distance(lat1, lon1, lat2, lon2):
    # Перевод градусов в радианы через шаманство модуля math
    lat1_rad = math.radians(lat1)
    lon1_rad = math.radians(lon1)
    lat2_rad = math.radians(lat2)
    lon2_rad = math.radians(lon2)
    dlon = lon2_rad - lon1_rad
    dlat = lat2_rad - lat1_rad
    # Формула гаверсинусов
    a = math.sin(dlat / 2)**2 + math.cos(lat1_rad) * math.cos(lat2_rad) * math.sin(dlon / 2)**2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))

    distance = EARTH_RADIUS * c
    return distance

def format_coords(lat, lon):
    def deg_to_dms(degrees):
        # Преобразуем десятичные градусы в градусы, минуты, секунды через офигенную функцию divmod
        # (знал бы я о ней раньше), которая присваивает значения сразу двум переменным
        # (целочисленное и %остаток от деления)
        minutes, seconds = divmod(abs(degrees) * 3600, 60) 
        degrees, minutes = divmod(minutes, 60)
        return int(degrees), int(minutes), seconds #Возвращаем наш суповой наборчик

    d_lat, m_lat, s_lat = deg_to_dms(lat)
    d_lon, m_lon, s_lon = deg_to_dms(lon)
    
    lat_dir = 'N' if lat >= 0 else 'S' #В США нет (вроде) городов в южном полушарии, но раз уж пилим, то пусть будет
    lon_dir = 'E' if lon >= 0 else 'W' #А вот в восточном полушарии - есть (привет Аляска, Гавайи, и вроде что-то в атлантике тоже было))
    # Форматирование с ведущими нулями
    # (03d, 02d, 05 (d - целое, 3,2,5 - нужная длина строки, 0 - символ спереди, если надо))
    # и точностью до 2 знаков после запятой (.2f) для секунд
    lat_str = f"{d_lat:03d}˚{m_lat:02d}'{s_lat:05.2f}\"{lat_dir}"
    lon_str = f"{d_lon:03d}˚{m_lon:02d}'{s_lon:05.2f}\"{lon_dir}"
    
    return f"({lat_str},{lon_str})"

def repl_loop():
    while True:
        try:
            command_input = input("Command ('loc', 'zip', 'dist', 'end') => ").strip().lower()
            print(command_input) # Печатаем команду, как в примере задания. Хотя как по мне не особо красиво

            if command_input == 'end':
                print("Done")
                break
            elif command_input == 'loc':
                handle_loc()
            elif command_input == 'zip':
                handle_zip()
            elif command_input == 'dist':
                handle_dist()
            else:
                print("Invalid command, ignoring")
        except KeyboardInterrupt: #ловим бряку (в инпуте нажать ctrl-c). Да, я поймал))) Чисто интересная фишка, в коде не нужно.
            print("\nExiting...")
            print("Done")
            break

def handle_loc():
    zip_code_input = input("Enter a ZIP Code to lookup => ").strip()
    print(zip_code_input)

    if zip_code_input in zip_to_details:
        details = zip_to_details[zip_code_input]
        coords_str = format_coords(details['lat'], details['lon'])
        print(f"ZIP Code {zip_code_input} is in {details['city']}, {details['state']}, {details['county']} county,")
        print(f"coordinates: {coords_str}")
    else:
        print(f"Error: ZIP Code {zip_code_input} not found or invalid.")

def handle_zip():
    city_input = input("Enter a city name to lookup => ").strip().upper()
    print(city_input)
    state_input = input("Enter the state name to lookup => ").strip().upper()
    print(state_input)

    key = (city_input, state_input)
    if key in city_state_to_zips:
        zips = sorted(city_state_to_zips[key]) # Сортируем для красивого вывода. Не уверен, что необходимо, вероятно в ксв уже всё и так причесано. Пусть будет
        print(f"The following ZIP Code(s) found for {city_input}, {state_input}: {', '.join(zips)}")
    else:
        print(f"Error: City/State combination {city_input}, {state_input} not found.")

def handle_dist():
    zip1 = input("Enter the first ZIP Code => ").strip()
    print(zip1)
    zip2 = input("Enter the second ZIP Code => ").strip()
    print(zip2)

    if zip1 in zip_to_details and zip2 in zip_to_details:
        details1 = zip_to_details[zip1]
        details2 = zip_to_details[zip2]
        
        distance = calculate_distance(
            details1['lat'], details1['lon'],
            details2['lat'], details2['lon']
        )
        print(f"The distance between {zip1} and {zip2} is {distance:.2f} miles")
    else:
        print("Error: One or both ZIP Codes not found or invalid.")

if __name__ == "__main__":
    load_data()
    repl_loop()