# -*- coding: utf-8 -*-
import scrapy
from douban.items import DoubanItem

class BookSpider(scrapy.Spider):
    name = 'book'
    allowed_domains = ['book.douban.com']
    start_urls = ['https://book.douban.com/tag/']

    def parse(self, response):
        item = DoubanItem()
        item["arts"] = response.xpath('//a[@name="文学"]/@name').extract_first()  # 文学
        # print(item)
        arts_target = response.xpath('//div[@class=""]/div[1]//table[1]/tbody/tr//td')
        # print(arts_target)
        for art in arts_target:
            item["WenXue"] = "https://book.douban.com" + art.xpath('./a/@href').extract_first()
            yield scrapy.Request(item["WenXue"], callback=self.parse_detail, meta={"item": item})

    def parse_detail(self, response):
        item = response.meta["item"]
        item["name"] = response.xpath('//div[@class="info"]/h2/a/@title').extract()
        yield item
        print(item)

