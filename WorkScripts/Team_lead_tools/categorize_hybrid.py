#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Гибридная категоризация задач Redmine:
1. Сначала применяются предметно-ориентированные правила (точно)
2. Затем BERTopic для оставшихся неопределённых задач

Установка:
    pip install bertopic sentence-transformers pandas

Запуск:
    python categorize_hybrid.py --input tasks.csv --output categorized.csv
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
# 1. ПРАВИЛА КАТЕГОРИЗАЦИИ (предметная область ННГ)
# ==========================================
RULES = [
    # GUI / Интерфейс / Визуализация
    ("🎨 GUI / Интерфейс / Визуализация", [
        'gui', 'кисточк', 'окно', 'вкладк', 'график', 'шаблон', 'отображени',
        'обновляются', 'auto-title', 'title', 'визуализация', 'рендеринг',
        'кнопк', 'меню', 'диалог', 'скролл', 'прокрутк', 'tooltip', 'иконк',
        'torque', 'torque 3d', '3d визуализация', 'цветовая шкала', 'легенда',
        'панель', 'toolbar', 'widget', 'drag', 'drop', 'hover', 'click',
        'chart', 'plot', 'canvas', 'viewport', 'camera', 'lighting',
    ]),

    # Импорт / Экспорт / Файлы / Форматы
    ("📥 Импорт / Экспорт / Файлы / Форматы", [
        'импорт', 'экспорт', 'загрузить', 'зачитываются', 'файл', 'sln', 'slg',
        'eclipse', 'cmg', 'petrel', 'rms', 'tnav', 'tnavigator', 'дренирования',
        'рестарт', 'restart', 'copy', 'сохранен', 'save', 'copy as',
        'импорта рестартной', 'копированием результатов', 'отсутствуют свойства',
        'конвертация', 'экспортировать', 'импортировать', 'загрузка', 'выгрузка',
        'формат', 'extension', 'file', 'read', 'write', 'parse', 'serialize',
        'grdecl', 'grid', 'init', 'restart', 'summary', 'unrst', 'unsmry',
    ]),

    # Расчёт / Workflow / Скважины
    ("⚙️ Расчёт / Workflow / Скважины", [
        'расчёт', 'расчета', 'расчет', 'workflow', 'траектории', 'скважин',
        'запуске', 'simgui', 'отличается', 'регион', 'satnum', 'regionproperty',
        'инициализация', 'пересчитываются', 'подключенным workflow',
        'гидродинамическ', 'дебит', 'давлени', 'заводнени', 'конусообразовани',
        'материальный баланс', 'относительные фазовые проницаемости',
        'well', 'wellbore', 'trajectory', 'calculation', 'simulation',
        'run', 'solver', 'convergence', 'iteration', 'timestep', 'cfl',
        'pressure', 'rate', 'production', 'injection', 'aquifer', 'pvt',
        'aquifer', 'boundary', 'source', 'sink', 'schedule', 'control',
    ]),

    # Геомоделирование / Дизайнер / Структура
    ("🗺️ Геомоделирование / Дизайнер / Структура", [
        'дизайнер моделей', 'model designer', 'reservoir coupling', 'геологическ',
        'структурная карта', 'изопахит', 'литолог', 'фаци', 'корреляция пластов',
        'калибровка', 'интерполяция', 'kriging', 'объем нефтенасыщенного',
        'сейсморазведк', 'горизонт', 'пласт', 'formation', 'layer', 'zone',
        'geology', 'structural', 'facies', 'porosity', 'permeability', 'saturation',
        'net-to-gross', 'ntg', 'volume', 'contact', 'owc', 'goc', 'woc',
        'upscaling', 'downscaling', 'geostatistics', 'variogram', 'correlation',
    ]),

    # Сеточная генерация / Гриды
    ("🔲 Сеточная генерация / Гриды", [
        'сетк', 'pebi', 'структурированная', 'неструктурированная', 'ячейк',
        'сгущение', 'адаптация', 'разлом', 'ортогональность', 'skewness',
        'качество сетки', 'перестроение сетки', 'grid', 'mesh', 'cell',
        'corner point', 'cpg', 'cartesian', 'radial', 'local grid refinement',
        'lgr', 'pinchout', 'truncation', 'fault', 'throw', 'heave',
    ]),

    # Оптимизация / Производительность
    ("🚀 Оптимизация / Производительность", [
        'торможение', 'задержк', 'медленно', 'оптимизация', 'ускорить',
        'производительность', 'параллелизация', 'кэширование', 'профилирование',
        'узкие места', 'время загрузки', 'утечка памяти', 'memory leak',
        'performance', 'slow', 'lag', 'freeze', 'hang', 'crash', 'speed',
        'accelerate', 'optimize', 'cache', 'parallel', 'mpi', 'openmp', 'gpu',
        'cuda', 'vectorize', 'simd', 'bottleneck', 'profil', 'benchmark',
    ]),

    # AHM / Адаптивная история моделирования
    ("📊 AHM / Адаптивная история моделирования", [
        'ahm', 'mba', 'adaptive', 'history match', 'history matching',
        'assisted history matching', 'ensemble', 'kalman filter', 'enkf',
        'optimization', 'objective function', 'mismatch', 'sensitivity',
    ]),

    # Тестирование / QA
    ("🧪 Тестирование / QA", [
        'тест', 'unit-test', 'интеграционные', 'регрессионное', 'нагрузочное',
        'падающий тест', 'покрытие кода', 'валидация', 'test', 'testing',
        'qa', 'quality assurance', 'regression', 'integration', 'unit test',
        'assert', 'verify', 'validate', 'check', 'inspect', 'review',
    ]),

    # Инфраструктура / DevOps
    ("🔧 Инфраструктура / DevOps", [
        'ci/cd', 'docker', 'postgresql', 'бэкап', 'мониторинг', 'логирование',
        'сборка', 'лицензирование', 'доступ', 'прав', 'рол', 'infrastructure',
        'devops', 'jenkins', 'gitlab', 'github actions', 'kubernetes', 'k8s',
        'deploy', 'release', 'version', 'build', 'pipeline', 'artifact',
        'license', 'authorization', 'authentication', 'permission', 'role',
    ]),

    # Документация
    ("📚 Документация", [
        'документация', 'руководство', 'wiki', 'changelog', 'инструкция',
        'справка', 'faq', 'описание api', 'documentation', 'manual', 'guide',
        'readme', 'tutorial', 'help', 'reference', 'glossary', 'index',
    ]),
]


def categorize_by_rules(subject, module=''):
    """Категоризация по правилам. Возвращает категорию или None"""
    text = str(subject).lower() + ' ' + str(module).lower()

    for category, keywords in RULES:
        if any(kw in text for kw in keywords):
            return category

    return None


# ==========================================
# 2. ПРЕДОБРАБОТКА ДЛЯ BERTOPIC
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
    if pd.isna(text):
        return ""
    text = str(text).lower()
    text = re.sub(r'#[\w\-]+', ' ', text)
    text = re.sub(r'\[.*?\]', ' ', text)
    text = re.sub(r'\(.*?\)', ' ', text)
    text = re.sub(r'https?://\S+', ' ', text)
    text = re.sub(r'\b\d+\.?\d*\b', ' ', text)
    text = re.sub(r'([a-z0-9])([A-Z])', r'\1 \2', text)
    words = text.split()
    words = [w.strip('.,;:!?—-/\\') for w in words 
             if len(w) > 2 and w not in RUSSIAN_STOPWORDS and w not in TECH_STOPWORDS]
    return ' '.join(words)


# ==========================================
# 3. ГИБРИДНАЯ КАТЕГОРИЗАЦИЯ
# ==========================================
def categorize_hybrid(df, subject_col='Тема', module_col='Module',
                       min_cluster_size=25, nr_topics='auto'):
    """
    Двухэтапная категоризация:
    1. Правила для очевидных случаев
    2. BERTopic для остальных
    """

    # Этап 1: Правила
    print("Этап 1: Применение предметных правил...")
    df['category'] = df.apply(
        lambda row: categorize_by_rules(
            row.get(subject_col, ''),
            row.get(module_col, '') if module_col in row else ''
        ),
        axis=1
    )

    rule_matched = df['category'].notna().sum()
    print(f"  Распределено по правилам: {rule_matched} / {len(df)} ({rule_matched/len(df)*100:.1f}%)")

    # Этап 2: BERTopic для неопределённых
    undefined = df['category'].isna()
    undefined_count = undefined.sum()

    if undefined_count > 0 and undefined_count >= min_cluster_size:
        print(f"\nЭтап 2: BERTopic для {undefined_count} неопределённых задач...")

        df_undef = df[undefined].copy()
        df_undef['text_for_model'] = df_undef[subject_col].fillna('')
        df_undef['processed'] = df_undef['text_for_model'].apply(preprocess_text)

        valid_mask = df_undef['processed'].str.len() > 5
        df_undef_valid = df_undef[valid_mask].copy()
        docs = df_undef_valid['processed'].tolist()

        if len(docs) >= min_cluster_size:
            # BERTopic
            embedding_model = SentenceTransformer('paraphrase-multilingual-MiniLM-L12-v2')

            umap_model = UMAP(
                n_neighbors=min(15, len(docs) // 10),
                n_components=5,
                min_dist=0.0,
                metric='cosine',
                random_state=42
            )

            hdbscan_model = HDBSCAN(
                min_cluster_size=min_cluster_size,
                min_samples=max(5, min_cluster_size // 5),
                metric='euclidean',
                cluster_selection_method='eom',
                prediction_data=True
            )

            vectorizer_model = CountVectorizer(
                ngram_range=(1, 2),
                stop_words=list(RUSSIAN_STOPWORDS | TECH_STOPWORDS),
                min_df=2,
                max_df=0.8
            )

            topic_model = BERTopic(
                embedding_model=embedding_model,
                umap_model=umap_model,
                hdbscan_model=hdbscan_model,
                vectorizer_model=vectorizer_model,
                nr_topics=nr_topics,
                top_n_words=10,
                calculate_probabilities=False,
                verbose=False
            )

            topics, _ = topic_model.fit_transform(docs)

            df_undef_valid = df_undef_valid.reset_index(drop=True)
            df_undef_valid['topic_id'] = topics

            def get_topic_name(tid):
                if tid == -1:
                    return "📂 Прочее / Не определено"
                words = topic_model.get_topic(tid)
                if words:
                    return "🤖 BERTopic: " + " | ".join([w[0] for w in words[:3]])
                return f"Тема {tid}"

            df_undef_valid['bertopic_cat'] = df_undef_valid['topic_id'].apply(get_topic_name)

            # Обновляем основной DataFrame
            for idx in df_undef_valid.index:
                orig_idx = df_undef_valid.loc[idx, df.index.name] if df.index.name else idx
                # Нужно аккуратно обновить — используем merge

            # Проще: создаём mapping по индексу
            idx_to_cat = dict(zip(df_undef_valid.index, df_undef_valid['bertopic_cat']))
            for idx, cat in idx_to_cat.items():
                if idx in df.index:
                    df.loc[idx, 'category'] = cat

    # Заполняем оставшиеся NaN
    df['category'] = df['category'].fillna("📂 Прочее / Не определено")

    # Добавляем источник категоризации
    df['category_source'] = df['category'].apply(
        lambda x: 'Правила' if not x.startswith('🤖') and not x.startswith('📂') else 
                  ('BERTopic' if x.startswith('🤖') else 'Не определено')
    )

    return df


# ==========================================
# 4. ОТЧЁТ
# ==========================================
def print_report(df):
    print(f"\n{'='*60}")
    print("СВОДКА ПО КАТЕГОРИЯМ:")
    print(f"{'='*60}")

    summary = df.groupby(['category', 'category_source']).size().reset_index(name='count')
    summary = summary.sort_values('count', ascending=False)

    for _, row in summary.iterrows():
        src_marker = "📋" if row['category_source'] == 'Правила' else "🤖" if row['category_source'] == 'BERTopic' else "❓"
        print(f"  {src_marker} {row['category']:<50} ({row['count']} задач)")

    print(f"\nВсего категорий: {df['category'].nunique()}")
    print(f"По правилам: {(df['category_source'] == 'Правила').sum()}")
    print(f"BERTopic: {(df['category_source'] == 'BERTopic').sum()}")
    print(f"Не определено: {(df['category_source'] == 'Не определено').sum()}")


# ==========================================
# 5. MAIN
# ==========================================
def main():
    parser = argparse.ArgumentParser(description='Гибридная категоризация задач Redmine')
    parser.add_argument('--input', '-i', required=True, help='Входной CSV')
    parser.add_argument('--output', '-o', default='categorized_hybrid.csv', help='Выходной CSV')
    parser.add_argument('--subject-col', default='Тема', help='Колонка с темой')
    parser.add_argument('--module-col', default='Module', help='Колонка с модулем')
    parser.add_argument('--min-cluster', type=int, default=25, help='Мин. размер категории для BERTopic')
    parser.add_argument('--nr-topics', default='auto', help='Число тем BERTopic')

    args = parser.parse_args()

    print(f"Чтение {args.input}...")
    df = pd.read_csv(args.input)
    print(f"Загружено задач: {len(df)}\n")

    nr_topics = int(args.nr_topics) if args.nr_topics != 'auto' else 'auto'
    df_result = categorize_hybrid(
        df,
        subject_col=args.subject_col,
        module_col=args.module_col,
        min_cluster_size=args.min_cluster,
        nr_topics=nr_topics
    )

    df_result.to_csv(args.output, index=False, encoding='utf-8-sig')
    print(f"\n✅ Результат сохранён: {args.output}")

    print_report(df_result)


if __name__ == '__main__':
    main()
