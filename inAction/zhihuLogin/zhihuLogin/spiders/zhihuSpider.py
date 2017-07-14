# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from scrapy.selector import Selector

from scrapy.http import Request,FormRequest
from zhihuLogin.items import ZhihuloginItem

from zhihuLogin.items import ZhihuloginItem


class ZhihuspiderSpider(CrawlSpider):
    name = 'zhihuSpider'
    allowed_domains = ['www.zhihu.com']
    start_urls = ['http://www.zhihu.com/']

    rules = (
        Rule(LinkExtractor(allow=('/question/\d+#.*?',)),callback='parse_page',follow=True),
        Rule(LinkExtractor(allow='/question/\d+',), callback='parse_item', follow=True),
    )
    headers={
        "Accept":"*/*",
        "Accept-Encoding":"gzip,deflate",
        "Accept-Language":"en-US,en;q=0.8,zh-TW;q=0.6,zh;q=0.4",
        "Connection":"keep-alive",
        "Connection-Type":"application/x-www-form-urlencoded;charset=UTF-8",
        "User-Agent":"Mozilla/5.0(Macintosh;Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/38.0.2125.111 Safari/537.36",
        "Referer":"http://www.zhihu.com/"
    }

    def start_requests(self):
        return [Request(url="http://www.zhihu.com/#signin", headers=self.headers,meta={'cookiejar':1},callback= self.post_login)]

    def post_login(self,response):
        print("Preparing login")
        xsrf=Selector(response).xpath('//input[@name="_xsrf"]/@value').extract()[0]
        print(xsrf)
        #FormRequest.form_response是Scrapy提供的一个函数，用于post表单
        #登录成功后，会调用after_login回调函数
        return scrapy.FormRequest(
                             url='http://www.zhihu.com/login/email',
                             meta={'cookiejar':response.meta['cookiejar']},
                             headers=self.headers,
                             formdata={
                                '_xsrf':xsrf,
                                'account':'1095511864@qq.com',
                                'password':'123456',
                                'remember_me': 'true',
                             },
                             callback=self.after_login
                            )

    def after_login(self,response):
        print("SUCCESS")

    def pasre_page(self,response):
        problem=Selector(response)
        item=ZhihuloginItem()
        item['url']=response.url
        item['name']=problem.xpath('/span[@class="name"]/text()').extract()
        print(item['name'])
        item['title']=problem.xpath('//h2[@class="zm-item-title zm-editable-content"]/text()').extract()
        item['description']=problem.xpath('//div[@class="zm-editable-content"]/text()').extract()
        item['answer']=problem.xpath('//div[@class="zm-editable-content clearfix"]/text()').extract()
        yield item
    def parse_item(self, response):
        i = ZhihuloginItem()
        #i['domain_id'] = response.xpath('//input[@id="sid"]/@value').extract()
        #i['name'] = response.xpath('//div[@id="name"]').extract()
        #i['description'] = response.xpath('//div[@id="description"]').extract()
        return i
