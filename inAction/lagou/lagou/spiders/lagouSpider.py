# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule

from lagou.items import LagouItem


class LagouspiderSpider(CrawlSpider):
    name = 'lagouSpider'
    allowed_domains = ['www.lagou.com']
    start_urls = ['https://www.lagou.com/']

    rules = (
        Rule(LinkExtractor(allow=r'www.lagou.com/zhaopin.*?')),
        Rule(LinkExtractor(allow=r'www.lagou.com/jobs/\d+.html'),callback='parse_item',follow=True),
    )

    def parse_item(self, response):
        i = LagouItem()
        url=response.url
        i["job_id"]
        i["title"]=response.xpath('//div[@class="position-content"]/div/div[@class="job-name"]/@title')
        i["url"]=response.url
        i["salary"]=response.xpath('//dd[@class="job_request"]/sapn[@class="salary"]/text()')
        i["job_city"]=response.xpath('//dd[@class="job_request"]/span')[1]
        i["work_years"]=response.xpath('//dd[@class="job_request"]/span')[2]
        i["degree_need"]=response.xpath('//dd[@class="job_request"]/span')[3]
        i["job_type"]=response.xpath('//dd[@class="job_request"]/span')[4]
        i["publish_time"]=response.xpath('//dd[@class="job_request"]/p[@class="publish_time"]/text()')
        i["job_advantage"]=response.xpath('//dd[@class="job-advantage"]/p/text()')
        i["job_desc"]=response.xpath('//dd[@class="job_bt"]/div/p/text()')
        city=response.xpath('//dd[@class="job-address clearfix"]/div[@class="work_addr"]/a/text()')[0]
        district=response.xpath('//dd[@class="job-address clearfix"]/div[@class="work_addr"]/a/text()')[1]
        road=response.xpath('//dd[@class="job-address clearfix"]/div[@class="work_addr"]/a/text()')[2]
        address=city+district+road
        i["job_addr"]=address
        i["company_url"]=response.xpath('//div[@class="content_r"]/d1[@class="job_company"]/dt/a/@href')
        i["company_name"]=response.xpath('//div[@class="content_r"]/d1[@class="job_compony"]/dt/img/@alt')
        #i['domain_id'] = response.xpath('//input[@id="sid"]/@value').extract()
        #i['name'] = response.xpath('//div[@id="name"]').extract()
        #i['description'] = response.xpath('//div[@id="description"]').extract()
        return i
