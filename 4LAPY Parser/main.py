import requests
from config import cities
import csv


class get4Lapy():
    
    def __init__(self, city, count):
        
        self.city = city
        self.count = count
        
    def startParse(self):
        
        headers = {
            'accept': 'application/json, text/plain, */*',
            'accept-language': 'ru,en;q=0.9,en-GB;q=0.8,en-US;q=0.7',
            'channel': 'web',
            'dnt': '1',
            'locale': 'ru-RU',
            'origin': 'https://4lapy.ru',
            'poligon': 'r600-baza-10-18-do-08-00-18-22-do-16-00',
            'priority': 'u=1, i',
            'referer': 'https://4lapy.ru/',
            'region': f'{cities[self.city]}',
            'sec-ch-ua': '"Microsoft Edge";v="131", "Chromium";v="131", "Not_A Brand";v="24"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'same-site',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36 Edg/131.0.0.0',
        }
        
        params = {
            'page': '1',
            'offset': '0',
            'limit': f'{self.count}',
            'withSections': 'true',
            'sort': 'popular',
            'filter[categoryIds]': '413',
            'filterByExpressStore': 'false',
            'skipQueryCorrection': 'false',
            'poligon': 'r600-baza-10-18-do-08-00-18-22-do-16-00',
            'region': f'{cities[self.city]}',
            'channel': 'web',
            'locale': 'ru-RU',
        }
            
        response = requests.get('https://api.4lapy.ru/api/v1/catalog/products', params=params, headers=headers)
        
        with open("output.csv", mode="a", encoding='utf-8') as w_file:
            
            file_writer = csv.writer(w_file, delimiter = ",", lineterminator="\r")
            
            file_writer.writerow(["id", "name", "url", "normal_pirce", "promo_price", "brand"])
        
            for item in response.json()['items']:
                
                price, old_price = int(item['offers'][0]['price']['priceValue']), int(item['offers'][0]['price']['oldPriceValue'])
                
                normal_pirce, promo_price = '', ''
                
                if price != 0 and old_price != 0:
                    
                    normal_pirce, promo_price = old_price, price
                    
                elif price != 0 and old_price == 0 :
                    
                    normal_pirce, promo_price = price, None
            
                file_writer.writerow([item['offers'][0]['productId'], item['offers'][0]['name'], 'https://4lapy.ru'+item['offers'][0]['url'], normal_pirce, promo_price, item['brandCode']])
            
        print('Finish!')
            
        return 'OK'

# Settings
# City: 0 - Москва; 1 - Питер
# Count: кол-во продуктов

get4Lapy(1, 100).startParse()
get4Lapy(0, 100).startParse()

# Daniil Ionov // doublemain9@gmail.com
# Daniil Ionov // doublemain9@gmail.com
# Daniil Ionov // doublemain9@gmail.com

