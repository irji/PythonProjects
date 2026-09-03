#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Кластеризация задач Redmine с помощью BERTopic
Чтение из CSV, автоматическое определение тем, сохранение результатов
"""

import pandas as pd
import numpy as np
from bertopic import BERTopic
from sentence_transformers import SentenceTransformer
from sklearn.feature_extraction.text import CountVectorizer
from hdbscan import HDBSCAN
from umap import UMAP
import warnings
warnings.filterwarnings('ignore')


def load_issues(csv_path: str, text_column: str = "subject") -> pd.DataFrame:
    """Загружает задачи из CSV. Ожидает колонки: id, subject"""
    df = pd.read_csv(csv_path)
    
    # Если в CSV есть колонка 'description' — склеиваем с subject
    if 'description' in df.columns:
        df['text'] = df['subject'].fillna('') + ' ' + df['description'].fillna('')
    else:
        df['text'] = df[text_column].fillna('')
    
    # Удаляем дубликаты и пустые строки
    df = df.dropna(subset=['text'])
    df = df[df['text'].str.strip() != '']
    
    print(f"Загружено задач: {len(df)}")
    return df


def create_russian_stopwords() -> list:
    """Расширенный список русских стоп-слов для техтекста"""
    return [
        "и", "в", "во", "не", "что", "он", "на", "я", "с", "со", "как", "а", "то", "все",
        "она", "так", "его", "но", "да", "ты", "к", "у", "же", "вы", "за", "бы", "по",
        "только", "ее", "мне", "было", "вот", "от", "меня", "еще", "нет", "о", "из",
        "ему", "теперь", "когда", "даже", "ну", "вдруг", "ли", "если", "уже", "или",
        "ни", "быть", "был", "него", "до", "вас", "нибудь", "опять", "уж", "вам",
        "ведь", "там", "потом", "себя", "ничего", "ей", "может", "они", "тут", "где",
        "есть", "надо", "ней", "для", "мы", "тебя", "их", "чем", "была", "сам", "чтоб",
        "без", "будто", "чего", "раз", "тоже", "себе", "под", "будет", "ж", "тогда",
        "кто", "этот", "того", "потому", "этого", "какой", "совсем", "ним", "здесь",
        "этом", "один", "почти", "мой", "тем", "чтобы", "нее", "сейчас", "были", "куда",
        "зачем", "всех", "никогда", "можно", "при", "наконец", "два", "об", "другой",
        "хоть", "после", "над", "больше", "тот", "через", "эти", "нас", "про", "всего",
        "них", "какая", "много", "разве", "три", "эту", "моя", "впрочем", "хорошо",
        "свою", "этой", "перед", "иногда", "лучше", "чуть", "том", "нельзя", "такой",
        "им", "более", "всегда", "конечно", "всю", "между",
        # Технические стоп-слова, которые не несут смысловой нагрузки
        "ошибка", "исправить", "добавить", "проблема", "необходимо", "требуется",
        "сделать", "реализовать", "обновить", "удалить", "изменить"
    ]


def run_bertopic_clustering(
    df: pd.DataFrame,
    n_topics: str = "auto",
    min_topic_size: int = 15,
    device: str = "cpu"
) -> tuple[BERTopic, pd.DataFrame]:
    """
    Основная функция кластеризации
    
    Args:
        df: DataFrame с колонкой 'text'
        n_topics: "auto" для автоматического определения, или число
        min_topic_size: минимальное число документов в теме
        device: "cpu" или "cuda" (если есть GPU)
    """
    
    docs = df['text'].tolist()
    
    # 1. Модель эмбеддингов
    # Для русского техтекста лучше всего paraphrase-multilingual-MiniLM-L12-v2
    # Если есть GPU — можно использовать 'intfloat/multilingual-e5-large'
    print("Загрузка модели эмбеддингов...")
    embedding_model = SentenceTransformer(
        'paraphrase-multilingual-MiniLM-L12-v2',
        device=device
    )
    
    # 2. UMAP для снижения размерности
    # Настройки для техтекста: больше n_neighbors = более глобальная структура
    umap_model = UMAP(
        n_neighbors=15,
        n_components=5,
        min_dist=0.0,
        metric='cosine',
        random_state=42
    )
    
    # 3. HDBSCAN для кластеризации
    # min_cluster_size зависит от размера датасета
    hdbscan_model = HDBSCAN(
        min_cluster_size=min_topic_size,
        metric='euclidean',
        cluster_selection_method='eom',
        prediction_data=True
    )
    
    # 4. Векторизатор для извлечения ключевых слов
    # Используем биграммы для лучшего захвата технических терминов
    stopwords = create_russian_stopwords()
    vectorizer_model = CountVectorizer(
        stop_words=stopwords,
        ngram_range=(1, 2),      # униграммы + биграммы
        min_df=2,                # игнорировать редкие термины
        max_df=0.8               # игнорировать слишком частые
    )
    
    # 5. Инициализация BERTopic
    topic_model = BERTopic(
        embedding_model=embedding_model,
        umap_model=umap_model,
        hdbscan_model=hdbscan_model,
        vectorizer_model=vectorizer_model,
        
        # Параметры тем
        nr_topics=n_topics,           # "auto" объединяет похожие темы
        min_topic_size=min_topic_size,
        
        # Вычисления
        calculate_probabilities=False,  # True очень медленно на CPU для 1348 задач
        verbose=True
    )
    
    # 6. Обучение
    print("Кластеризация задач...")
    topics, _ = topic_model.fit_transform(docs)
    
    # 7. Добавляем результаты в DataFrame
    df['topic_id'] = topics
    
    # Получаем читаемые названия тем
    topic_info = topic_model.get_topic_info()
    id_to_name = dict(zip(topic_info['Topic'], topic_info['Name']))
    df['topic_name'] = df['topic_id'].map(lambda x: id_to_name.get(x, '❌ Outlier'))
    
    return topic_model, df


def analyze_results(topic_model: BERTopic, df: pd.DataFrame, output_dir: str = "."):
    """Анализ и сохранение результатов"""
    
    # Статистика по темам
    stats = df['topic_name'].value_counts()
    n_outliers = (df['topic_id'] == -1).sum()
    
    print(f"\n{'='*60}")
    print("РЕЗУЛЬТАТЫ КЛАСТЕРИЗАЦИИ")
    print(f"{'='*60}")
    print(f"Всего задач: {len(df)}")
    print(f"Найдено тем: {len(stats) - (1 if n_outliers > 0 else 0)}")
    print(f"Outliers (без темы): {n_outliers} ({n_outliers/len(df)*100:.1f}%)")
    print(f"\nРаспределение по темам:")
    print(stats.to_string())
    
    # Ключевые слова по темам
    print(f"\n{'='*60}")
    print("КЛЮЧЕВЫЕ СЛОВА ПО ТЕМАМ")
    print(f"{'='*60}")
    
    for topic_id in sorted(df['topic_id'].unique()):
        if topic_id == -1:
            continue
        keywords = topic_model.get_topic(topic_id)
        if keywords:
            kw_str = ", ".join([f"{word}({score:.3f})" for word, score in keywords[:5]])
            topic_name = df[df['topic_id'] == topic_id]['topic_name'].iloc[0]
            print(f"\nТема {topic_id}: {topic_name}")
            print(f"  Ключевые слова: {kw_str}")
    
    # Сохранение результатов
    output_csv = f"{output_dir}/issues_with_topics.csv"
    df.to_csv(output_csv, index=False, encoding='utf-8-sig')
    print(f"\n💾 Результаты сохранены: {output_csv}")
    
    # Сохранение иерархии тем (если нужно детальнее разбить)
    hierarchy = topic_model.hierarchical_topics(df['text'].tolist())
    if len(hierarchy) > 0:
        hierarchy.to_csv(f"{output_dir}/topic_hierarchy.csv", index=False, encoding='utf-8-sig')
    
    # Визуализация (опционально, требует plotly)
    try:
        fig = topic_model.visualize_topics()
        fig.write_html(f"{output_dir}/topic_visualization.html")
        print(f"💾 Визуализация: {output_dir}/topic_visualization.html")
    except Exception as e:
        print(f"Визуализация пропущена: {e}")
    
    return stats


def interactive_topic_merge(topic_model: BERTopic, df: pd.DataFrame):
    """
    Интерактивное объединение похожих тем после первичного анализа
    """
    print(f"\n{'='*60}")
    print("ИНТЕРАКТИВНОЕ ОБЪЕДИНЕНИЕ ТЕМ")
    print(f"{'='*60}")
    print("Если темы похожи, введите ID тем для объединения через пробел.")
    print("Например: '3 7' объединит темы 3 и 7")
    print("Пустая строка — завершить")
    
    while True:
        user_input = input("> ").strip()
        if not user_input:
            break
        try:
            topics_to_merge = [int(x) for x in user_input.split()]
            if len(topics_to_merge) >= 2:
                topic_model.merge_topics(df['text'].tolist(), topics_to_merge)
                print(f"✅ Темы {topics_to_merge} объединены")
        except Exception as e:
            print(f"Ошибка: {e}")


def main():
    # === НАСТРОЙКИ ===
    CSV_PATH = "D:\\Task_priority_GUI_MD_SIM_26.4.csv"          # путь к вашему CSV
    TEXT_COLUMN = "Тема"                   # колонка с темой тикета
    OUTPUT_DIR = "D:\\0000_result"                   # куда сохранять
    MIN_TOPIC_SIZE = 15                       # мин. размер темы (для 1348 задач 15-25 оптимально)
    DEVICE = "cpu"                            # или "cuda" если есть GPU
    
    import os
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    
    # 1. Загрузка
    df = load_issues(CSV_PATH, TEXT_COLUMN)
    
    # 2. Кластеризация
    topic_model, df = run_bertopic_clustering(
        df,
        n_topics="auto",
        min_topic_size=MIN_TOPIC_SIZE,
        device=DEVICE
    )
    
    # 3. Анализ
    stats = analyze_results(topic_model, df, OUTPUT_DIR)
    
    # 4. Примеры задач по каждой теме
    print(f"\n{'='*60}")
    print("ПРИМЕРЫ ЗАДАЧ ПО ТЕМАМ")
    print(f"{'='*60}")
    for topic_id in sorted(df['topic_id'].unique()):
        if topic_id == -1:
            continue
        sample = df[df['topic_id'] == topic_id].head(3)
        topic_name = sample['topic_name'].iloc[0]
        print(f"\n--- Тема {topic_id}: {topic_name} ---")
        for _, row in sample.iterrows():
            print(f"  #{row['id']}: {row['text'][:80]}...")
    
    # 5. Интерактивное объединение (опционально)
    # interactive_topic_merge(topic_model, df)


if __name__ == "__main__":
    main()