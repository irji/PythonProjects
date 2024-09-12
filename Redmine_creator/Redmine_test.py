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

        # Создаем тикет в Redmine
        issue = redmine.issue.create(
            project_id=project_id,
            subject=subject,
            description=description,
            priority=7,
            assigned_to_id=114,
            fixed_version_id='24.4',
            #uploads=uploads,
            custom_fields=[{'id': 0, 'value': False}, {'id': 2, 'value': 'Model Designer'}]
        )
        print(f"Тикет '{subject}' успешно создан! ID: {issue.id}")

    except Exception as e:
        print(f"Ошибка при создании тикета: {e}")

def read_redmine_ticket(resource_id):
    # ['allowed_statuses', 'assigned_to', 'attachments', 'author', 'changesets', 'children', 'closed_on', 'created_on',
    #  'custom_fields', 'description', 'done_ratio', 'due_date', 'estimated_hours', 'fixed_version', 'id', 'internal_id',
    #  'is_private', 'journals', 'manager', 'priority', 'project', 'relations', 'spent_hours', 'start_date', 'status',
    #  'subject', 'time_entries', 'total_estimated_hours', 'total_spent_hours', 'tracker', 'updated_on', 'url',
    #  'watchers']

    # Custom fields values
    # 0 "Error">,
    # 1 "QA">,
    # 2 "Module">,
    # 3 "Account">,
    # 4 "Planned Version">,
    # 5 "Announced">,
    # 6 "Licenses">,
    # 7 "Staff">,
    # 8 "BTR">

    try:
        # Создаем тикет в Redmine
        issue = redmine.issue.get(
            resource_id = resource_id,
        )
        print(f"Тикет '{issue.id}' успешно прочитан! ID: {issue.custom_fields[0]}")
        print(issue.custom_fields[2]["value"])

    except Exception as e:
        print(f"Ошибка при чтении тикета: {e}")

#read_redmine_ticket(85164)

create_redmine_ticket("new-models", "Test", "Test_task")