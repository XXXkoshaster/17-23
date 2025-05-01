import streamlit as st
import pandas as pd
import time

# Загрузка данных из CSV-файла
data = pd.read_csv('data.csv')

# Настройка заголовка приложения
st.title('Данные компаний')

# Отображение данных в виде таблицы
st.write("Ниже представлены данные:")
st.dataframe(data)

# Создание текстового ввода для выбора ИНН
inn_index = st.text_input('Введите ИНН для подробной информации:')

# Получение и отображение подробной информации по выбранному ИНН
if st.button('Показать подробности'):
    if inn_index in data['inn'].astype(str).values:
        st.write("Подробная информация:")
        st.write(data.loc[data['inn'].astype(str) == inn_index])
    else:
        st.error("ИНН не найден!")

# Форма для добавления новой компании
with st.form(key='add_company_form'):
    new_inn_index = st.text_input('Введите новый ИНН:')
    new_data_index = st.text_input('Введите новые данные:')
    submit_button = st.form_submit_button(label='Добавить')

new_id=len(data)+1

if submit_button:
    if new_inn_index and new_data_index:
        
        new_row = pd.DataFrame({'id': [new_id], 'inn': [new_inn_index], 
                                'data': [new_data_index], 'fetched_at': [time.ctime()]})
        data = pd.concat([data, new_row], ignore_index=True)
        
        # Сохранение изменений в CSV (если нужно)
        data.to_csv('data.csv', index=False)
        
        st.success('Компания добавлена!')
        st.dataframe(data)
    else:
        st.error('Пожалуйста, заполните все поля.')
