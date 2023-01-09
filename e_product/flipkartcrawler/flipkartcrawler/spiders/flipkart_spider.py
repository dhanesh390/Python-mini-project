import scrapy


class FlipKartOffer(scrapy.Spider):
    name = 'flipkart'
    allowed_domains = ['flipkart.com']
    start_urls = ['https://www.flipkart.com/mobiles/pr?sid=tyy%2C4io&p%5B%5D=facets.brand%255B%255D%3Drealme&p%5B%5D=facets.availability%255B%255D%3DExclude%2BOut%2Bof%2BStock&param=7564&ctx=eyJjYXJkQ29udGV4dCI6eyJhdHRyaWJ1dGVzIjp7InRpdGxlIjp7Im11bHRpVmFsdWVkQXR0cmlidXRlIjp7ImtleSI6InRpdGxlIiwiaW5mZXJlbmNlVHlwZSI6IlRJVExFIiwidmFsdWVzIjpbIlNob3AgTm93Il0sInZhbHVlVHlwZSI6Ik1VTFRJX1ZBTFVFRCJ9fX19fQ%3D%3D&otracker=clp_metro_expandable_1_3.metroExpandable.METRO_EXPANDABLE_Shop%2BNow_mobile-phones-store_Q1PDG4YW86MF_wp2&fm=neo%2Fmerchandising&iid=M_4fcaa499-c7a8-4e11-85c2-4ac7ee87cb42_3.Q1PDG4YW86MF&ppt=hp&ppn=homepage&ssid=kiklrsqqrk0000001673236915550&page=1']

    def parse(self, response):
        # Product = response.xpath('//div[@class="hGSR34"]/text()').extract()
        product = response.xpath('//div[@class="_4rR01T"]/text()').extract()
        original_price = response.xpath('//div[@class="_3I9_wc _27UcVY"]/text()').extract()
        offer_percentage = response.xpath('//div[@class="_3Ay6Sb"]/text()').extract()
        offer_price = response.xpath('//div[@class="_30jeq3 _1_WHN1"]/text()').extract()

        row_data = zip(product, original_price, offer_percentage, offer_price)
        for item in row_data:
            details = {'product': item[0], 'original_price': item[1],
                       'offer_percentage': item[2], 'offer_price': item[3]}
            yield details

