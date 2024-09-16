from redminelib import Redmine

# Конфигурация Redmine
redmine_url = 'https://redmine.rfdyn.ru'  # URL вашего Redmine
api_key = '401a6b058962fbd1063c570fb0a1f99361c7e9b3'  # Ваш API Access Key

# Создание экземпляра Redmine
redmine = Redmine(redmine_url, key=api_key)

# Функция для создания тикета в Redmine
def create_redmine_ticket(project_id, subject, description, parrent_task_id, image_file=None):
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
            parent_issue_id=98636,
            #uploads=uploads,
            custom_fields=[{'id': 47, 'value': 'Нет'}, {'id': 2, 'value': 'Model Designer'}]
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

    try:
        # Создаем тикет в Redmine
        issue = redmine.issue.get(
            resource_id = resource_id,
        )
        print(f"Тикет '{issue.id}' успешно прочитан! ID: {issue.custom_fields[0]}")
        print(issue.custom_fields[2]["value"])

    except Exception as e:
        print(f"Ошибка при чтении тикета: {e}")

read_redmine_ticket(85164)

#create_redmine_ticket("new-models", "Test", "Test_task", 98636)