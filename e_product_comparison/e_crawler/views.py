import os
import re
from datetime import datetime

import psycopg2
import requests
from bs4 import BeautifulSoup

from crawl_logger import logger

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'e_product_comparison.settings')

connection = psycopg2.connect(database='product_e',
                              user='postgres',
                              password='dhanesh@22',
                              host='localhost',
                              port='5432'
                              )


# def crawl_flipkart(start_url):
#     # start_url = 'https://www.flipkart.com/search?' + urlencode(
#     #     {'q': product}) + '&otracker=search&otracker1=search&marketplace=FLIPKART&as-show=off&as=off&page=%s'
#
#     urls = [start_url.replace('%s', str(page)) for page in range(1, 20)]
#
#     for url in urls:
#         print('1: ', url)
#         response = requests.get(url)
#         soup = BeautifulSoup(response.content, 'html.parser')
#
#         product_titles = soup.find_all('div', class_='_4rR01T')
#         product_price = soup.find_all('div', class_='_3I9_wc _27UcVY')
#         product_offer = soup.find_all('div', class_='_3Ay6Sb')
#         product_offer_price = soup.find_all('div', class_='_30jeq3 _1_WHN1')
#         product_data = soup.find_all('a', class_='_1fQZEK')
#         next_page = soup.find('div', class_='_2MImiq')
#         _next = soup.find_all('a', class_='ge-49M')
#         _page = soup.find_all('a', class_='_1LKTO3')
#
#         print('a: ', next_page)
#         print('b: ', _next)
#         print('c: ', _page)
#         for page in _page:
#             print('d: ', "https://www.flipkart.com"+page.get('href'))
#         # for i in zip(product_titles, product_price, product_offer, product_offer_price, product_data):
#         #     name = re.sub("\(.*?\)", "()", i[0].text)
#         #     product_name = name.replace('()', '').rstrip(' ')
#         #     original_price = i[1].text.replace('₹', '').replace(',', '')
#         #     offer_percentage = i[2].text.replace('off', '').replace('%', '')
#         #     vendor_price = i[3].text.replace('₹', '').replace(',', '')
#         #     product_url = 'https://www.flipkart.com' + i[4].get("href")
#         #
#         #     create_offers(shop_id=1, product_name=product_name, original_price=original_price,
#         #                   offer_percentage=offer_percentage,
#         #                   vendor_price=vendor_price, product_url=product_url)

def crawl_flipkart(start_url):
    count = 1
    continue_crawling = True
    while continue_crawling:
        try:
            url = start_url.replace('%s', str(count))
            print('1: ', url)
            response = requests.get(url)
            soup = BeautifulSoup(response.content, 'html.parser')

            product_titles = soup.find_all('div', class_='_4rR01T')
            product_price = soup.find_all('div', class_='_3I9_wc _27UcVY')
            product_offer = soup.find_all('div', class_='_3Ay6Sb')
            product_offer_price = soup.find_all('div', class_='_30jeq3 _1_WHN1')
            product_data = soup.find_all('a', class_='_1fQZEK')
            next_page = soup.find('div', class_='_2MImiq')
            _next = soup.find_all('a', class_='ge-49M')
            _page = soup.find_all('a', class_='_1LKTO3')
            current_page = next_page.find('span').text.split()[1]
            final_page = next_page.find('span').text.split()[3]
            if int(current_page) < int(final_page):
                count += 1
            elif int(current_page) >= int(final_page):
                continue_crawling = False
        except AttributeError as ex:
            logger.error('Attribute error occurred ')

        for i in zip(product_titles, product_price, product_offer, product_offer_price, product_data):
            name = re.sub("\(.*?\)", "()", i[0].text)
            product_name = name.replace('()', '').rstrip(' ')
            original_price = i[1].text.replace('₹', '').replace(',', '')
            offer_percentage = i[2].text.replace('off', '').replace('%', '')
            vendor_price = i[3].text.replace('₹', '').replace(',', '')
            product_url = 'https://www.flipkart.com' + i[4].get("href")

            create_offers(shop_id=1, product_name=product_name, original_price=original_price,
                          offer_percentage=offer_percentage,
                          vendor_price=vendor_price, product_url=product_url)


def crawl_e_websites(start_url):
    urls = [start_url.replace('%s', str(page)) for page in range(1, 3)]

    for url in urls:
        print('url: ', url)
        response = requests.get(url)
        soup = BeautifulSoup(response.content, 'html.parser')

        product_titles = soup.find_all('h3', class_='product-title plp-prod-title')
        product_offer_price = soup.find_all('span', attrs={'data-testid': 'new-price'})
        product_offer = soup.find_all('span', class_='discount discount-mob-plp')
        product_price = soup.find_all('span', attrs={'data-testid': 'old-price'})
        product_data = soup.find_all('div', class_='product-img')

        for i in zip(product_titles, product_price, product_offer, product_offer_price, product_data):
            name = re.sub("\(.*?\)", "()", i[0].text)
            name = name.replace('()', '').rstrip(' ')
            create_offers(shop_id=3, product_name=name,
                          original_price=i[1].text.replace('₹', '').replace(',', '').replace('MRP:', ''),
                          offer_percentage=i[2].text.replace('Off', '').replace('%', ''),
                          vendor_price=i[3].text.replace('₹', '').replace(',', '').replace('MRP:', ''),
                          product_url='https://www.croma.com' + i[4].next.get('href'))


def create_offers(shop_id, product_name, original_price, offer_percentage, vendor_price, product_url):
    with connection.cursor() as cursor:
        qry = "SELECT id, name FROM product_product WHERE name = (%s);"
        print('name: ', product_name)
        cursor.execute(qry, (product_name,))
        product = cursor.fetchone()
        if product is not None:
            query = '''INSERT into offer_offer(product_id, shop_id, actual_price, offer_percentage,
                    vendor_price, product_url, is_active, created_on,
                     updated_on) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s);'''
            values = (product[0], shop_id, original_price, offer_percentage, vendor_price, product_url, True,
                      datetime.now().strftime("%d/%m/%Y %H:%M:%S"),
                      datetime.now().strftime("%d/%m/%Y %H:%M:%S")
                      )
            print(cursor.query)
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
                # crawl_flipkart('https://www.flipkart.com/search?q=iphone+mobile&page=%s')
                # crawl_flipkart('https://www.flipkart.com/search?q=iphone+mobile&sid=tyy%2C4io&as=on&as-show=on'
                #                '&otracker=AS_QueryStore_OrganicAutoSuggest_1_12_na_na_na&otracker1'
                #                '=AS_QueryStore_OrganicAutoSuggest_1_12_na_na_na&as-pos=1&as-type=HISTORY&suggestionId'
                #                '=iphone+mobile%7CMobiles&requestId=7f1918b0-3b65-41c8-8ccd-676779e3e8c5&page=%s')

                crawl_flipkart('https://www.flipkart.com/search?q=android+mobile&sid=tyy%2C4io&as=on&as-show=on'
                               '&otracker=AS_QueryStore_OrganicAutoSuggest_1_4_na_na_na&otracker1'
                               '=AS_QueryStore_OrganicAutoSuggest_1_4_na_na_na&as-pos=1&as-type=RECENT&suggestionId'
                               '=android+mobile%7CMobiles&requestId=ebe59748-6602-4dc9-be53-081b951fd2f7&as-backfill'
                               '=on&page=%s')

            case 2:
                print('start scraping amazon')
                crawl_e_websites('https://www.amazon.in/s?i=electronics&rh=n%3A1389401031&fs=true&page=%s')
                # crawl_e_websites('https://www.amazon.in/s?i=electronics&rh=n%3A1389401031&fs=true&page=2')
                # urls = ['https://www.amazon.in/s?i=electronics&rh=n%3A1389401031&fs=true&page=%s'.replace('%s', str(page)) for page
                #         in range(1, 100 + 1)]

            case 3:
                print('start crawling crome')
                crawl_e_websites('https://www.croma.com/phones-wearables/mobile-phones/iphones/c/97')
