import numpy as np
import pandas as pd
from sentence_transformers import SentenceTransformer
from sklearn.cluster import MiniBatchKMeans
from sklearn.metrics import silhouette_score
import matplotlib.pyplot as plt
from collections import Counter
import re

def extract_keywords(tasks, n_keywords=5):
    """Извлеките ключевые слова из набора задач"""
    all_words = []
    
    for task in tasks:
        # Очистите текст
        words = re.findall(r'\w+', task.lower())
        # Отфильтруйте стоп-слова
        stop_words = {'и', 'или', 'в', 'на', 'для', 'по', 'с', 'из', 'к', 'как', 
                      'что', 'это', 'всё', 'все', 'так', 'вам', 'вас', 'уже', 'но'}
        words = [w for w in words if w not in stop_words and len(w) > 2]
        all_words.extend(words)
    
    # Найдите самые частые слова
    most_common = Counter(all_words).most_common(n_keywords)
    return [word for word, _ in most_common]

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
model = SentenceTransformer('paraphrase-multilingual-mpnet-base-v2')

#model.to('cuda')  # Если есть GPU

embeddings = model.encode(
    tasks,
    batch_size=128,
    show_progress_bar=True,
    convert_to_numpy=True
)
print(f"✓ Embeddings созданы: форма {embeddings.shape}")

# 3. НАЙДИТЕ ОПТИМУМ В ДИАПАЗОНЕ 10-20
print("\n► Поиск оптимального количества кластеров (10-20)...")

silhouette_scores = {}

for n_clusters in range(10, 21):
    kmeans = MiniBatchKMeans(
        n_clusters=n_clusters,
        random_state=42,
        batch_size=256,
        n_init=10
    )
    labels = kmeans.fit_predict(embeddings)
    silhouette = silhouette_score(embeddings, labels)
    silhouette_scores[n_clusters] = silhouette
    
    print(f"  n_clusters={n_clusters}: silhouette={silhouette:.4f}")

optimal_clusters = max(silhouette_scores, key=silhouette_scores.get)
print(f"\n✓ Оптимально: {optimal_clusters} кластеров")

# 4. ФИНАЛЬНАЯ КЛАСТЕРИЗАЦИЯ
print(f"\n► Финальная кластеризация с {optimal_clusters} кластерами...")

kmeans_final = MiniBatchKMeans(
    n_clusters=optimal_clusters,
    random_state=42,
    batch_size=256,
    n_init=20
)
cluster_labels = kmeans_final.fit_predict(embeddings)
print("✓ Кластеризация завершена")

# 5. СОЗДАЙТЕ РЕЗУЛЬТИРУЮЩИЙ ДАТАФРЕЙМ С ИСХОДНЫМИ ДАННЫМИ
results_df = pd.DataFrame({
    task_id_column: original_df[task_id_column],  # Номер задачи
    task_text_column: original_df[task_text_column],  # Исходный текст задачи
    'cluster': cluster_labels  # Номер кластера
})

# Сортируйте по номеру кластера для удобства
results_df = results_df.sort_values('cluster')

# Сохраните результаты
results_df.to_csv('D:\\Tasks\\clustered_tasks.csv', index=False)
print("✓ Результаты сохранены: clustered_tasks.csv")

# 6. СТАТИСТИКА
print("\n" + "="*60)
print("СТАТИСТИКА КЛАСТЕРОВ")
print("="*60)

cluster_stats = results_df['cluster'].value_counts().sort_index()
for cluster_id, count in cluster_stats.items():
    print(f"Кластер {cluster_id}: {count} задач")

print(f"\nВсего: {len(results_df)} задач")





cluster_names = {}
for cluster_id in range(optimal_clusters):
    cluster_tasks = results_df[results_df['cluster'] == cluster_id]['тема'].tolist()
    
    keywords = extract_keywords(cluster_tasks, n_keywords=3)
    cluster_names[cluster_id] = ", ".join(keywords)
    
    print(f"Кластер {cluster_id}: {cluster_names[cluster_id]}")

# Добавьте имена в итоговый датафрейм
results_df['cluster_name'] = results_df['cluster'].map(cluster_names)
results_df.to_csv('D:\\Tasks\\clustered_tasks_with_names.csv', index=False)

