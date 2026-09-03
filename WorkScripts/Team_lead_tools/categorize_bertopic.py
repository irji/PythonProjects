#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Автоматическая категоризация задач Redmine с помощью BERTopic
Для набора из 1348+ задач по моделированию добычи нефти и газа

Установка зависимостей:
    pip install bertopic sentence-transformers pandas

Запуск:
    python categorize_bertopic.py --input Task_priority_GUI_MD_SIM_26.4.csv --output categorized.csv  --nr-topics 15
"""

import argparse
import pandas as pd
import numpy as np
import re
import warnings
warnings.filterwarnings('ignore')

from bertopic import BERTopic
from sentence_transformers import SentenceTransformer
from sklearn.feature_extraction.text import CountVectorizer
from umap import UMAP
from hdbscan import HDBSCAN


# ==========================================
# 1. ПРЕДОБРАБОТКА
# ==========================================
RUSSIAN_STOPWORDS = {
    'с', 'в', 'на', 'по', 'из', 'для', 'не', 'при', 'под', 'за', 'о', 'от', 'до',
    'через', 'без', 'про', 'над', 'между', 'после', 'перед', 'во', 'со', 'ко',
    'и', 'а', 'но', 'или', 'да', 'как', 'что', 'чтобы', 'когда', 'где',
    'этот', 'такой', 'который', 'весь', 'все', 'быть', 'есть', 'иметь',
    'более', 'менее', 'очень', 'слишком', 'весьма', 'достаточно', 'почти',
    'только', 'лишь', 'даже', 'тоже', 'также', 'уже', 'ещё', 'еще',
}

TECH_STOPWORDS = {
    'тикет', 'bug', 'feature', 'task', 'issue', 'новая', 'в работе', 'закрыт',
    'отложена', 'на ревью', 'требует доработки', 'срочно', 'важно',
}


def preprocess_text(text):
    """Очистка тем тикетов для BERTopic"""
    if pd.isna(text):
        return ""

    text = str(text).lower()

    # Убираем технические артефакты Redmine
    text = re.sub(r'#[\w\-]+', ' ', text)           # #bug, #feature
    text = re.sub(r'\[.*?\]', ' ', text)            # [v2.5]
    text = re.sub(r'\(.*?\)', ' ', text)            # (срочно)
    text = re.sub(r'https?://\S+', ' ', text)       # ссылки
    text = re.sub(r'\b\d+\.?\d*\b', ' ', text)  # числа

    # Разделяем CamelCase
    text = re.sub(r'([a-z0-9])([A-Z])', r'\1 \2', text)

    # Убираем стоп-слова
    words = text.split()
    words = [w.strip('.,;:!?—-/\\') for w in words 
             if len(w) > 2 and w not in RUSSIAN_STOPWORDS and w not in TECH_STOPWORDS]

    return ' '.join(words)


# ==========================================
# 2. КАТЕГОРИЗАЦИЯ
# ==========================================
def categorize_with_bertopic(df, subject_col='Тема', description_col=None,
                              min_cluster_size=25, nr_topics='auto'):
    """
    Категоризация задач с помощью BERTopic

    Args:
        df: DataFrame с задачами
        subject_col: название колонки с темой
        description_col: название колонки с описанием (опционально)
        min_cluster_size: минимум задач в категории (~2% от 1348 = 27)
        nr_topics: 'auto' или число категорий

    Returns:
        DataFrame с колонками topic_id, category_name, topic_keywords
    """

    # Формируем текст для анализа
    if description_col and description_col in df.columns:
        df['text_for_model'] = df[subject_col].fillna('') + ' ' + df[description_col].fillna('')
    else:
        df['text_for_model'] = df[subject_col].fillna('')

    df['processed'] = df['text_for_model'].apply(preprocess_text)

    # Фильтруем слишком короткие
    valid_mask = df['processed'].str.len() > 5
    df_valid = df[valid_mask].copy()
    docs = df_valid['processed'].tolist()

    print(f"Документов после очистки: {len(docs)}")
    if len(docs) < min_cluster_size:
        raise ValueError(
            f"Слишком мало задач ({len(docs)}) для BERTopic. "
            f"Минимум: {min_cluster_size}. Используйте гибридный скрипт."
        )

    # Модель эмбеддингов (мультиязычная, понимает русский + англ. термины)
    print("Загрузка модели эмбеддингов...")
    embedding_model = SentenceTransformer('paraphrase-multilingual-MiniLM-L12-v2')

    # UMAP — снижение размерности
    umap_model = UMAP(
        n_neighbors=min(15, len(docs) // 10),
        n_components=5,
        min_dist=0.0,
        metric='cosine',
        random_state=42
    )

    # HDBSCAN — кластеризация
    hdbscan_model = HDBSCAN(
        min_cluster_size=min_cluster_size,
        min_samples=max(5, min_cluster_size // 5),
        metric='euclidean',
        cluster_selection_method='eom',
        prediction_data=True
    )

    # Vectorizer для ключевых слов на русском
    vectorizer_model = CountVectorizer(
        ngram_range=(1, 2),
        stop_words=list(RUSSIAN_STOPWORDS | TECH_STOPWORDS),
        min_df=2,
        max_df=1
    )

    # BERTopic
    print("Обучение BERTopic...")
    topic_model = BERTopic(
        embedding_model=embedding_model,
        umap_model=umap_model,
        hdbscan_model=hdbscan_model,
        vectorizer_model=vectorizer_model,
        nr_topics=nr_topics,
        top_n_words=10,
        calculate_probabilities=False,
        verbose=True
    )

    topics, _ = topic_model.fit_transform(docs)

    # Добавляем результаты
    df_valid = df_valid.reset_index(drop=True)
    df_valid['topic_id'] = topics

    # Формируем читаемые названия
    def get_topic_name(tid):
        if tid == -1:
            return "📂 Прочее / Не определено"
        words = topic_model.get_topic(tid)
        if words:
            return " | ".join([w[0] for w in words[:3]])
        return f"Тема {tid}"

    df_valid['category_bertopic'] = df_valid['topic_id'].apply(get_topic_name)

    # Ключевые слова для каждой задачи
    def get_keywords(tid):
        if tid == -1:
            return ""
        words = topic_model.get_topic(tid)
        return ", ".join([w[0] for w in words[:5]]) if words else ""

    df_valid['topic_keywords'] = df_valid['topic_id'].apply(get_keywords)

    # Сливаем обратно
    df_result = df.merge(
        df_valid[['topic_id', 'category_bertopic', 'topic_keywords']],
        left_index=True,
        right_index=True,
        how='left'
    )
    df_result['topic_id'] = df_result['topic_id'].fillna(-1).astype(int)
    df_result['category_bertopic'] = df_result['category_bertopic'].fillna("📂 Прочее / Не определено")

    return df_result, topic_model


# ==========================================
# 3. ОТЧЁТ
# ==========================================
def print_report(df):
    """Вывод сводки по категориям"""
    print(f"\n{'='*60}")
    print("ОБНАРУЖЕННЫЕ КАТЕГОРИИ:")
    print(f"{'='*60}")

    summary = df.groupby(['topic_id', 'category_bertopic']).size().reset_index(name='count')
    summary = summary.sort_values('count', ascending=False)

    for _, row in summary.iterrows():
        marker = "⚠️  " if row['topic_id'] == -1 else "📁 "
        print(f"{marker}[{row['topic_id']:>3}] {row['category_bertopic']:<45} ({row['count']} задач)")

    print(f"\nВсего категорий: {len(summary)}")

    # Примеры
    print(f"\n{'='*60}")
    print("ПРИМЕРЫ ЗАДАЧ ПО КАТЕГОРИЯМ:")
    print(f"{'='*60}")

    for tid in sorted(df['topic_id'].unique())[:10]:
        subset = df[df['topic_id'] == tid]
        cat = subset['category_bertopic'].iloc[0]
        print(f"\n--- {cat} ({len(subset)} задач) ---")
        for subj in subset[df.columns[0] if 'Тема' not in df.columns else 'Тема'].head(3):
            if pd.notna(subj):
                print(f"   • {str(subj)[:80]}...")


# ==========================================
# 4. MAIN
# ==========================================
def main():
    parser = argparse.ArgumentParser(description='Категоризация задач Redmine через BERTopic')
    parser.add_argument('--input', '-i', required=True, help='Входной CSV файл')
    parser.add_argument('--output', '-o', default='categorized_bertopic.csv', help='Выходной CSV')
    parser.add_argument('--subject-col', default='Тема', help='Колонка с темой тикета')
    parser.add_argument('--desc-col', default=None, help='Колонка с описанием (опционально)')
    parser.add_argument('--min-cluster', type=int, default=25, help='Мин. размер категории')
    parser.add_argument('--nr-topics', default='auto', help='Число категорий (auto или число)')

    args = parser.parse_args()

    # Чтение
    print(f"Чтение {args.input}...")
    df = pd.read_csv(args.input)
    print(f"Загружено задач: {len(df)}")

    # Категоризация
    nr_topics = int(args.nr_topics) if args.nr_topics != 'auto' else 'auto'
    df_result, model = categorize_with_bertopic(
        df,
        subject_col=args.subject_col,
        description_col=args.desc_col,
        min_cluster_size=args.min_cluster,
        nr_topics=nr_topics
    )

    # Сохранение
    df_result.to_csv(args.output, index=False, encoding='utf-8-sig')
    print(f"\n✅ Результат сохранён: {args.output}")

    # Отчёт
    print_report(df_result)


if __name__ == '__main__':
    main()
