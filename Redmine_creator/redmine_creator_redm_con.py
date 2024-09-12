import streamlit as st
from redminelib import Redmine

# Конфигурация Redmine
redmine_url = 'https://your-redmine-url.com'  # URL вашего Redmine
api_key = 'your-api-access-key'  # Ваш API Access Key

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

        # Создаем тикет в Redmine
        issue = redmine.issue.create(
            project_id=project_id,
            subject=subject,
            description=description,
            uploads=uploads
        )
        st.success(f"Тикет '{subject}' успешно создан! ID: {issue.id}")

    except Exception as e:
        st.error(f"Ошибка при создании тикета: {e}")

# Ввод названия приложения и имени пользователя
user_name = st.text_input("Введите ваше имя", "")

if user_name:
    app_title = st.text_input("Введите название приложения", "Приложение с вводом данных")
    st.title(app_title)

    categories = ['ГУИ', 'Физика', 'IO', 'Скважины', 'Сторожа']
    fields = {}

    # Поля ввода и загрузка изображений
    for category in categories:
        if st.checkbox(category):
            user_input = st.text_area(f"Введите данные для {category}", "")
            uploaded_image = st.file_uploader(f"Прикрепите изображение для {category}", type=["png", "jpg", "jpeg"])
            fields[category] = (user_input, uploaded_image)

    # ID проекта в Redmine
    project_id = st.text_input("Введите ID проекта в Redmine", "")

    if st.button("Создать"):
        if project_id.isdigit():
            project_id = int(project_id)
            for field_name, (text, image_file) in fields.items():
                if text:
                    subject = f"{user_name} - {field_name}"
                    create_redmine_ticket(project_id, subject, text, image_file)
                else:
                    st.warning(f"Поле '{field_name}' пустое. Тикет не будет создан.")
        else:
            st.warning("Пожалуйста, введите корректный ID проекта.")

else:
    st.warning("Пожалуйста, введите ваше имя.")
