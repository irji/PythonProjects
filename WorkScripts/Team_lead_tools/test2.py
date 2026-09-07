import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans
from collections import Counter
import matplotlib.pyplot as plt

# 1. Загрузка данных из CSV файла (замените 'tickets.csv' на реальное имя файла)
try:
    df = pd.read_csv('D:\\Task_priority_GUI_MD_SIM_26.4.csv', encoding='utf-8')
except Exception as e:
    # Если файл не найден, создаем пример с данными из цитат
    print("Файл не найден. Используем примерные данные для демонстрации.")
    
    data = [
        ["", "", "", "150633", "MD. При импорте проекта c кл. словом SLAVES, слейв-проекты в MD называются именем подключаемых data-файлов, а не согласно первому параметру в кл. слове SLAVES", "3", "", "Новая", "Ризванов Альберт", "Воробьев Алексей", "", "Model Designer", "", "GUI", "", "Да", "Тикет", "150633"],
        ["", "", "", "148027", "ДМ. Block Info - не обновляется параметр(свойство для оси) в режиме кроссплота пока не сдвинешь слайдер временных шагов", "4", "", "Новая", "Ха Алексей", "Воронкин Дмитрий", "", "Model Designer", "", "GUI", "", "Да", "Тикет", "148027"],
        ["", "", "", "150444", "MD: трап при удалении строчек из таблицы добычи скважин", "3", "", "Новая", "Садовников Роман", "Воронкин Дмитрий", "", "Model Designer", "", "GUI", "", "Да", "Тикет", "150444"],
        ["", "", "", "41898", "Удаление кода больше не нужного в новых компиляторах", "2", "", "Отложена", "Семушин Сергей", "Телишев Алексей", "", "Model Designer", "", "GUI", "", "Да", "Тикет", "41898"],
        ["", "", "", "41894", "Попробовать убрать зависимость модуля sim_objects от модулей gt", "2", "", "Отложена", "Семушин Сергей", "Глазкова Екатерина", "", "Model Designer", "", "GUI", "", "Да", "Тикет", "41894"],
        ["", "", "", "41666", "Генерить на лету словарь переменных в воркфлоу для передачи в расчеты", "3", "", "Новая", "Калинин Никита", "Калинин Никита", "", "Model Designer", "", "GUI", "", "Да", "Тикет", "41666"],
        ["", "", "", "41322", "Описать на devdocs кратко использование span", "2", "", "Новая", "Семушин Сергей", "Глазкова Екатерина", "", "Model Designer", "", "GUI", "", "Да", "Тикет", "41322"],
        ["", "", "", "76483", "Не записывается TNAVCTRL с флагом формата E3", "4", "", "Новая", "Калинин Олег", "Васильев Дмитрий", "", "Model Designer", "", "GUI", "", "Да", "Тикет", "76483"],
        ["", "", "", "59194", "Некорректно отображается имя результата в названии графика в настройках шаблона графиков", "3", "", "Новая", "Парфенова Анастасия", "Воронкин Дмитрий", "", "Model Designer", "", "GUI", "", "Да", "Тикет", "59194"],
        ["", "", "", "56986", "попадание в дебаг паузу при вставке таблицы из LibreOffice в таблицу ГРП", "3", "", "Новая", "Петров Никита", "Воробьев Алексей", "", "Model Designer", "", "GUI", "", "Да", "Тикет", "56986"],
        ["", "", "", "56822", "Написать тест для  #56723 (результаты в ND при расчете модели в очереди)", "2", "", "Новая", "Семушин Сергей", "Березин Александр", "", "Model Designer", "", "GUI", "", "Да", "Тикет", "56822"]
    ]
    
    columns = ["col1", "col2", "col3", "col4", "description", "col6", "col7", "col8", "col9", "col10", "col11", "col12", "col13", "col14", "col15", "col16", "col17", "col18"]
    df = pd.DataFrame(data, columns=columns)

# 2. Определение колонки с темами обращений
# Ищем колонку с описанием/темой
theme_columns = [col for col in df.columns if 'desc' in col.lower() or 'theme' in col.lower() or 'title' in col.lower() or 'name' in col.lower()]
if theme_columns:
    theme_col = theme_columns[0]
else:
    # Если нет явных колонок темы, используем последнюю колонку (предположительно описание)
    theme_col = df.columns[-1]

df['theme'] = df[theme_col]

# Удаление строк с пустыми темами
df = df[df['theme'].notna() & (df['theme'] != '')]
print(f"Количество строк после фильтрации: {len(df)}")

# 3. TF-IDF векторизация
vectorizer = TfidfVectorizer(
    max_features=1000,
    stop_words='russian',
    ngram_range=(1, 2)
)

X = vectorizer.fit_transform(df['theme'])

# 4. Кластеризация KMeans для получения 15 категорий
num_clusters = 15
kmeans = KMeans(n_clusters=num_clusters, random_state=42, n_init=10)
clusters = kmeans.fit_predict(X)

# Создание четких, непересекающихся категорий (на русском языке)
categories = [
    "Ошибки в интерфейсе",
    "Работа с проектами и данными",
    "Визуализация и графики",
    "Системные ошибки",
    "Коллективная работа",
    "Управление моделями",
    "Интеграция и связи",
    "Создание фильтров",
    "Ошибки в логах",
    "Тестирование и пакеты",
    "Сводные тикеты",
    "Проблемы с единицами измерения",
    "Работа с пользователями",
    "Инструменты разработки",
    "Другое / Прочее"



    Ошибки в интерфейсе (GUI)	5	26.3%
Некорректное отображение данных	3	15.8%
Проблемы с импортом/экспортом моделей	1	5.3%
Технические ошибки / Баги	2	10.5%
Работа с графиками и данными (PLT/RFT)	1	5.3%
Ошибки при работе с перфорациями	1	5.3%
Проблемы с отображением вкладок и элементов	1	5.3%
Работа с проектами и файлами	2	10.5%
Взаимодействие с системой (User Projects)	2	10.5%
Ошибки при смене шага / настройках	1	5.3%
Работа с единицами измерения	1	5.3%
Проблемы с памятью и производительностью	1	5.3%
Отладка / Логирование	1	5.3%
]

# Присвоение категорий
df['category'] = [categories[cluster] for cluster in clusters]

# 5. Сводная таблица
category_counts = df['category'].value_counts()
category_stats = pd.DataFrame({
    'Категория': category_counts.index,
    'Количество тикетов': category_counts.values,
    'Доля в % от общего объема': round((category_counts / len(df)) * 100, 2)
})

print("\nСводная таблица:")
print(category_stats.to_string(index=False))

# 6. Визуализация
plt.figure(figsize=(12, 6))
bars = plt.bar(range(len(category_counts)), category_counts.values, color='skyblue')
plt.xlabel('Категории')
plt.ylabel('Количество тикетов')
plt.title('Распределение тикетов по категориям')
plt.xticks(range(len(category_counts)), category_counts.index, rotation=45, ha='right')

# Добавление значений над столбцами
for i, (bar, count) in enumerate(zip(bars, category_counts.values)):
    plt.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.1,
             str(count), ha='center', va='bottom')

plt.tight_layout()
plt.show()

# 7. Сохранение результата
df.to_excel('categorized_tickets.xlsx', index=False)
print("\nФайл сохранен как categorized_tickets.xlsx")

# Вывод примеров категорий
print("\nПримеры распределения по категориям:")
for cat in categories[:5]:  # Показываем первые 5 категорий
    count = category_counts.get(cat, 0)
    print(f"- {cat}: {count} тикетов")
