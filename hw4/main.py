import os
import re
from collections import Counter, defaultdict
from math import log

from hw2.main import extract_text_from_html

FOLDER = 'results'
TOKEN_FOLDER = '../hw2/results'
PAGES_FOLDER = '../hw1/pages'
PAGES_COUNT = 122


def idf(term_tf):
    df_counter = defaultdict(int)
    for doc_id in term_tf:
        for term, tf in term_tf[doc_id].items():
            if tf > 0:
                df_counter[term] += 1
    return {term: log(PAGES_COUNT / df_counter[term]) for term in df_counter}


def write_tf_idf(term_tf, idf_dict, name, i):
    path = os.path.join(FOLDER, f"{name}-{i}.txt")
    with open(path, "w", encoding="utf-8") as f:
        for term, tf in term_tf[i].items():
            tf_idf = tf * idf_dict[term]
            f.write(f"{term} {idf_dict[term]} {tf_idf}\n")


if __name__ == '__main__':
    if not os.path.exists(FOLDER):
        os.makedirs(FOLDER)

    term_tf = defaultdict(dict)
    lemma_tf = defaultdict(dict)

    for i in range(1, PAGES_COUNT + 1):
        tokens = []
        lemmas = []

        token_path = os.path.join(TOKEN_FOLDER, f"tokens-{i}.txt")
        with open(token_path, 'r', encoding="utf-8") as f:
            tokens = [line.strip() for line in f if line.strip()]

        page_path = os.path.join(PAGES_FOLDER, f"download-{i}.html")
        with open(page_path, 'r', encoding="utf-8") as f:
            text = extract_text_from_html(f.read().lower())
            words = re.findall(r"\w+", text)
            counter = Counter(words)
            # counter - счетчик для терминов

        total_terms_in_doc = sum(counter[token] for token in tokens)

        for token in tokens:
            term_tf[i][token] = counter[token] / total_terms_in_doc
        # tf как отношение количества раз, которое токен (термин) встречается на странице к общему количеству терминов на странице

        lemma_path = os.path.join(TOKEN_FOLDER, f"lemmas-{i}.txt")
        with open(lemma_path, 'r', encoding="utf-8") as f:
            for line in f:
                lemma = line.split()[0]
                forms = line.split()[1:]
                lemma_tf[i][lemma] = sum(counter[form] for form in forms) / total_terms_in_doc
                # tf для леммы - отношение суммы вхождения числа терминов к общему количеству терминов в документе

    idf_term = idf(term_tf)
    idf_lemma = idf(lemma_tf)

    for i in range(1, PAGES_COUNT + 1):
        write_tf_idf(term_tf, idf_term, f'tokens', i)
        write_tf_idf(lemma_tf, idf_lemma, f'lemmas', i)
