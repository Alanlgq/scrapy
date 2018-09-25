# -*- coding: utf-8 -*-
import scrapy
import requests
import json
from ..items import ZhilianscrapyItem
from bs4 import BeautifulSoup
import re



class ZhilianSpider(scrapy.Spider):
    name = 'zhilian'
    allowed_domains = ['www.zhaopin.com']
    start_urls = ['http://www.zhaopin.com/']


    def start_requests(self):
        for num in range(30):
            url = 'https://sou.zhaopin.com/?pageSize=60&jl=%E4%B8%8A%E6%B5%B7&kw=%E6%95%B0%E6%8D%AE%E5%88%86%E6%9E%90&kt=3'.format(num)
            yield scrapy.Request(url, callback=self.parse)

    def parse(self, response):
        wbdata = response.text
        # soup = BeautifulSoup(wbdata, 'lxml')
        # job_title = soup.select("table.newlist > tr > td.zwmc > div > a:nth-of-type(1)")  # job_title

        pattern = re.compile('<td class="zwmc".*?href="(.*?)" target="_blank">(.*?)</a>.*?')
        print(pattern)