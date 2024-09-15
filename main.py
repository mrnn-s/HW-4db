#User-Agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36


from lxml import html
import requests
from pprint import pprint
import csv
import os

# Строка агента пользователя в заголовке HTTP-запроса, чтобы имитировать веб-браузер и избежать блокировки сервером.
header = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36'}

# 1.  Выберите веб-сайт с табличными данными, который вас интересует. (Например, news.mail.ru)
url = 'https://news.mail.ru/'

# 2.  Напишите код Python, использующий библиотеку requests для отправки HTTP GET-запроса на сайт
# и получения HTML-содержимого страницы.
response = requests.get(url, headers = header)
if response.status_code == 200:
    print("Успешный запрос API!")
    dom = html.fromstring(response.text)

    # извлgit ссылок на главные новости
    links = dom.xpath("//div[@data-logger='news__MainTopNews']//li[@class='list__item']//a[@href]/@href | //div[@data-logger='news__MainTopNews']//td[not(@class='daynews__spring')]//a[@href]/@href")
    
    items_list = []
    
    for link in links:
        item_info = {}
        
        response = requests.get(link, headers=header)
        
        if response.status_code == 200:
            info = html.fromstring(response.text)
            
            # Извлечение заголовка
            article = info.xpath("//h1[@data-qa='Title']/text()")
            article = article[0] if article else "Не найдено"
            
            # Извлечение источника новости
            source = info.xpath("//span[@class='breadcrumbs__item']//span[@class='link__text']/text()")
            source = source[0] if source else "Не найдено"
            
            # Извлечение тегов
            tags = info.xpath("//a[@data-qa='tags-link']/text()")
            
            
            item_info["article"] = article
            item_info["source"] = source
            item_info["tags"] = tags
            item_info["link"] = link
            items_list.append(item_info)   
    pprint(items_list)
else:
    print("Ошибка при выполнении запроса")
   
    
    
 # 4.  Сохраните извлеченные данные в CSV-файл с помощью модуля csv.
   
file_name = 'file_for_hw4.csv' # Открытие файла для записи
with open(file_name, 'w', newline='', encoding='utf-8') as file:
        fieldnames = ['article', 'source', 'tags', 'link']
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        
        # Запись заголовков столбцов
        writer.writeheader()
        
        # Запись строк данных
        for item in items_list:
            # Преобразование списка тегов в строку
            item['tags'] = ', '.join(item['tags'])
            writer.writerow(item)

print(f"CSV файл '{file_name}' создан и туда записаны новости.")
