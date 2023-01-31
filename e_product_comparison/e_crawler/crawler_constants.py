DATABASE = 'product_e'
USER = 'postgres'
PASSWORD = 'dhanesh@22'
HOST = 'localhost'
PORT = '5432'
DIV = 'div'
A = 'a'
SPAN = 'span'
H_3 = 'h3'
MRP = 'MRP:'
PERCENTAGE = '%'
RUPEE = '₹'
CURVE_BRACKETS = '()'
EMPTY_STRING = ''
HTML_PARSER = 'html.parser'
REPLACE = '%s'
NAME_SPLIT_PATTERN = "\(.*?\)"
CROMA_URL = 'https://www.croma.com'
FLIPKART_URL = 'https://www.flipkart.com'
HREF = "href"
# PRODUCT_SELECT_QUERY = "SELECT id, name, specification FROM product_product WHERE name = (%s)"
PRODUCT_SELECT_QUERY = "SELECT id, name, specification->>'color' AS color, specification->>'storage' AS storage FROM " \
                        "product_product WHERE name = (%s) AND specification->>'color' = (%s) AND " \
                        "specification->>'storage' = (%s)"
OFFER_SELECT_QUERY = "SELECT * from offer_offer WHERE product_id = (%s) AND shop_id = (%s) AND " \
                                 "actual_price = (%s) AND offer_percentage = (%s) AND vendor_price = (%s)"
OFFER_INSERT_QUERY = '''INSERT into offer_offer(product_id, shop_id, actual_price, offer_percentage,
                        vendor_price, product_url, is_active, created_on,
                         updated_on) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s);'''
DATE_TIME_FORMAT = "%d/%m/%Y %H:%M:%S"
FLIPKART_IPHONE_URL = 'https://www.flipkart.com/search?q=iphone+mobile&page=%s'
FLIPKART_ANDROID_URL = 'https://www.flipkart.com/search?q=android+mobile&page=%s'
CROMA_IPHONE_URL = 'https://www.croma.com/phones-wearables/mobile-phones/iphones/c/97'
CROMA_ANDROID_URL = 'https://www.croma.com/phones-wearables/mobile-phones/android-phones/c/95'
AMAZON_ELECTRONICS_URL = 'https://www.amazon.in/s?i=electronics&rh=n%3A1389401031&fs=true&page=%s'