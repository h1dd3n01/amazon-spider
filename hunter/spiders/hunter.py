from scrapy.spiders import CrawlSpider
from scrapy import FormRequest, Request
from ..items import HunterItem
from ..meta import *
import time


class Hunter(CrawlSpider):
    name = 'hun73r'
    start_urls = ['https://www.laptopoutlet.co.uk']
    product_list = []

    def __init__(self, product_type=None, brand=None, screensize=None):
        self.type = product_type
        self.brand = brand
        self.screensize = screensize
        super(Hunter, self).__init__()

    def parse(self, response):
        typeList = []
        brandList = []
        screensizeList = []
        product_type = ''
        product_brand = ''
        product_screensize = ''

        start_point = response.css('.header-bottom-wrap>div>div>div>form')

        # ----------------- Start type check ---------------------------------
        if self.type is not None:
            for element in start_point.css('#type_div>select>option').extract():
                if self.type.lower() in element.lower():
                    product_type = element.split('"')[1]
                    break
                val = element.split('>')[1]
                val = val.split('<')[0]
                typeList.append(val)
            if product_type == '' and self.type is not None:
                print('Available device types are...')
                for i in typeList[1:]:
                    print(i)

        # ------------------ End type Check -----------------------------------

        # ----------------- Start brand check ---------------------------------
        if self.brand is not None:
            for element in start_point.css('#brand_div>select>option').extract():
                if self.brand.title() in element:
                    product_brand = element.split('"')[1]
                    break
                    # Do not remove! it will brake.
                if self.brand in element:
                    product_brand = element.split('"')[1]
                    break
                val = element.split('>')[1]
                val = val.split('<')[0]
                brandList.append(val)
        if product_brand == '' and self.brand is not None:
            print('Available brands are...')
            for i in brandList[1:]:
                print(i)
                print('--------')

        # ------------------ End brand Check -----------------------------------

        # ----------------- Start screensize check ---------------------------------
        if self.screensize is not None:
            for element in start_point.css('#type_div>select>option').extract():
                if self.screensize in element:
                    product_screensize = element.split('"')[1]
                    break
                val = element.split('>')[1]
                val = val.split('<')[0]
                screensizeList.append(val)
            if product_screensize == '' and self.screensize is not None:
                print('Available core types are...')
                for i in screensizeList[1:]:
                    print(i)
                    print('--------')

        # ------------------ End type Check -----------------------------------

        url = 'https://www.laptopoutlet.co.uk/catalogsearch/advanced/result/?type={}&brand={}&' \
              'processor=&screensize={}&price_range=&price[from]=&price[to]='. \
            format(product_type, product_brand, product_screensize)
        yield Request(url=url, callback=self.parse_form_data)

    def parse_form_data(self, response):

        start_point = response.css('.main-container>div>.col-main>.category-products>ul')

        for li in start_point.css('.item'):
            item = {'title': li.css('.border-right>.product-info>h2>a::text').extract_first(),
                    'price': li.css('.border-right>.price-box>span>.price::text').extract_first()}

            if item['price'] is None:
                item['price'] = li.css('.border-right>.price-box>p>.price::text').extract_first()

            item = parse_meta(item, self.brand)
            if int(item['price']) > 100:
                self.product_list.append(item)

            pagination = response.css('.main-container>div>.col-main>'
                                      '.category-products>.toolbar-bottom'
                                      '>div>.pager>.pages>ol>li:last-child>a::attr(href)').extract_first()
            if pagination is not None:
                yield Request(pagination, callback=self.parse_form_data)
            else:
                yield Request(url='https://www.amazon.com/', callback=self.amazon_request_start)

    def amazon_request_start(self, response):
        req = 1
        for i in self.product_list:
            title = i['title'] + ' ' + i['ssd'] if i['cpu'] is '' else \
                i['title'] + ' ' + i['cpu'] + ' ' + i['year']
            yield FormRequest.from_response(
                response,
                formname='site-search',
                formdata={'field-keywords': title},
                meta={'item': i, 'depth': 10},
                callback=self.start_amazon_search
            )
            print('Started request #' + str(req))
            req += 1
            time.sleep(1)

    def start_amazon_search(self, response):

        not_found = response.css('.s-desktop-width-max>div:nth-child(2)>div>span:nth-child(4)>div>span'
                                 '>div>div>h1>span::text').extract_first()
        if not_found is not None:
            print('Product not found ' + response.meta['item']['title'])
            return

        start_point = response.css('#search>.s-desktop-width-max>div:nth-child(2)>div>span:nth-child(5)'
                                   '>div>div>div>span>div>div>div:nth-child(2)')

        item = HunterItem()
        item['main_item'] = {'title': response.meta['item']['title'],
                             'ssd': response.meta['item']['ssd'],
                             'cpu': response.meta['item']['cpu'],
                             'price': response.meta['item']['price'],
                             'ram': response.meta['item']['ram']}

        for i in start_point:
            title = i.css('div:nth-child(2)>div>div:nth-child(1)>div>div>div>h2>a>span::text').extract_first() or None
            url = i.css('div:nth-child(2)>div>div:nth-child(1)>div>div>div>h2>a::attr(href)').extract_first() or None
            price = i.css(
                'div:nth-child(2)>div>div:nth-child(2)>div>'
                'div>div>div>div>a>span>.a-offscreen::text').extract_first() or None

            if price is not None:
                sample = {'title': title,
                          'price': price}
                sample = parse_meta(sample, self.brand)
                item['secondary_item'] = {'title': sample['title'],
                                          'price': sample['price'],
                                          'ssd': sample['ssd'],
                                          'cpu': sample['cpu'],
                                          'ram': sample['ram'],
                                          'url': 'https://www.amazon.com/{}'.format(url)}
                yield item

        pagination = response.css('.s-desktop-width-max>div:nth-child(2)>div>span:nth-child(10)'
                                  '>div>div>span>div>div>ul>.a-last>a::attr(href)').extract_first()

        if pagination is not None:
            current_page = pagination[-1]
            if int(current_page) <= 5 or current_page is '':
                yield Request('https://www.amazon.com' + pagination, callback=self.start_amazon_search)

        # print('-'*20)
        # for i in self.final_product_list:
        #     for k, v in i.items():
        #         print('{} - {}'.format(k, v))
        # print('-' * 20)
