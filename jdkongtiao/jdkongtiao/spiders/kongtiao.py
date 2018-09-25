# -*- coding: utf-8 -*-
import scrapy
import re
import json
from ..items import JdkongtiaoItem


class KongtiaoSpider(scrapy.Spider):
    name = 'kongtiao'
    allowed_domains = ['www.jd.com']
    start_urls = ['http://www.jd.com/']

    url = 'https://search.jd.com/Search?keyword=%E7%A9%BA%E8%B0%83&enc=utf-8&wq=%E7%A9%BA%E8%B0%83&pvid=e393b36d8d0a4c21acac470d972cbef6'

    def start_requests(self):
        yield scrapy.Request(url=self.url, callback=self.parse_product, dont_filter=True)

    def parse_product(self, response):
        productIds = response.css('#J_goodsList .gl-warp li::attr(data-sku)').extract()
        productIds = list(set(productIds))
        # print(productIds)
        # productIds = ['1993092']
        for productId in productIds:
            url = 'https://sclub.jd.com/comment/productPageComments.action?callback=fetchJSON_comment98vv137009&productId='+productId+'&score=0&sortType=5&page=0&pageSize=10&isShadowSku=0&fold=1'
            yield scrapy.Request(url=url, callback=self.parse_page, dont_filter=True)

    def parse_page(self, response):
        # re.compile定义正则表达式
        pattern = re.compile('"maxPage":(\d+)', re.S)
        # re.search用正则表达式去匹配pattern 第2个内容
        page = int(re.search(pattern, response.text).group(1))
        for ye in range(page):
            #用正则表达式对产品ID进行提取，拼接成每页新的URL
            productId = re.search('&productId=(.*?)&', response.url).group(1)
            url = 'https://sclub.jd.com/comment/productPageComments.action?callback=fetchJSON_comment98vv206962&productId='+ productId +'&score=0&sortType=5&page='+ str(ye) +'&pageSize=10&isShadowSku=0&fold=1'
            yield scrapy.Request(url=url, callback=self.parse_info, dont_filter=True)

    def parse_info(self, response):
        # print(response.text)
        html = response.text.replace('fetchJSON_comment98vv206962(', '')
        html = html.replace(');', '')
        product = json.loads(html)
        comments = product['comments']
        for comment in comments:
            item = JdkongtiaoItem()
            item['content'] = comment['content']       #评论
            item['id'] = comment['id']      #产品ID
            item['referenceName'] = comment['referenceName']     #产品名字
            item['productColor'] = comment['productColor']       #产品匹数
            item['productSize'] = comment['productSize']         #产品类型
            yield item

    def parse(self, response):
        pass
