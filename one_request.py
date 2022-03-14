import time
import requests
from lxml import html

URL = 'https://hh.ru/search/vacancy?&fromSearchLine=true&text=python'

USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 " \
             "(KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36"

HEADERS = {'User-Agent': f'{USER_AGENT}'}

start = time.time()

response = requests.get(url=URL, headers=HEADERS)

end = time.time()

delta = end - start
print(delta)

news_page = html.fromstring(response.text)


vacancy_links = news_page.xpath(
            '//div[contains(@class, "vacancy-serp-item")]'
            '//a[contains(@data-qa, "vacancy-title")]')

print(len(vacancy_links))

for i in vacancy_links:
    print(i)

