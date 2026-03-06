import os
from collections import defaultdict

INDEX = 'inverted_index.txt'
FOLDER = "../hw2/results"
PAGES_COUNT = 122
# 122 страницы


def build_inverted_index():
    index = defaultdict(set)
    # index - словарь вида {'лемма' : 'номер страницы 1', 'номер страницы 2', 'номер страницы 3'}

    for i in range(1, PAGES_COUNT + 1):
        path = os.path.join(FOLDER, f"lemmas-{i}.txt")

        with open(path, "r", encoding="utf-8") as file:
            for line in file:
                lemma = line.split()[0]
                index[lemma].add(i)

    return index


if __name__ == '__main__':
    with open(INDEX, "w", encoding="utf-8") as file:
        index = build_inverted_index()
        for lemma, doc_ids in sorted(index.items()):
            # преобразую номера страниц/документов в имена файлов
            filenames = [f"download-{doc_id}.html" for doc_id in sorted(doc_ids)]
            file.write(f"{lemma} {filenames}\n")
