import re
from datetime import datetime

import psycopg2
import requests
from urllib.parse import urlencode
from bs4 import BeautifulSoup
import os
from crawl_logger import logger
from e_product_comparison.e_crawler.crawler_constants import DIV, A, SPAN

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'e_product_comparison.settings')

connection = psycopg2.connect(database='product_e',
                              user='postgres',
                              password='dhanesh@22',
                              host='localhost',
                              port='5432'
                              )


def crawl_flipkart(start_url):
    count = 1
    continue_crawling = True
    while continue_crawling:
        try:
            url = start_url.replace('%s', str(count))
            print('1: ', url)
            response = requests.get(url)
            soup = BeautifulSoup(response.content, 'html.parser')

            product_titles = soup.find_all(DIV, class_='_4rR01T')
            product_price = soup.find_all(DIV, class_='_3I9_wc _27UcVY')
            product_offer = soup.find_all(DIV, class_='_3Ay6Sb')
            product_offer_price = soup.find_all(DIV, class_='_30jeq3 _1_WHN1')
            product_data = soup.find_all(A, class_='_1fQZEK')
            next_page = soup.find(DIV, class_='_2MImiq')
            # _next = soup.find_all(A, class_='ge-49M')
            # _page = soup.find_all(A, class_='_1LKTO3')
            current_page = next_page.find(SPAN).text.split()[1].replace(',', '')
            final_page = next_page.find(SPAN).text.split()[3].replace(',', '')
            if int(current_page) < int(final_page):
                count += 1
            elif int(current_page) >= int(final_page):
                continue_crawling = False
        except AttributeError as ex:
            logger.error(f'Attribute error occurred as {ex}')
            continue_crawling = False
            print('scraping completed due to attributre error')
        else:
            for data in zip(product_titles, product_price, product_offer, product_offer_price, product_data):
                specifications = re.findall("\(.*?\)", data[0].text)
                print('specifications: ', specifications)
                print('1: ', specifications[0])
                color = specifications[0].replace('(', '').replace(')', '').split(',')
                print('2: ', type(color))
                if len(color) > 1:
                    print('3: ', color[0])
                    print('4: ', color[1])
                else:
                    print('3: ', color[0])
                name = re.sub("\(.*?\)", "()", data[0].text)
                product_name = name.replace('()', '').rstrip(' ')
                original_price = data[1].text.replace('₹', '').replace(',', '')
                offer_percentage = data[2].text.replace('off', '').replace('%', '')
                vendor_price = data[3].text.replace('₹', '').replace(',', '')
                product_url = 'https://www.flipkart.com' + data[4].get("href")

                create_offers(shop_id=1, product_name=product_name.upper(), original_price=original_price,
                              offer_percentage=offer_percentage,
                              vendor_price=vendor_price, product_url=product_url)


def crawl_e_websites(start_url):
    urls = [start_url.replace('%s', str(page)) for page in range(1, 3)]

    for url in urls:
        print('url: ', url)
        response = requests.get(url)
        soup = BeautifulSoup(response.content, 'html.parser')

        product_titles = soup.find_all('h3', class_='product-title plp-prod-title')
        product_offer_price = soup.find_all(SPAN, attrs={'data-testid': 'new-price'})
        product_offer = soup.find_all(SPAN, class_='discount discount-mob-plp')
        product_price = soup.find_all(SPAN, attrs={'data-testid': 'old-price'})
        product_data = soup.find_all(DIV, class_='product-img')

        for data in zip(product_titles, product_price, product_offer, product_offer_price, product_data):
            name = re.sub("\(.*?\)", "()", data[0].text)
            name = name.replace('()', '').rstrip(' ')
            create_offers(shop_id=3, product_name=name.upper(),
                          original_price=data[1].text.replace('₹', '').replace(',', '').replace('MRP:', ''),
                          offer_percentage=data[2].text.replace('Off', '').replace('%', ''),
                          vendor_price=data[3].text.replace('₹', '').replace(',', '').replace('MRP:', ''),
                          product_url='https://www.croma.com' + data[4].next.get('href'))


def create_offers(shop_id, product_name, original_price, offer_percentage, vendor_price, product_url):
    with connection.cursor() as cursor:
        qry = "SELECT id, name FROM product_product WHERE name like (%s);"
        print('name: ', product_name)
        cursor.execute(qry, (product_name,))
        product = cursor.fetchone()
        print('product: ', product)
        if product is not None:
            print('into query: ', product[1])
            query = '''INSERT into offer_offer(product_id, shop_id, actual_price, offer_percentage,
                    vendor_price, product_url, is_active, created_on,
                     updated_on) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s);'''
            values = (product[0], shop_id, original_price, offer_percentage, vendor_price, product_url, True,
                      datetime.now().strftime("%d/%m/%Y %H:%M:%S"),
                      datetime.now().strftime("%d/%m/%Y %H:%M:%S")
                      )
            cursor.execute(query, values)
            connection.commit()

        else:
            pass


if __name__ == "__main__":
    is_continue = True
    while is_continue:
        user_choice = int(input('Enter 1 to scrawl e_crawler\nEnter 2 to scrawl amazon\nEnter 3 to scrawl croma: '))
        match user_choice:
            case 1:
                print('Crawling flipkart for iphones')
                # crawl_flipkart('https://www.flipkart.com/search?q=iphone+mobile&page=%s')
                # print('crawling flipkart for android phones')
                crawl_flipkart('https://www.flipkart.com/search?q=android+mobile&page=%s')
                # print('crawling electronics')

            case 2:
                print('start scraping amazon')
                crawl_e_websites('https://www.amazon.in/s?i=electronics&rh=n%3A1389401031&fs=true&page=%s')

            case 3:
                print('start crawling crome')
                crawl_e_websites('https://www.croma.com/phones-wearables/mobile-phones/iphones/c/97')
