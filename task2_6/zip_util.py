# -*- coding: utf-8 -*-
"""
Created on Sun Dec 14 18:06:36 2025

@author: maalv
"""

import csv
import sys
import os

CSV_FILENAME = "zip_codes_states.csv"

def read_zip_all():
    """
    Читает данные из CSV файла и возвращает список списков (структура из задания).
    """
    if not os.path.exists(CSV_FILENAME):
        # В реальной задаче этот модуль просто возвращает пустой список или вызывает ошибку, 
        # но мы добавим проверку файла для надежности.
        print(f"Ошибка в zip_util: Файл данных '{CSV_FILENAME}' не найден.")
        sys.exit(1)

    data = []
    try:
        with open(CSV_FILENAME, mode='r', newline='', encoding='utf-8') as file: # 1. Открытие файла
            reader = csv.reader(file) # 2. Создание объекта для чтения CSV
            next(reader) # 3. Пропускаем строку заголовков
            for row in reader: # 4. Чтение данных построчно
                # row уже является списком строк
                # Преобразуем latitude и longitude в float, остальное оставляем как строки
                try:
                    row[1] = float(row[1]) # latitude
                    row[2] = float(row[2]) # longitude
                    data.append(row) # Добавляем готовую строку (теперь уже с числами) в итоговый список
                except ValueError:
                    # Пропускаем строки с некорректными данными
                    continue
    except Exception as e:
        print(f"Произошла ошибка при чтении файла CSV в zip_util: {e}")
        sys.exit(1)
        
    return data