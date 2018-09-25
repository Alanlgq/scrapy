# -*- coding: utf-8 -*-
import scrapy
from urllib.parse import quote
from ..items import TaobaoscrapyItem


class TaobaoSpider(scrapy.Spider):
    name = 'taobao'
    allowed_domains = ['www.taobao.com']
    start_urls = ['http://www.taobao.com/']

    # base_url = 'https://s.taobao.com/search?q=%E6%89%8B%E6%9C%BA&stats_click=search_radio_all&cps=yes&s=0&app=vproduct&cd=false&v=auction&tab=all&vlist=1'
    base_url = 'https://s.taobao.com/search?q='

    def start_requests(self):
        for i in self.settings.get('KEYWORD'):
            url = self.base_url + quote(i)
        for pn in range(1, self.settings.get('MAXPAGE')+1):
            yield scrapy.Request(url=url, callback=self.parse, meta={'page':pn}, dont_filter=True)

    def parse(self, response):
        # print(response.url)
        results = response.xpath('//div[@class="items"]/div[contains(@class,"item")]')
        results2 = response.xpath('//div[@class="grid"]/div[contains(@class,"item")]')
        # results = response.css('.items .item')
        for result in results:
            item = TaobaoscrapyItem()
            item['price'] = result.xpath('.//div[contains(@class,"price")]/strong/text()').extract_first()
            item['deal'] = result.xpath('.//div[@class="deal-cnt"]/text()').extract_first()
            item['name'] = result.css('.pic img::attr(alt)').extract_first()
            item['shop'] = ''.join(result.xpath('.//div[@class="shop"]/a/span/text()').extract()).strip()
            item['location'] = result.xpath('.//div[@class="location"]/text()').extract_first()
            yield item
        for re in results2:
            item = TaobaoscrapyItem()
            item['price'] = re.xpath('.//div[contains(@class,"price")]/strong/text()').extract_first()
            item['deal'] = re.xpath('.//div[@class="deal-cnt"]/text()').extract_first()
            item['name'] = re.css('.pic img::attr(alt)').extract_first()
            item['shop'] = ''.join(re.xpath('.//div[@class="shop"]/a/span/text()').extract()).strip()
            item['location'] = re.xpath('.//div[@class="location"]/text()').extract_first()
            yield item








        #
        # for result in results:
        #     item = TaobaoscrapyItem()
        #     # 提取价格
        #     item['price'] = result.xpath('.//div[contains(@class,"price")]/strong/text()').extract_first()
        #     # 交易数量
        #     item['deal'] = result.xpath('.//div[@class="deal-cnt"]/text()').extract_first()
        #     # 商店位置
        #     item['location'] = result.xpath('.//div[@class="location"]/text()').extract_first()
        #     # 商店名
        #     item['shop'] = ''.join(result.xpath('.//div[@class="shop"]/a/span/text()').extract()).strip()
        #     # 产品描述
        #     item['name'] = ''.join(result.xpath('.//div[contains(@class,"title")]/a//text()').extract()).strip()
        #     yield item
        #


