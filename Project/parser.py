import requests
from bs4 import BeautifulSoup
import csv

CSV = 'cars.csv'
#URL = 'https://auto.ria.com/search/?indexName=auto,order_auto,newauto_search&brand.id[0]=13&country.import.usa.not=-1&price.currency=1&abroad.not=0&custom.not=1&page=0&size=10'
HEADERS = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36'}


def get_html(url, params=None):
    r = requests.get(url, headers=HEADERS, params=params)
    return r


def get_content(html):
    soup = BeautifulSoup(html, 'html.parser')
    items = soup.find_all('div', class_='content-bar')
    cars = []

    for item in items:
        price_uah = item.find('span', class_='i-block')
        if price_uah:
            price_uah = price_uah.get_text().replace('\xa0грн', '')
        else:
            price_uah = 'Ціну уточнюйте!!!'
        cars.append({
            'title': item.find('span', class_='blue bold').get_text(strip=True),
            'link': item.find('a', class_='m-link-ticket').get('href'),
            'price_usd': item.find('span', class_='bold green size22').get_text(),
            'price_uah': price_uah,
            'run': item.find('li', class_='item-char js-race').get_text(),
        })
    return cars


def save_doc(items, path):
    with open(path, 'w', newline='') as file:
        writer = csv.writer(file, delimiter=';')
        writer.writerow(['Name', 'Link', 'Price Dollars', 'Price UAH', 'Run'])
        for item in items:
            writer.writerow([item['title'], item['link'], item['price_usd'], item['price_uah'], item['run']])


def parse():
    URL=input('Введіть посилання: ')
    URL = URL.strip()
    PAGENATION = input('Кількість сторінок: ')
    PAGENATION= int(PAGENATION.strip())
    html = get_html(URL)
    if html.status_code == 200:
        cars = []
        for page in range(1, PAGENATION):
            print(f'Парсимо сторінку: {page}')
            html = get_html(URL, params={'page': page})
            cars.extend(get_content(html.text))
            save_doc(cars, CSV)

    else:
        print('Error')


parse()



