import streamlit as st
import os

# Функция для сохранения текста и изображения в файлы
def save_to_file(field_name, user_name, text, image_file, index):
    text_filename = f"{user_name}_{field_name}_{index}.txt"
    with open(text_filename, 'w', encoding='utf-8') as text_file:
        text_file.write(text)
    st.success(f"Файл '{text_filename}' успешно создан!")

    if image_file is not None:
        image_filename = f"{user_name}_{field_name}_{index}.png"
        with open(image_filename, "wb") as image_file_object:
            image_file_object.write(image_file.getbuffer())
        st.success(f"Файл изображения '{image_filename}' успешно создан!")

# Заголовок и ввод имени пользователя
user_name = st.text_input("Введите название тикета", "")

# Проверяем, введено ли имя пользователя
if user_name:
    # Список с названиями категорий
    categories = ['ГУИ', 'Физика', 'IO', 'Скважины', 'Сторожа']
    fields = {}

    # Отображаем чек-боксы и при их выборе - поля ввода и загрузка изображений
    for category in categories:
        if st.checkbox(category):
            user_input = st.text_area(f"Введите данные для {category}", "")
            uploaded_image = st.file_uploader(f"Прикрепите изображение для {category}", type=["png", "jpg", "jpeg"])
            fields[category] = (user_input, uploaded_image)

    # Кнопка создания файлов
    if st.button("Создать"):
        if not os.path.exists('output'):
            os.makedirs('output')
        os.chdir('output')
        for i, (field_name, (text, image_file)) in enumerate(fields.items(), start=1):
            if text:
                save_to_file(field_name, user_name, text, image_file, i)
            else:
                st.warning(f"Поле {field_name} пустое. Файл не будет создан.")
        os.chdir('..')

# Инструкция по запуску приложения
st.write("Запустите это приложение командой `streamlit run app.py` в вашей командной строке.")
