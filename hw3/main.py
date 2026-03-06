import os
import re
from collections import defaultdict

import pymorphy3

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
INDEX = os.path.join(BASE_DIR, 'inverted_index.txt')
morph = pymorphy3.MorphAnalyzer()


def get_inverted_index():
    index = defaultdict(set)
    # index - словарь вида {'лемма' : 'документ1', 'документ2', 'документ3'}
    with open(INDEX, "r", encoding="utf-8") as file:
        for line in file:
            parts = line.strip().split(maxsplit=1)
            lemma = parts[0]
            docs = eval(parts[1])
            index[lemma] = set(docs)
    return index


def replace_not(match):
    word = match.group(1)
    return f"(all_docs - {word})"


def normalize_query(query):
    query = query.lower()

    # заменяю операторы
    query = query.replace(" and ", " & ")
    query = query.replace(" or ", " | ")
    # заменяю not на выражение с all_docs
    query = re.sub(r"not\s+([а-яё]+)", replace_not, query)

    return query


def boolean_search(query, index, all_docs):
    query = normalize_query(query)

    # выделяю токены - русские слова (т.к. мой индекс построен только на русских словах)
    tokens = set(re.findall(r"[а-яё]+", query))

    # если слово не встречалось в индексе, создаю для него пустой сет
    # чтобы потом работало вычисление запроса
    for token in tokens:
        if token not in index:
            index[token] = set()

    # преобразую запрос в питон выражение
    # пример запроса: (Гарри  AND Гермиона) OR Хогвартс
    # стало: "(index['гарри'] & index['гермиона']) | index['хогвартс']"
    expr = query
    for token in tokens:
        lemma = morph.parse(token)[0].normal_form
        expr = re.sub(rf"\b{token}\b", f"index['{lemma}']", expr)

    result = eval(expr)
    return result


if __name__ == '__main__':
    index = get_inverted_index()
    all_docs = {f"download-{i}.html" for i in range(1, 123)}

    while True:
        print("Доступные операторы: AND, OR, NOT")
        query = input("Введите запрос: ").lower()
        if query == 'exit':
            break
        try:
            result = boolean_search(query, index, all_docs)
            if not result:
                print('Ничего не найдено')
            else:
                print(f'Найдено в {len(result)} файлах: {result}')
        except:
            print('Вы ввели что-то не то')
