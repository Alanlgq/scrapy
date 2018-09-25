# -*- coding: utf-8 -*-
import scrapy
import os

class PItem(scrapy.Item):
    image_urls = scrapy.Field()
    images = scrapy.Field()

class MeizaiSpider(scrapy.Spider):
    name = 'meizai'
    allowed_domains = ['www.meizitu.com']
    start_urls = ['http://www.meizitu.com/a/sexy_1.html']

    # url = 'http://www.meizitu.com/a/list_1_1.html'

    def parse(self, response):
        # exp = '//div[@id="wp_page_numbers"]//a[text()="下一页"]/@href'
        # _next = response.xpath(exp).extract_first()
        img = response.css('.inWrap .navigation #wp_page_numbers').extract_first() #翻页（页码）位置
        pages = 1
        for page in range(1, pages + 1):
            url = 'http://www.meizitu.com/a/sexy_'+str(page)+'.html'
            os.makedirs('xxoo', exist_ok=True)  # 创建文件夹
            os.chdir('xxoo')
        # for p in response.xpath('//li[@class="wp-item"]//a/@href').extract():
        for p in response.css('.inWrap .wp-item a::attr(href)').extract():   #定位到图片组头
            yield scrapy.FormRequest(p,callback=self.parse_item)



    def parse_item(self,response):
        item = PItem()
        # urls = response.xpath('//div[@id="picture"]//img/@src').extract()
        urls = response.css('.postContent #picture img::attr(src)').extract()  #定位到图片
        item['image_urls'] = urls
        return item
