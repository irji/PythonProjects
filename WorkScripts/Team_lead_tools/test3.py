import numpy as np
import pandas as pd
from sentence_transformers import SentenceTransformer
from sklearn.cluster import MiniBatchKMeans
from sklearn.metrics import silhouette_score

# 1. ЗАГРУЗИТЕ ЗАДАЧИ
tasks_df = pd.read_csv('D:\\Tasks\\Task_priority_GUI_MD_SIM_26.4_full.csv', sep=";")  # или другой источник
tasks = tasks_df['тема'].tolist()
print(f"✓ Загружено {len(tasks)} задач")

# Сохраните все исходные колонки
original_df = tasks_df.copy()

# Предположим, что текст задачи во второй колонке 
# (первая - номер, вторая - описание)
# Если названия колонок другие, измените здесь:
task_id_column = tasks_df.columns[0]  # Первая колонка (номер задачи)
task_text_column = tasks_df.columns[1]  # Вторая колонка (текст задачи)

print(f"ID колонка: '{task_id_column}'")
print(f"Текст колонка: '{task_text_column}'")

tasks = tasks_df[task_text_column].tolist()

# 2. СОЗДАЙТЕ EMBEDDINGS
print("\n► Создание embeddings...")
# Быстрая, лёгкая (рекомендуется)
#model = SentenceTransformer('paraphrase-multilingual-MiniLM-L12-v2')
# Более мощная, но медленнее
model = SentenceTransformer('all-MiniLM-L6-v2')

#model.to('cuda')  # Если есть GPU
embeddings = model.encode(tasks, batch_size=256, show_progress_bar=True, convert_to_numpy=True)

kmeans = MiniBatchKMeans(n_clusters=11, random_state=42, batch_size=256, n_init=20)
cluster_labels = kmeans.fit_predict(embeddings)

embeddings = model.encode(
    tasks,
    batch_size=128,
    show_progress_bar=True,
    convert_to_numpy=True
)
print(f"✓ Embeddings созданы: форма {embeddings.shape}")

# 3. СОЗДАЙТЕ СЛОВАРЬ НАЗВАНИЙ КЛАСТЕРОВ
cluster_names = {
    0: "Расчеты и моделирование",
    1: "Интерфейс и GUI",
    2: "Импорт и экспорт данных",
    3: "Визуализация результатов",
    4: "Управление кейсами",
    5: "Работа со скважинами",
    6: "Совместная работа",
    7: "Системные логи и ошибки",
    8: "Настройки и свойства",
    9: "Оптимизация и производительностька",
    10: "Прочее",
}

# # 3. НАЙДИТЕ ОПТИМУМ В ДИАПАЗОНЕ 10-30
# print("\n► Поиск оптимального количества кластеров (10-30)...")

# silhouette_scores = {}

# for n_clusters in range(10, 31):
#     kmeans = MiniBatchKMeans(
#         n_clusters=n_clusters,
#         random_state=42,
#         batch_size=256,
#         n_init=10
#     )
#     labels = kmeans.fit_predict(embeddings)
#     silhouette = silhouette_score(embeddings, labels)
#     silhouette_scores[n_clusters] = silhouette
    
#     print(f"  n_clusters={n_clusters}: silhouette={silhouette:.4f}")

# optimal_clusters = max(silhouette_scores, key=silhouette_scores.get)
# print(f"\n✓ Оптимально: {optimal_clusters} кластеров")

# # 4. ФИНАЛЬНАЯ КЛАСТЕРИЗАЦИЯ
# print(f"\n► Финальная кластеризация с {optimal_clusters} кластерами...")

kmeans_final = MiniBatchKMeans(
    #n_clusters=optimal_clusters,
    n_clusters=11,
    random_state=42,
    batch_size=256,
    n_init=20
)
cluster_labels = kmeans_final.fit_predict(embeddings)
print("✓ Кластеризация завершена")

# 5. СОЗДАЙТЕ РЕЗУЛЬТИРУЮЩИЙ ДАТАФРЕЙМ С ИСХОДНЫМИ ДАННЫМИ
results_df = pd.DataFrame({
    task_id_column: original_df[task_id_column],
    task_text_column: original_df[task_text_column],
    'cluster_id': cluster_labels,
    'cluster_name': [cluster_names.get(label, f'Кластер {label}') for label in cluster_labels]
})

# Сортируйте по номеру кластера для удобства
results_df = results_df.sort_values('cluster_id')

# Сохраните результаты
results_df.to_csv('D:\\Tasks\\clustered_tasks.csv', index=False)
print("✓ Результаты сохранены: clustered_tasks.csv")

# 6. СТАТИСТИКА
print("\n" + "="*60)
print("СТАТИСТИКА КЛАСТЕРОВ")
print("="*60)

cluster_stats = results_df['cluster_name'].value_counts().sort_index()
for cluster_id, count in cluster_stats.items():
    print(f"Кластер {cluster_id}: {count} задач")

print(f"\nВсего: {len(results_df)} задач")
