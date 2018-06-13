# -*- coding: utf-8 -*-
import scrapy
from shiyanlougithub.items import MultipageItem


class MultipageSpider(scrapy.Spider):
    name = 'multipage'

    @property
    def start_urls(self):
        url_tmp = 'https://github.com/shiyanlou?page={}&tab=repositories'
        urls = (url_tmp.format(i) for i in range(1, 2))
        return urls

    def parse(self, response):
        for rep in response.css('li.public'):
            item = MultipageItem()
        
            item['name'] = rep.xpath('.//a[@itemprop="name codeRepository"]/text()').re_first('\n\s*(.*)')
            item['update_time'] = rep.xpath('.//relative-time/@datetime').extract_first()
            print('--------------------{}-----------------------------'.format(item['update_time']))
           
            detail_href = rep.xpath('.//a[@itemprop="name codeRepository"]/@href').extract_first()

            github_detail_url = response.urljoin(detail_href)
            request = scrapy.Request(github_detail_url, callback=self.parse_detail)
            request.meta['item'] = item
            yield request

    def parse_detail(self, response):
        item = response.meta['item']
        for number in response.css('ul.numbers-summary li'):
            type_text = number.xpath('.//a/text()').re_first('\n\s*(.*)\n')
            number_text = number.xpath('.//span[@class="text-emphasized"]/text()').re_first('\n\s*(.*)\n')
            if type_text and number_text:
                number_text = number_text.replace(',', '')
                if type_text in ('commit', 'commits'):
                    item['commits'] = int(number_text)
                if type_text in ('branch', 'branches'):
                    item['branches'] = int(number_text)
                if type_text in ('release', 'releases'):
                    item['releases'] = int(number_text)
            yield item
