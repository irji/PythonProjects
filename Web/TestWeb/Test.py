import streamlit as st



# Заголовок и ввод имени пользователя
user_name = st.text_input("Введите название тикета 15253", "")

# # Проверяем, введено ли имя пользователя
# if user_name:

# Список с названиями категорий
categories = ['ГУИ', 'Физика', 'IO', 'Скважины', 'Сторожа']
fields = {}

# Отображаем чек-боксы и при их выборе - поля ввода и загрузка изображений
for category in categories:
    if st.checkbox(category):
        user_input = st.text_area(f"Введите данные для {category}", "")

st.table()

# Кнопка создания файлов
if st.button("Создать"):
    st.warning(f"Тема и описание тикета не могут быть пустыми.")
