# -*- coding: utf-8 -*-
import scrapy
from scrapy import Item,Field
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule

class NewsItem(Item):
    title = Field()
    url = Field()
    text = Field()
    datetime = Field()
    source = Field()
    website = Field()

class ChinaSpider(CrawlSpider):
    name = 'china'
    allowed_domains = ['tech.china.com']
    start_urls = ['http://tech.china.com/articles/']

    rules = (
        Rule(LinkExtractor(allow='article\/.*\.html',
                           restrict_xpaths='//*[@id="left_side"]/div[2]/div[1]/a'), callback='parse_item'),
        Rule(LinkExtractor( restrict_xpaths='//*[@id="pageStyle"]/a[contains(.,"下一页")]')),
    )

    def parse_item(self, response):
        item = NewsItem()
        item['title'] = response.xpath('//*[@id="chan_newsTitle"]/text()').extract()
        item['url'] = response.url
        item['text'] = ''.join(response.xpath('//*[@id="chan_newsDetail"]//text()').extract()).strip()
        item['datetime'] = response.xpath('//*[@id="chan_newsInfo"]/text()').re_first('(\d+-\d+-\d+\s\d+:\d+:\d+)')
        item['source'] = response.xpath('//*[@id="chan_newsInfo"]/text()').re_first('来源：(.*)').strip()
        item['website'] = '中华网'
        print(item['text'])
        yield item
