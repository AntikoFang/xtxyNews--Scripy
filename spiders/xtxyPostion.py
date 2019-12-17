# -*- coding: utf-8 -*-
"""
Created on Sun Nov 24 21:10:14 2019

@author: AntikoFng
"""
import scrapy
from xtxyNews.items import XtxynewsItem
from lxml import etree
from scrapy import Request
import xtxyNews.function as function

class XtxypostionSpider(scrapy.Spider):
    name = 'xtxyPostion'

    def start_requests(self):
        #allowed_domains = ['http://www.hbue.edu.cn/']
        #i = 1
        urls = ['http://xgxy.hbue.edu.cn/2627/list1.htm']
        for url in urls:
            yield Request(url = url, callback = self.parse)
            #yield Request(start_urls[0], meta={'url':start_urls[0]}, callback = self.parse)

    def parse(self, response):
        #url = response.meta['url']
        url = response.url
        hrefs1 = []
        data=function.get_data(url)
        selector=etree.HTML(data)
        # 标题链接
        hrefs = selector.xpath('//span[@class="Article_Title"]/a/@href')
        # 发布时间
        time = selector.xpath('//span[@class="Article_PublishDate"]/text()')
        # 判断发布时间是否为2019年，返回2019年发布的文章链接
        for i in range(len(hrefs)):
            if '2019' in time[i]:
                if hrefs[i][0] == '/':
                    hrefs1.append('http://xgxy.hbue.edu.cn' + hrefs[i])
                else:
                    print('error http')
        # 遍历进入链接获取信息
        for item in hrefs1:
            data_page = function.get_data(item)
            selector = etree.HTML(data_page)
            item = XtxynewsItem()
            item['title'] = selector.xpath('//title/text()')
            item['content'] = selector.xpath('//meta[2]/@content')

            yield item
            
        #翻页
        for i in range(2,4):
            next_url = 'http://xgxy.hbue.edu.cn/2627/list{}.htm'.format(i)
        yield scrapy.Request(next_url, callback = self.parse)
            
                
        
#scrapy runspider xtxyPostion.py -o xtxyNews.csv -t csv
#scrapy crawl xtxyPostion.py -o xtxy.csv
#scrapy crawl xtxyPostion