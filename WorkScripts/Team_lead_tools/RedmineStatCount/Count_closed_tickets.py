from redminelib import Redmine
import datetime
from time import sleep

# Костин Георгий Александрович    114
# Воробьев Константин Валерьевич  176
# Цветкова Полина Александровна   420
# Непотасов Герман Вячеславович   451
# Бевзенко Дмитрий Андреевич      592
# Федяева Ольга Александровна     174
# Клийменко Дмитрий Владимирович  173
# Корюзлов Павел Сергеевич        300
# Спиридонов Андрей Васильевич    124
# Тимошенко Александр Анатольевич 115
# Хатмуллина Айгуль Ильдусовна    620
# Аль-Кебси Ахмед Али Мохаммед    613

redmine = Redmine('https://redmine.rfdyn.ru', key="401a6b058962fbd1063c570fb0a1f99361c7e9b3")

start_date = datetime.date(2026, 7, 1)
end_date = datetime.date(2026, 7, 20)

#issues = redmine.issue.filter(query_id='3245')
#issues = redmine.query.get(3245)
#issues = redmine.issue.get("144593")

# https://redmine.rfdyn.ru/projects/group-gui/issues?utf8=%E2%9C%93&op%5Bclosed_on%5D=%3E%3C&v%5Bclosed_on%5D%5B%5D=2026-07-01&v%5Bclosed_on%5D%5B%5D=2026-07-20
# https://redmine.rfdyn.ru/projects/group-gui/issues?utf8=%E2%9C%93&op[closed_on]=><&v[closed_on][]=2026-07-01&v[closed_on][]=2026-07-20

# Фильтр по статусу "Закрыт" (ID зависит от вашей конфигурации Redmine)
# Обычно статус "Закрыт" имеет ID 5, но проверьте в настройках
closed_status_id = 5

# ID пользователя, чьи закрытия считаем
TARGET_USER_ID = 174

# Получаем тикеты
all_issues = redmine.issue.filter(
    status_id=closed_status_id,
    closed_on=f'><{start_date.strftime("%Y-%m-%d")}|{end_date.strftime("%Y-%m-%d")}',
    include='journals'
)

print(f"Найдено закрытых тикетов: {len(all_issues)}\n")

# === Способ 2: По журналу изменений (точный способ — кто реально закрыл) ===
closed_by_user = []

for issue in all_issues:

    sleep(0.01)

    # Получаем детальную информацию о тикете с журналом
    detailed_issue = redmine.issue.get(issue.id, include='journals')
    
    # Ищем запись в журнале о смене статуса на "Закрыт"
    for journal in getattr(detailed_issue, 'journals', []):
        for detail in getattr(journal, 'details', []):
            if (detail.get('name') == 'status_id' and 
                str(detail.get('new_value')) == '5' and  # ID статуса "Закрыт"
                journal.user.id == TARGET_USER_ID):
                
                closed_by_user.append({
                    'id': issue.id,
                    'subject': issue.subject,
                    'closed_on': issue.closed_on,
                    'closed_by': journal.user.name,
                    'journal_date': journal.created_on
                })

                print(issue.id)
                break
        else:
            continue
        break

print(f"\nСпособ 2 (по журналу изменений): {len(closed_by_user)} тикетов реально закрыл пользователь #{TARGET_USER_ID}")
