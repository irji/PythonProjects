from redminelib import Redmine
import datetime
from time import sleep

user_list = {114: ["Костин Георгий", 0],
176: ["Воробьев Константин", 0],
420: ["Цветкова Полина", 0],
451: ["Непотасов Герман", 0],
562: ["Бевзенко Дмитрий", 0],
174: ["Федяева Ольга", 0],
173: ["Клийменко Дмитрий", 0],
300: ["Корюзлов Павел", 0],
124: ["Спиридонов Андрей", 0],
115: ["Тимошенко Александр", 0],
602: ["Хатмуллина Айгуль", 0],
613: ["Аль-Кебси Ахмед Али Мохаммед Абдулла", 0]}

redmine = Redmine('https://redmine.rfdyn.ru', key="401a6b058962fbd1063c570fb0a1f99361c7e9b3")

start_date = datetime.date(2026, 7, 1) #26.06.2026
end_date = datetime.date(2026, 7, 20)

#issues = redmine.issue.filter(query_id='3245')
#issues = redmine.query.get(3245)
#issues = redmine.issue.get("144593")

# https://redmine.rfdyn.ru/projects/group-gui/issues?utf8=%E2%9C%93&op%5Bclosed_on%5D=%3E%3C&v%5Bclosed_on%5D%5B%5D=2026-07-01&v%5Bclosed_on%5D%5B%5D=2026-07-20
# https://redmine.rfdyn.ru/projects/group-gui/issues?utf8=%E2%9C%93&op[closed_on]=><&v[closed_on][]=2026-07-01&v[closed_on][]=2026-07-20

# Фильтр по статусу "Закрыт"
closed_status_id = 5

# Получаем тикеты
all_issues = redmine.issue.filter(
    status_id=closed_status_id,
    closed_on=f'><{start_date.strftime("%Y-%m-%d")}|{end_date.strftime("%Y-%m-%d")}',
    include='journals'
)

print(f"Найдено закрытых тикетов: {len(all_issues)}\n")

# === По журналу изменений (точный способ — кто реально закрыл) ===
for issue in all_issues:

    sleep(1)

    # Получаем детальную информацию о тикете с журналом
    detailed_issue = redmine.issue.get(issue.id, include='journals')
    is_closed = False
    
    # Ищем запись в журнале о смене статуса на "Закрыт"
    for journal in getattr(detailed_issue, 'journals', []):
        if is_closed == False:
            for detail in getattr(journal, 'details', []):
                if (detail.get('name') == 'status_id' and str(detail.get('new_value')) == '5'): # ID статуса "Закрыт"
                    if journal.user.id in user_list:
                        print("{}:{}".format(issue.id, journal.user.name))
                        user_list[journal.user.id][1] = int(user_list[journal.user.id][1]) + 1
                        is_closed = True
                        break
                    else:
                        is_closed = True
                        break
                else:
                    if is_closed == True:
                        break
                    else:
                        continue
        else:
            break

for value in user_list.values():
    print("{}:{}".format(value[0], value[1]))
