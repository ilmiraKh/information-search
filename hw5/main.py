import os
import re
from collections import Counter, defaultdict

import pymorphy3

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
INDEX_PATH = os.path.join(BASE_DIR, "..", "hw3", "inverted_index.txt")
TF_IDF_FOLDER = os.path.join(BASE_DIR, "..", "hw4", "results")
PAGES_FOLDER = os.path.join(BASE_DIR, "..", "hw1", "pages")
PAGES_COUNT = 122

morph = pymorphy3.MorphAnalyzer()


def get_inverted_index():
    index = defaultdict(set)
    with open(INDEX_PATH, "r", encoding="utf-8") as file:
        for line in file:
            parts = line.strip().split(maxsplit=1)
            lemma = parts[0]
            docs = eval(parts[1])
            index[lemma] = set(docs)
    return index


def load_tf_idf():
    vectors = defaultdict(dict)
    idf_dict = {}

    for i in range(1, PAGES_COUNT + 1):
        path = os.path.join(TF_IDF_FOLDER, f"lemmas-{i}.txt")
        if os.path.exists(path):
            with open(path, 'r', encoding='utf-8') as f:
                for line in f:
                    parts = line.strip().split()
                    if len(parts) == 3:
                        term, idf_str, tfidf_str = parts
                        vectors[i][term] = float(tfidf_str)
                        idf_dict[term] = float(idf_str)

    return vectors, idf_dict


def cosine_similarity(vec1, vec2):
    scalar = sum(vec1.get(t, 0) * vec2.get(t, 0) for t in set(vec1) | set(vec2))
    norm1 = sum(x * x for x in vec1.values()) ** 0.5
    norm2 = sum(x * x for x in vec2.values()) ** 0.5
    return scalar / (norm1 * norm2) if norm1 > 0 and norm2 > 0 else 0


def lemmatize_query(query):
    tokens = re.findall(r"\w+", query.lower())
    lemmas = []

    for token in tokens:
        lemma = morph.parse(token)[0].normal_form
        lemmas.append(lemma)

    return lemmas


def query_to_vector(lemmas, idf_dict):
    tf = Counter(lemmas)

    total = sum(tf.values())

    q_vec = {}
    for term in tf:
        if term in idf_dict:
            q_vec[term] = (tf[term] / total) * idf_dict[term]

    return q_vec


def vector_search(query, lemma_vectors, lemma_idf, index):
    query_lemmas = lemmatize_query(query)

    # список кандидатов - файлы, где леммы встречаются (из индекса)
    candidates = set()
    for lemma in query_lemmas:
        if lemma in index:
            candidates.update(index[lemma])

    if not candidates:
        print("Нет документов с этими леммами")
        return []

    query_vec = query_to_vector(query_lemmas, lemma_idf)

    scores = {}
    for doc in candidates:
        doc_id = int(doc.replace('download-', '').replace('.html', ''))
        if doc_id in lemma_vectors:
            doc_vec = lemma_vectors[doc_id]
            similarity = cosine_similarity(query_vec, doc_vec)
            scores[doc_id] = similarity

    ranked = sorted(scores.items(), key=lambda x: x[1], reverse=True)
    return ranked[:10]
    # возвращаю топ 10 лучших результатов


if __name__ == '__main__':
    lemma_vectors, lemma_idf = load_tf_idf()
    index = get_inverted_index()
    while True:
        query = input("Введите запрос: ").lower()
        if query == 'exit':
            break
        results = vector_search(query, lemma_vectors, lemma_idf, index)
        print("Результаты поиска:")

        for doc_id, score in results:
            print(f"download-{doc_id}.html  score={score:.4f}")
        print()
