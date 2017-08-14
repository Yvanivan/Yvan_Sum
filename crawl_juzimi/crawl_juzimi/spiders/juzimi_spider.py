# -*- coding: utf-8 -*-
import scrapy
from scrapy.http import Request

filew = open('res.txt','a')
class JuzimiSpiderSpider(scrapy.Spider):
    name = "juzimi_spider"
    start_urls = ['http://www.juzimi.com/ju/1137']

    def parse(self, response):
        res = response.xpath("//meta[@name='description']/@content").extract()[0]
        print res
        filew.write(res+'\n')
        nexturl = 'http://www.juzimi.com'+response.xpath("//div[@class='nextlinks']/a/@href").extract()[0]
        yield Request(nexturl)
        pass
