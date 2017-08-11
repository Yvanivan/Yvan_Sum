# -*- coding: utf-8 -*-
import scrapy


class JuzimiSpiderSpider(scrapy.Spider):
    name = "juzimi_spider"
    start_urls = ['http://www.juzimi.com/ju/597389']

    def parse(self, response):
        print response.xpath("//meta[@name='description']/@content").extract()[0]
        pass
