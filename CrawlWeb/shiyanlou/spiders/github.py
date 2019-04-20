# -*- coding: utf-8 -*-
import scrapy
from shiyanlou.items import ShiyanlouItem
import time

class GithubSpider(scrapy.Spider):
    name = 'github'
    allowed_domains = ['github.com']
    initial = input("Enter username: ")
    @property
    def start_urls(self, initial=initial):
        result = ('https://github.com/{}?tab=repositories'.format(initial),)
        return result

    def parse(self, response):
        repos = response.xpath('//li[@itemprop="owns"]')

        for repo in repos:
            item = ShiyanlouItem()
            item["repo_name"] = repo.xpath(".//a[@itemprop='name codeRepository']/text()").extract_first().strip()
            item["update_time"] = repo.xpath(".//relative-time/@datetime").extract_first()

            yield item

        # next page
        # spans = response.css('div.pagination span.disabled::text')
 
        # if len(spans) == 0 or spans[-1].extract() != 'Next':
        #     next_url = response.css('div.paginate-container a:last-child::attr(href)').extract_first()
        #     # next_url = response.css("div.pagiation-container a:last-child::attr(href)").extract_first()
        #     yield response.follow(next_url, callback=self.parse)

        pages = response.css("div.paginate-container a:last-child::text")
        
        if  pages.extract_first() == "Next":
            next_url = response.css("div.paginate-container a:last-child::attr(href)").extract_first()

            yield response.follow(next_url, callback=self.parse)