import os
import time

import requests


ENCODING = 'utf-8'
FOLDER = 'pages'
INDEX = 'index.txt'
CHAPTER_COUNT = 122


# скачанные страницы - главы книги "Гарри Поттер и методы рационального мышления"
def download_page(chapter_number):
    url = f'https://hpmor.ru/book/1/{chapter_number}/'

    response = requests.get(url)
    response.encoding = ENCODING

    filename = os.path.join(FOLDER, f"download-{chapter_number}.html")
    with open(filename, 'w', encoding=ENCODING) as file:
        file.write(response.text)

    return url


if __name__ == '__main__':
    if not os.path.exists(FOLDER):
        os.makedirs(FOLDER)

    with open(INDEX, 'w', encoding=ENCODING) as file:
        for i in range(1, CHAPTER_COUNT + 1):
            url = download_page(i)
            file.write(f'{i} {url}\n')

            # паузы между запросами
            if i % 5 == 0:
                time.sleep(2)
                print(f'{i} chapters downloaded')
