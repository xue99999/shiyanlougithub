# -*- coding: utf-8 -*-
import scrapy
from shiyanlougithub.items import ShiyanlougithubItem


class RepositoriesSpider(scrapy.Spider):
    name = 'repositories'

    @property
    def start_urls(self):
        url_tmp = 'https://github.com/shiyanlou?page={}&tab=repositories'
#        url_tmp = "https://github.com/shiyanlou?page={}&tab=repositories"
        urls = (url_tmp.format(i) for i in range(1, 5))
        return urls

    def parse(self, response):
        for rep in response.css('li.public'):
            yield ShiyanlougithubItem({
                'name': rep.xpath('.//a[@itemprop="name codeRepository"]/text()').re_first('\n\s*(.*)'),
                'update_time': rep.xpath('.//relative-time/@datetime').extract_first()
                })
