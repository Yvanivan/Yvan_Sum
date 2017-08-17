#-*- coding:utf-8 _*-
""" 
@author:yvan 
@file: main.py 
@time: 2017/08/11 
"""
import sys


reload(sys)
sys.setdefaultencoding('utf8')

from scrapy import cmdline
# cmdline.execute("scrapy crawl livetext ".split())
cmdline.execute("scrapy crawl juzimi_spider ".split())

