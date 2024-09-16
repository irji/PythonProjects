import streamlit as st
from redminelib import Redmine

# Конфигурация Redmine
redmine_url = 'https://redmine.rfdyn.ru'  # URL вашего Redmine
api_key = '401a6b058962fbd1063c570fb0a1f99361c7e9b3'  # Ваш API Access Key

# Создание экземпляра Redmine
redmine = Redmine(redmine_url, key=api_key)

# Функция для создания тикета в Redmine
def create_redmine_ticket(project_id, subject, description, image_file=None):
    try:
        # Список прикрепленных файлов
        uploads = []

        # Если изображение загружено, загружаем его в Redmine
        if image_file is not None:
            upload = redmine.upload.create(file=image_file)
            uploads.append({'token': upload.token, 'filename': image_file.name, 'description': "Прикрепленное изображение"})

        # {'id': 47, 'name': 'Error', 'value': 'Да'},
        # {'id': 9, 'name': 'QA', 'value': ''},
        #  {'id': 2, 'name': 'Module', 'value': 'Model Designer'},
        #  {'id': 4, 'name': 'Account', 'multiple': True, 'value': []},
        #  {'id': 7, 'name': 'Planned Version', 'value': '279'},
        #  {'id': 8, 'name': 'Announced', 'value': '0'},
        #  {'id': 12, 'name': 'Licenses', 'multiple': True, 'value': []},
        #  {'id': 10, 'name': 'Staff', 'multiple': True, 'value': ['Dmirty Ivanov (Oman)']},
        #  {'id': 73, 'name': 'BTR', 'value': None}]

        # Создаем тикет в Redmine
        issue = redmine.issue.create(
            project_id=project_id,
            subject=subject,
            description=description,
            priority_id=7,
            assigned_to_id=114,
            fixed_version_id=279,
            watcher_user_ids=[127],
            #parent_issue_id=parrent_task_id,
            #uploads=uploads,
            custom_fields=[{'id': 47, 'value': 'Нет'}, {'id': 2, 'value': 'Model Designer'}]
        )
        st.success(f"Задача с номером '{issue.id}' успешно создана!")
        return issue.id

    except Exception as e:
        st.success(f"Ошибка при создании тикета: {e}")
        return 0

# Функция для свзывания тикетов
def related_task(base_id, related_id):
    try:
        # Связываем между собой тикеты
        relation = redmine.issue_relation.create(
            issue_id=base_id,
            issue_to_id=related_id,
            relation_type='relates'
        )
        #st.success(f"Тикет с номером '{issue.id}' успешно создан!")

    except Exception as e:
        #print(f"Ошибка при создании тикета: {e}")
        st.success(f"Ошибка при связывании тикетов: {e}")


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

    base_task_id = 0

    # Кнопка создания файлов
    if st.button("Создать"):
        for i, (field_name, (text, image_file)) in enumerate(fields.items(), start=1):
            if text:
                task_id = create_redmine_ticket("new-models", field_name + ": " + user_name, text)

                if base_task_id == 0:
                    base_task_id = task_id
                else:
                    related_task(base_task_id, task_id)
            else:
                st.warning(f"Тема и описание тикета не могут быть пустыми.")
