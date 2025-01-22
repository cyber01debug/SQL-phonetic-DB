# импортируем библиотеки
from flask import Flask, render_template, request
import sqlite3
import pandas as pd

DATABASE = 'data\data_base.db'  #путь к базе данных формата .db

def db_connection():
    '''Устанавливает соединение с базой данных'''
    conn = sqlite3.connect(DATABASE) #устанавливаем соединение с базой, прописанной в DATABASE
    conn.row_factory = sqlite3.Row #используем row_factory для возврата строк базы в виде словарей
    return conn

def tables_list():
    '''Получает список всех таблиц в базе данных'''
    conn = db_connection() #соединяемся с бд 
    cursor = conn.cursor() #создаем курсор для sql запросов
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';") #выполняем запрос для получения списка имен таблиц
    tables = [row[0] for row in cursor.fetchall()] #извлекаем имена таблиц 
    conn.close() #закрываем соединение
    return tables

def pd_table_data(table_name):
    '''Получает данные из указанной таблицы с помощью pandas'''
    conn = db_connection() #открываем соединение
    query = f"SELECT * FROM {table_name}" #создаем запрос по указаной таблице для получения всех данных
    df = pd.read_sql_query(query, conn) #выполняем sql запрос с помощью pandas и получает DataFrame (df)
    conn.close() #закрываем соединение
    return df

def statistic(df):
    '''Вычисляет статистику для df'''
    # получаем имена всез числовых столбцов бд
    num_col = df.select_dtypes(include=['number']).columns
    # создаем новый дата фрейм для статистических данных
    stats = pd.DataFrame({
        'Сумма': df[num_col].sum(),
        'Количество': df[num_col].count(),
        'Среднее': df[num_col].mean(),
        'Минимальное': df[num_col].min(), 
        'Максимальное': df[num_col].max(),
        'Медиана': df[num_col].median(), 
        'Отклонение': df[num_col].std()
    })
    # преобразуем дата фрейм в словарь и возвращает его 
    return stats.to_dict(orient='index')