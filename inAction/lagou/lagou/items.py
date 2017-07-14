# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class LagouItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    job_id=scrapy.Field()
    title=scrapy.Field()
    url=scrapy.Field()
    salary=scrapy.Field()
    job_city=scrapy.Field()
    work_years=scrapy.Field()
    degree_need=scrapy.Field()
    job_type=scrapy.Field()
    publish_time=scrapy.Field()
    job_advantage=scrapy.Field()
    job_desc=scrapy.Field()
    job_addr=scrapy.Field()
    company_url=scrapy.Field()
    compant_name=scrapy.Field()
