# -*- coding: utf-8 -*-
import scrapy
from shiyanlougithub.items import MultipageItem


class MultipageSpider(scrapy.Spider):
    name = 'multipage'

    @property
    def start_urls(self):
        url_tmp = 'https://github.com/shiyanlou?page={}&tab=repositories'
        urls = (url_tmp.format(i) for i in range(1, 5))
        return urls

    def parse(self, response):
        for rep in response.css('li.public'):
            item = MultipageItem()
        
            item['name'] = rep.xpath('.//a[@itemprop="name codeRepository"]/text()').re_first('\n\s*(.*)')
            item['update_time'] = rep.xpath('.//relative-time/@datetime').extract_first()
           
            detail_href = rep.xpath('.//a[@itemprop="name codeRepository"]/@href').extract_first()

            github_detail_url = response.urljoin(detail_href)
            request_url = scrapy.Request(github_detail_url, callback=self.parse_detail)
            request.meta['item'] = item
            yield request

    def parse_detail(self, response):
        item = request.meta['item']
        item['commits'] = response.xpath(('(.//span[@class="text-emphasized"])[1]/text()').extract_first()
        item['branches'] = response.xpath(('(.//span[@class="text-emphasized"])[2]/text()').extract_first()
        item['releases'] = response.xpath(('(.//span[@class="text-emphasized"])[3]/text()').extract_first()
        yield item