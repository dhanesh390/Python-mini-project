import os
import re
from datetime import datetime

import psycopg2
import requests
from schedule import repeat, run_pending, every
from background_task import background
from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.triggers.interval import IntervalTrigger
from bs4 import BeautifulSoup

from crawl_logger import logger
from e_product_comparison.e_crawler.crawler_constants import DIV, A, SPAN, HTML_PARSER, REPLACE, H_3, \
    NAME_SPLIT_PATTERN, FLIPKART_ANDROID_URL, FLIPKART_IPHONE_URL, DATABASE, USER, PASSWORD, HOST, PORT, MRP, PERCENTAGE
from e_product_comparison.e_crawler.crawler_constants import FLIPKART_URL, CROMA_URL, HREF, PRODUCT_SELECT_QUERY, \
    OFFER_INSERT_QUERY, DATE_TIME_FORMAT, CROMA_ANDROID_URL, CROMA_IPHONE_URL, RUPEE, CURVE_BRACKETS, EMPTY_STRING

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'e_product_comparison.settings')

connection = psycopg2.connect(database=DATABASE,
                              user=USER,
                              password=PASSWORD,
                              host=HOST,
                              port=PORT
                              )


def crawl_flipkart(start_url):
    count = 1
    continue_crawling = True
    while continue_crawling:
        try:
            url = start_url.replace(REPLACE, str(count))
            print('1: ', url)
            response = requests.get(url)
            soup = BeautifulSoup(response.content, HTML_PARSER)

            product_titles = soup.find_all(DIV, class_='_4rR01T')
            product_price = soup.find_all(DIV, class_='_3I9_wc _27UcVY')
            product_offer = soup.find_all(DIV, class_='_3Ay6Sb')
            product_offer_price = soup.find_all(DIV, class_='_30jeq3 _1_WHN1')
            product_data = soup.find_all(A, class_='_1fQZEK')
            next_page = soup.find(DIV, class_='_2MImiq')
            current_page = next_page.find(SPAN).text.split()[1].replace(',', EMPTY_STRING)
            final_page = next_page.find(SPAN).text.split()[3].replace(',', EMPTY_STRING)
            if int(current_page) < int(final_page):
                count += 1
            elif int(current_page) >= int(final_page):
                continue_crawling = False
        except AttributeError as ex:
            logger.error(f'{ex} as occurred ')
            continue_crawling = False
        else:
            for data in zip(product_titles, product_price, product_offer, product_offer_price, product_data):
                specifications = re.findall(NAME_SPLIT_PATTERN, data[0].text)
                color = ''
                storage = ''
                if specifications:
                    specification = specifications[0].replace('(', EMPTY_STRING).replace(')', EMPTY_STRING).split(',')
                    if len(specification) > 1:
                        color = specification[0].upper()
                        storage = specification[1].lstrip(' ').replace(' ', EMPTY_STRING).upper()
                    else:
                        color = specification[0].upper()
                name = re.sub(NAME_SPLIT_PATTERN, CURVE_BRACKETS, data[0].text)
                product_name = name.replace(CURVE_BRACKETS, EMPTY_STRING).rstrip(' ')
                original_price = data[1].text.replace(RUPEE, EMPTY_STRING).replace(',', EMPTY_STRING)
                offer_percentage = data[2].text.replace('off', '').replace(PERCENTAGE, EMPTY_STRING)
                vendor_price = data[3].text.replace(RUPEE, EMPTY_STRING).replace(',', EMPTY_STRING)
                product_url = FLIPKART_URL + data[4].get(HREF)

                create_offers(shop_id=1, product_name=product_name.upper(), original_price=original_price,
                              offer_percentage=offer_percentage,
                              vendor_price=vendor_price, product_url=product_url, color=color, storage=storage)


def crawl_e_websites(start_url):
    urls = [start_url.replace(REPLACE, str(page)) for page in range(1, 3)]

    for url in urls:
        print('url: ', url)
        response = requests.get(url)
        soup = BeautifulSoup(response.content, HTML_PARSER)
        product_titles = soup.find_all(H_3, class_='product-title plp-prod-title')
        product_offer_price = soup.find_all(SPAN, attrs={'data-testid': 'new-price'})
        product_offer = soup.find_all(SPAN, class_='discount discount-mob-plp')
        product_price = soup.find_all(SPAN, attrs={'data-testid': 'old-price'})
        product_data = soup.find_all(DIV, class_='product-img')

        for data in zip(product_titles, product_price, product_offer, product_offer_price, product_data):
            specifications = re.findall(NAME_SPLIT_PATTERN, data[0].text)
            specification = specifications[0].replace('(', EMPTY_STRING).replace(')', EMPTY_STRING).split(',')
            color = EMPTY_STRING
            storage = EMPTY_STRING
            if len(specification) > 1:
                color = specification[1].lstrip(' ').upper()
                storage = specification[0].upper()
            else:
                color = specification[1].upper()
            name = re.sub(NAME_SPLIT_PATTERN, CURVE_BRACKETS, data[0].text)
            name = name.replace(CURVE_BRACKETS, EMPTY_STRING).rstrip(' ')
            create_offers(shop_id=3, product_name=name.upper(),
                          original_price=data[1].text.replace(RUPEE, EMPTY_STRING).replace(',', EMPTY_STRING).replace(MRP, EMPTY_STRING),
                          offer_percentage=data[2].text.replace('Off', EMPTY_STRING).replace(PERCENTAGE, EMPTY_STRING),
                          vendor_price=data[3].text.replace(RUPEE, EMPTY_STRING).replace(',', EMPTY_STRING).replace(MRP, EMPTY_STRING),
                          product_url=CROMA_URL + data[4].next.get(HREF), color=color, storage=storage)


def create_offers(shop_id, product_name, original_price, offer_percentage, vendor_price, product_url, color, storage):
    with connection.cursor() as cursor:
        logger.info('connection established')
        cursor.execute(PRODUCT_SELECT_QUERY, (product_name, color, storage))
        product = cursor.fetchone()
        if product is not None:
            logger.info('matching product found')
            if product[2] == color and product[3] == storage:
                logger.info('product matching the specification found')
                query = OFFER_INSERT_QUERY
                values = (product[0], shop_id, original_price, offer_percentage, vendor_price, product_url, True,
                          datetime.now().strftime(DATE_TIME_FORMAT),
                          datetime.now().strftime(DATE_TIME_FORMAT)
                          )
                cursor.execute(query, values)
                connection.commit()
                logger.info('offer successfully created')
            else:
                pass

        else:
            pass


@repeat(every().day.at('17:25'))
def my_scrape():
    crawl_flipkart(FLIPKART_IPHONE_URL)
    crawl_flipkart(FLIPKART_ANDROID_URL)
    crawl_e_websites(CROMA_IPHONE_URL)
    crawl_e_websites(CROMA_ANDROID_URL)


while True:
    run_pending()

