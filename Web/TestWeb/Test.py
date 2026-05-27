import streamlit as st



# Заголовок и ввод имени пользователя
user_name = st.text_input("Введите название тикета 15253", "")

# Проверяем, введено ли имя пользователя
if user_name:
    # Список с названиями категорий
    categories = ['ГУИ', 'Физика', 'IO', 'Скважины', 'Сторожа']
    fields = {}

    # Отображаем чек-боксы и при их выборе - поля ввода и загрузка изображений
    for category in categories:
        if st.checkbox(category):
            user_input = st.text_area(f"Введите данные для {category}", "")

    base_task_id = 0

    # Кнопка создания файлов
    if st.button("Создать"):
        for i, (field_name, (text, image_file)) in enumerate(fields.items(), start=1):
            if text:
                task_id = 1111
            else:
                st.warning(f"Тема и описание тикета не могут быть пустыми.")
