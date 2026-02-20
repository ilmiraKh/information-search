import os
import re
from collections import defaultdict

import pymorphy3
from bs4 import BeautifulSoup

FOLDER = 'results'
PAGES_FOLDER = '../hw1/pages'
PAGES_COUNT = 122
# 122 главы в книге - в заданиии 1 было скачано 122 страницы


morph = pymorphy3.MorphAnalyzer()
russian_word_pattern = re.compile(r"^[а-яА-ЯёЁ]+$")
BAD_POS = {"PREP", "CONJ", "PRCL"} # предлоги, союзы, частицы не сохраняем


def extract_text_from_html(html):
    soup = BeautifulSoup(html, "html.parser")
    text = soup.get_text(separator=' ', strip=True)
    cleaned_text = re.sub(r'\s+', ' ', text)
    return cleaned_text


def extract_tokens(text):
    tokens = set()
    for word in text.lower().split():
        if not russian_word_pattern.match(word):
            continue

        parse = morph.parse(word)[0]

        if parse.tag.POS in BAD_POS:
            continue

        tokens.add(word)
    return tokens


if __name__ == '__main__':
    if not os.path.exists(FOLDER):
        os.makedirs(FOLDER)

    count = 0

    for i in range(1, PAGES_COUNT + 1):
        filename = os.path.join(PAGES_FOLDER, f"download-{i}.html")
        tokens = set()
        lemmas = defaultdict(set)
        # lemmas - словарь вида {'лемма' : 'токен1', 'токен2', 'токен3'}

        with open(filename, "r", encoding="utf-8") as file:
            html = file.read()
            text = extract_text_from_html(html)
            tokens.update(extract_tokens(text))

        with open(f'{FOLDER}/tokens-{i}.txt', "w", encoding="utf-8") as file:
            for token in sorted(tokens):
                file.write(f"{token}\n")

        for token in tokens:
            lemma = morph.parse(token)[0].normal_form
            lemmas[lemma].add(token)

        with open(f'{FOLDER}/lemmas-{i}.txt', "w", encoding="utf-8") as file:
            for lemma, forms in sorted(lemmas.items()):
                file.write(f"{lemma} {' '.join(forms)}\n")

        count += 1
        if count % 5 == 0:
            print(f"{count} pages processed")
