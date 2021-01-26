import requests                                                     
import pandas as pd
from bs4 import BeautifulSoup 

from django.shortcuts import render

from .models import Product

def price_str_to_float(price, digits):
    tmp = ''                                                            # Каждую цену из строчного типа переводим в вещественный, чтоб можно было корректно сортировать в дальнейшем
    for j in range(len(price)):                                         # Создается подстрака, в которую попадает только числовая часть цены
        if price[j] == ',':                                             # Посимвольно переносятся элементы строки цены в подстроку до первого символа, который не цифра или не точка(запята)
            tmp += '.'
        elif price[j] in digits:
            tmp += price[j]
        elif price[j] not in digits:
            break
    price = float(tmp)                                                  # Непосредственно перевод цены из строки в вещественное число
    return price


def parse_epic():

    url = 'https://epicentrk.ua/ua/shop/krupy-i-makaronnye-izdeliya/fs/vid-krupa-grechnevaya/'            
    r = requests.get(url)
    with open('test3.html', 'w', encoding='utf-8') as output_file:     
        output_file.write(r.text)

    result = pd.DataFrame()
    name_d = []
    price_d = []
    store = []
    counter_price = 0                                                   
    counter_name = 0                                                    

    r = requests.get(url)                                              
    soup = BeautifulSoup(r.text, features="html.parser")

    digits = set(['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '.'])  # Множество цифр для перевода цены из строки в число
    for link in soup.find_all('span', {'class': 'card__price-sum'}):    
        counter_price += 1
        price = link.text.replace('<br />', '\n').strip()

        price = price_str_to_float(price, digits)  # Перевод строки из цены в числоы

        print(price)
        price_d.append(price)                                             

    for link in soup.find_all('div', {'class': 'card__name'}):       
        counter_name += 1
        name = link.text.replace('<br />', '\n').strip()                  
        print(name)
        name_d.append(name)
        store.append('Epicenter')                                            
        if counter_name == counter_price:
            break                                                         

    df = pd.DataFrame({'name': name_d, 'price': price_d, 'store': store})

    return df

def parse_fozzy():
    url = 'https://fozzyshop.ua/ru/300143-krupa-grechnevaya'            #url страницы
    r = requests.get(url)
    with open('test3.html', 'w', encoding='utf-8') as output_file:      #загружаем html код в файл
        output_file.write(r.text)

    result = pd.DataFrame()
    name_d = []
    price_d = []
    store = []
    counter_price = 0                                                   #счетчик для цен (чтобы ограничить потом количество имен (которые будут без цен, например товара нету)
    counter_name = 0                                                    #счетчик для имен товара

    r = requests.get(url)                                               #передаем url
    soup = BeautifulSoup(r.text, features="html.parser")                #парсим страницу

    digits = set(['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '.'])    #Множество цифр для перевода цены из строки в число

    for link in soup.find_all('span', {'class': 'product-price'}):      #находим все теги span с классом product-price которые есть на странице
        counter_price += 1
        price = link.text.replace('<br />', '\n').strip()                 #записуем в price текст из тега удаляя все отступы и пробелы

        price = price_str_to_float(price, digits)                       #Перевод строки из цены в числоы

        print(price)
        price_d.append(price)                                             #заполняем список price_d данными которые получены в price

    for link in soup.find_all('div', {'class': 'h3 product-title'}):    #находим все теги div с классом h3 product-title которые есть на странице
        counter_name += 1
        name = link.text.replace('<br />', '\n').strip()                  #записуем в name текст из тега удаляя все отступы и пробелы
        print(name)
        name_d.append(name)   
        store.append('Fozzy')                                              #заполняем список name_d данными которые получены в name
        if counter_name == counter_price:
            break                                                           #когда счетчик имен достигнет количества цен прекращаем поиск

    df = pd.DataFrame({'name': name_d, 'price': price_d, 'store': store}) 

    return df

def parse_novus():
    url = 'https://epicentrk.ua/ua/shop/krupy-i-makaronnye-izdeliya/fs/vid-krupa-grechnevaya/'            #url страницы
    r = requests.get(url)
    with open('test3.html', 'w', encoding='utf-8') as output_file:      #загружаем html код в файл
        output_file.write(r.text)

    result = pd.DataFrame()
    name_d = []
    price_d = []
    store = []
    counter_price = 0                                                   #счетчик для цен (чтобы ограничить потом количество имен (которые будут без цен, например товара нету)
    counter_name = 0                                                    #счетчик для имен товара

    r = requests.get(url)                                               #передаем url
    soup = BeautifulSoup(r.text, features="html.parser")                #парсим страницу

    digits = set(['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '.'])  # Множество цифр для перевода цены из строки в число
    for link in soup.find_all('span', {'class': 'card__price-sum'}):      #находим все теги span с классом product-price которые есть на странице
        counter_price += 1
        price = link.text.replace('<br />', '\n').strip()                 #записуем в price текст из тега удаляя все отступы и пробелы

        price = price_str_to_float(price, digits)  # Перевод строки из цены в числоы

        print(price)
        price_d.append(price)                                             #заполняем список price_d данными которые получены в price

    for link in soup.find_all('div', {'class': 'card__name'}):          #находим все теги div с классом h3 product-title которые есть на странице
        counter_name += 1
        name = link.text.replace('<br />', '\n').strip()                  #записуем в name текст из тега удаляя все отступы и пробелы
        print(name)
        name_d.append(name)                                                 #заполняем список name_d данными которые получены в name
        store.append('Novus')                                        
        if counter_name == counter_price:
            break                                                           #когда счетчик имен достигнет количества цен прекращаем поиск

    df = pd.DataFrame({'name': name_d, 'price': price_d, 'store': store})               #создаем dataFrame с именами столбцов name_d, price_d

    #print(df)
    return df

def index(request):

    data1 = parse_epic()
    data2 = parse_fozzy()
    data3 = parse_novus()

    data = pd.concat([data1, data2, data3], axis=0, ignore_index=True)
    data.sort_values('price', inplace = True)



    data = data.reset_index(drop = True)
    data.index += 1
    data = data.reset_index().to_dict('records')
    headers = ['id', 'name', 'price', 'store']
    #size = data.shape[0]

    print(data)

    #name = data["name"].tolist()
    #price = data["price"].tolist()
    #store = data["store"].tolist()

    return render(
        request,
        'index.html',
        context={'data':data, 'headers':headers},
    )