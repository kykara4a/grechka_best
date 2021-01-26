import requests                                                     
import pandas as pd
from bs4 import BeautifulSoup 

from django.shortcuts import render

from .models import Product


def parse_epic():

    url = 'https://epicentrk.ua/ua/shop/krupy-i-makaronnye-izdeliya/fs/vid-krupa-grechnevaya/'            
    r = requests.get(url)
    with open('test3.html', 'w', encoding='utf-8') as output_file:     
        output_file.write(r.text)

    result = pd.DataFrame()
    name_d = []
    price_d = []
    store = []
    counter_price = 0                                                   #счетчик для цен (чтобы ограничить потом количество имен (которые будут без цен, например товара нету)
    counter_name = 0
    counter_links = 0                             #счетчик для имен товара
    store = []
    links = []                                                     

    r = requests.get(url)                                              
    soup = BeautifulSoup(r.text, features="html.parser")

    for link in soup.find_all('span', {'class': 'card__price-sum'}):    
        counter_price += 1
        price = link.text.replace('<br />', '\n').strip()
       # print(price)
        price_d.append(price)                                             

    for link in soup.find_all('div', {'class': 'card__name'}):       
        counter_name += 1
        name = link.text.replace('<br />', '\n').strip()                  
       # print(name)
        name_d.append(name)
        store.append('Epicenter')                                            
        if counter_name == counter_price:
            break  

    for link in soup.find_all('a', {'class': 'custom-link custom-link--big custom-link--inverted custom-link--blue'}): #находим все теги span с классом product-price которые есть на странице
        counter_links += 1                                                
        if link.has_attr('href'):
            links.append('https://epicentrk.ua' + link['href'])
            #print(link['href'])
        if counter_links == counter_price:
            break                                                       

    df = pd.DataFrame({'name': name_d, 'price': price_d, 'store': store, 'links': links})

    return df

def parse_auchan():
    url = 'https://auchan.zakaz.ua/ru/categories/buckwheat-auchan/'      #url страницы
    r = requests.get(url)
    with open('test3.html', 'w', encoding='utf-8') as output_file:      #загружаем html код в файл
        output_file.write(r.text)

    result = pd.DataFrame()
    name_d = []
    price_d = []
    store = []
    links = []
    counter_price = 0                                                   #счетчик для цен (чтобы ограничить потом количество имен (которые будут без цен, например товара нету)
    counter_name = 0   
    counter_links = 0                                                      #счетчик для имен товара

    r = requests.get(url)                                               #передаем url
    soup = BeautifulSoup(r.text, features="html.parser")                #парсим страницу


    for link in soup.find_all('span', {'class': 'jsx-3642073353 Price__value_caption'}):      #находим все теги span с классом product-price которые есть на странице
        counter_price += 1
        price = link.text.replace('<br />', '\n').strip()                 #записуем в price текст из тега удаляя все отступы и пробелы
        #print(price)
        price_d.append(price)                                             #заполняем список price_d данными которые получены в price

    for link in soup.find_all('span', {'class': 'jsx-725860710 product-tile__title'}):    #находим все теги div с классом h3 product-title которые есть на странице
        counter_name += 1
        name = link.text.replace('<br />', '\n').strip()                  #записуем в name текст из тега удаляя все отступы и пробелы
       # print(name)
        name_d.append(name)   
        store.append('Auchan')                                              #заполняем список name_d данными которые получены в name
        if counter_name == counter_price:
            break                                                           #когда счетчик имен достигнет количества цен прекращаем поиск

    for link in soup.find_all('a', {'class': 'jsx-725860710 product-tile'}):
        counter_links += 1                                                #находим все теги span с классом product-price которые есть на странице
        if link.has_attr('href'):
            links.append('https://auchan.zakaz.ua' + link['href'])
            #print(link['href'])
        if counter_links == counter_price:
            break        

    df = pd.DataFrame({'name': name_d, 'price': price_d, 'store': store, 'links': links})     

    return df

def parse_novus():
    
    url = 'https://novus.zakaz.ua/ru/categories/buckwheat/'            #url страницы
    r = requests.get(url)
    with open('test4.html', 'w', encoding='utf-8') as output_file:      #загружаем html код в файл
        output_file.write(r.text)


    result = pd.DataFrame()
    name_d = []
    store = []
    price_d = []
    links = []
    counter_price = 0                                                   #счетчик для цен (чтобы ограничить потом количество имен (которые будут без цен, например товара нету)
    counter_name = 0   
    counter_links = 0                                                   #счетчик для имен товара
    


    r = requests.get(url)                                               #передаем url
    soup = BeautifulSoup(r.text, features="html.parser")                #парсим страницу


    for link in soup.find_all('span', {'class': 'jsx-3642073353 Price__value_caption Price__value_discount'}):      #исключительная ситуация скидка
        counter_price += 1
        price = link.text.replace('<br />', '\n').strip()                 #записуем в price текст из тега удаляя все отступы и пробелы
        #print(price+'*')
        price_d.append(price+'*')                                             #заполняем список price_d данными которые получены в price

    for link in soup.find_all('span', {'class': 'jsx-3642073353 Price__value_caption'}):      #находим все теги span с классом product-price которые есть на странице
        counter_price += 1
        price = link.text.replace('<br />', '\n').strip()                 #записуем в price текст из тега удаляя все отступы и пробелы
        #print(price)
        price_d.append(price)
                                                                    #заполняем список price_d данными которые получены в price
    for link in soup.find_all('a', {'class': 'jsx-725860710 product-tile'}):
        counter_links += 1                                                #находим все теги span с классом product-price которые есть на странице
        if link.has_attr('href'):
            links.append('https://novus.zakaz.ua' + link['href'])
            #print(link['href'])
        if counter_links == counter_price:
            break


    for link in soup.find_all('span', {'class': 'jsx-725860710'}):      #находим все теги div с классом h3 product-title которые есть на странице
        counter_name += 1
        name = link.text.replace('<br />', '\n').strip()                  #записуем в name текст из тега удаляя все отступы и пробелы
        #print(name)
        name_d.append(name)
        store.append('Novus')                                                      #заполняем список name_d данными которые получены в name
        if counter_name == counter_price:
            break                                                           #когда счетчик имен достигнет количества цен прекращаем поиск

    df = pd.DataFrame({'name': name_d, 'price': price_d, 'store': store, 'links': links})             #создаем dataFrame с именами столбцов name_d, price_d

    #print(df)
    return df

def index(request):

    data1 = parse_epic()
    data2 = parse_auchan()
    data3 = parse_novus()

    data = pd.concat([data1, data2, data3], axis=0, ignore_index=True)
    data.sort_values('price', inplace = True)

    data = data.reset_index(drop = True)
    data.index += 1
    data = data.reset_index().to_dict('records')
    headers = ['id', 'Назва', 'Ціна (грн)', 'Магазин']
    #size = data.shape[0]

    #print(data)

    #name = data["name"].tolist()
    #price = data["price"].tolist()
    #store = data["store"].tolist()

    return render(
        request,
        'index.html',
<<<<<<< Updated upstream
        context={'data':data, 'headers':headers},
=======
        context={'num_Products': name_d},
>>>>>>> Stashed changes
    )