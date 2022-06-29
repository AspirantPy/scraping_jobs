from bs4 import BeautifulSoup
import requests
import re
from datetime import datetime, timezone, date, timedelta
import time
import csv

# Parsing with query: 'Разработка и IT/Скрипты и боты/Парсеры'

def get_datetime():
    '''Finds local time for GMT +4 timezone'''

    now_utc = datetime.now(timezone.utc)
    local_time = str(now_utc + timedelta(hours=4))
    time = local_time[11:13] + '-' + local_time[14:16]
    date = local_time[8:10] + '-' + local_time[5:7]

    return time + '_' + date

kwork_ru = requests.get('https://kwork.ru/projects?c=41&attr=211')
print(kwork_ru)

csv_file = open(f'{get_datetime()}.csv', 'w', newline='') # last arg disables universal newlines to avoid windows from adding blank rows to csv.
csv_writer = csv.writer(csv_file)
csv_writer.writerow(['Headline & Source', 'Price', 'Link', 'Summary', 'Applicants', 'Time remaining']) # These are headers for our columns.

soup = BeautifulSoup(kwork_ru.text, 'lxml')

kwork_offers = soup.find_all('div', class_=re.compile('^card want-card js-card-'))
for kwork_offer in kwork_offers:
    activity = kwork_offer.find('div', class_='query-item__info')
    time_remaining = activity.find_all('span')[0].text
    num_applicants = activity.find_all('span')[1].text.strip()
    match = re.search('[0-9]+', num_applicants)

    if int(match.group()) <= 10:

        headline = kwork_offer.find('a').text
        link = kwork_offer.a['href']

        raw_text = kwork_offer.find('div', class_='wants-card__description-text br-with-lh').text
        useful_text = re.findall('Показать полностью(.*)Скрыть', raw_text, re.DOTALL)[0].replace(u'\xa0', u' ')
        price_offer = kwork_offer.find('div', class_='wants-card__header-price wants-card__price m-hidden').text
        min_price = int(''.join(re.findall('[0-9]+', price_offer)))
        price_output = f"Бюджет: до {min_price} р., " + f"допустимый: {min_price * 3}"

        print(headline)
        print(price_output)
        print(link)
        print(time_remaining)
        print(num_applicants)
        print(useful_text)
        print()

        csv_writer.writerow([headline, price_output, link, useful_text, num_applicants, time_remaining])

# 2nd page

kwork_ru_p2 = requests.get('https://kwork.ru/projects?c=41&attr=211&page=2')
print(kwork_ru_p2)

soup = BeautifulSoup(kwork_ru_p2.text, 'lxml')

kwork_offers = soup.find_all('div', class_=re.compile('^card want-card js-card-'))
for kwork_offer in kwork_offers:
    activity = kwork_offer.find('div', class_='query-item__info')
    time_remaining = activity.find_all('span')[0].text
    num_applicants = activity.find_all('span')[1].text.strip()
    match = re.search('[0-9]+', num_applicants)

    if int(match.group()) <= 10: # re.match('[0-9]+', num_applicants)

        headline = kwork_offer.find('a').text
        link = kwork_offer.a['href']

        raw_text = kwork_offer.find('div', class_='wants-card__description-text br-with-lh').text
        useful_text = re.findall('Показать полностью(.*)Скрыть', raw_text, re.DOTALL)[0].replace(u'\xa0', u' ')
        price_offer = kwork_offer.find('div', class_='wants-card__header-price wants-card__price m-hidden').text
        min_price = int(''.join(re.findall('[0-9]+', price_offer)))

        print(headline)
        print(f"Бюджет: до {min_price} р., " + f"допустимый: {min_price * 3}")
        print(link)
        print(time_remaining)
        print(num_applicants)
        print(useful_text)
        print()