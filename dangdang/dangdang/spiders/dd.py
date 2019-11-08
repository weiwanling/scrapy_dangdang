# -*- coding: utf-8 -*-
import scrapy
import lxml
from dangdang.items import DangdangItem
'''
scrapy框架爬取当当网上商品的标题评论价格等
爬取网址：http://category.dangdang.com/pg1-cid4010013.html
可翻页默认爬取5页，每页48个商品
'''
class DdSpider(scrapy.Spider):
    name = 'dd'
    page_num=5           #指定爬取页数
    #allowed_domains = ['dangdang.com']
    def start_requests(self):
        start_urls = []        #url列表
        for i in range(1,self.page_num+1):
            url = 'http://category.dangdang.com/pg' + str(i) + '-cid4010013.html'  #构造url
            start_urls.append(url)

        for url in start_urls:
            yield  scrapy.Request(url=url,callback=self.parse)       #一次提交一个



    def parse(self, response):
        items=DangdangItem()

        #xpath提取信息
        items['title']=response.xpath('//a[@name="itemlist-title"]/@title').extract()
        items['link']=response.xpath('//a[@name="itemlist-title"]/@href').extract()
        items['comment']=response.xpath('//a[@name="itemlist-review"]/text()').extract()
        items['price']=response.xpath('//span[@class="price_n"]/text()').extract()
        items['shop']=response.xpath('//a[@name="itemlist-shop-name"]/@title').extract()

        #print(items)
        yield  items   #提交给items



