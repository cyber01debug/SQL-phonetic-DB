# импортируем библиотеки
import pandas as pd
from flask import Flask, render_template, request
from functions import * #импортируем все из файла с функциями

# создаем фласк приложение
app = Flask(__name__)

# определяем маршрут для страницы html, которая обрабатывает get и post запросы
@app.route('/', methods=['GET', 'POST']) 
def index():
    '''Отображает главную страницу со списком таблиц и данными выбранной таблицы'''
    tables = tables_list() #получаем список всех таблиц из нашей базы данных
    selected_table = request.form.get('table_select') #получаем имя выбранной таблицы
    filter_value = request.form.get('filter_value') #получаем значение параметра при фильрации данных  
    # создаем переменные для хранения данных таблицы ее статистики и об ошибках
    table_data = None
    stats_data = None
    error_message = None
    no_results_message = None

    # если мы выбрали одну из пяти таблиц
    if selected_table:
        # получаем данные из выбранной таблицы
        df = pd_table_data(selected_table)

        # если мы задали какой либо параметр при поиске
        if filter_value:
            # фильтрация идет только по столбцу items_
            if 'items_' in df.columns: 
                # фильтруем данные в столбике 
                df_filtered = df[df['items_'].astype(str).str.contains(filter_value, case=False)]
                # если ничего не найдено выводим об этом сообщение 
                if df_filtered.empty:
                    no_results_message = "По запросу ничего не нашлось."
                else: #если подходящие данные есть, то конвертируем их в формат списка словарей и вычисляет статистику
                    table_data = df_filtered.to_dict(orient='records')
                    stats_data = statistic(df_filtered)
            else: #если столбца items нет в таблице выводим сообщение об этом
                error_message = "В выбранной таблице отсутствует столб items!"
        else: #если мы не вводили параметр для поиска то все равно выводится выбранная таблица 
            table_data = df.to_dict(orient='records')
            stats_data = statistic(df)
    # возвращаем нашу страницу html со всеми данными и фильтрами
    return render_template('index.html', tables=tables, table_data=table_data, selected_table=selected_table, filter_value=filter_value, stats_data=stats_data, error_message=error_message, no_results_message = no_results_message)
# запускаем flask приложение
if __name__ == '__main__':
    app.run(debug=True)