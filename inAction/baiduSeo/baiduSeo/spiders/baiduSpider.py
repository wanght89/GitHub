# -*- coding: utf-8 -*-
import scrapy
import pymysql
from baiduSeo.items import BaiduseoItem
from scrapy.http import Request

class BaiduspiderSpider(scrapy.Spider):
    name = "baiduSpider"
    allowed_domains = ["zhidao.baidu.com"]
    start_urls = (
        "http://zhidao.baidu.com/question/647795152324593805.html", #python
        "http://zhidao.baidu.com/question/23976256.html", #database
        "http://zhidao.baidu.com/question/336615223.html", #C++
        "http://zhidao.baidu.com/question/251232779.html", #operator system
        "http://zhidao.baidu.com/question/137965104.html"  #Unix programing
    )
    #add database
    connDataBase=pymysql.connect(host="127.0.0.1",user="root",passwd="root",db="zhidaodb")
    cDataBase=connDataBase.cursor()
    sql = "CREATE TABLE IF NOT EXISTS infoLib (id int(4) primary key not null auto_increment,name text,url text,html text)"
    cDataBase.execute(sql)
    sql2 = "CREATE TABLE IF NOT EXISTS urlLib (url varchar(255) primary key not null)"
    cDataBase.execute(sql2)

    def parse(self, response):
        item=BaiduseoItem()
        pageName=response.xpath('//title/text()').extract()[0]   #解析爬取网页中的名称
        pageUrl=response.xpath('//head/link[@rel="canonical"]').re('href="(.*?)"')[0]     #解析爬取网页的url，并不是直接使用函数获取，那样或夹杂乱码
        pageHtml=response.xpath('//div/pre[@class="best-text mb-10"]/text()').extract()[0]          #解析网页html
        #judge whether pageUrl in cUrl
        # 若当前url是start_url中的一员，进行该判断的原因是，我们对重复的start_url中的网址仍然进行爬取，而对非start_url中曾今爬取过的网页将不再爬取
        if pageUrl in self.start_urls:
            sql="SELECT * FROM urlLib where url =(%s)"
            self.cDataBase.execute(sql,(pageUrl,))
            lines=self.cDataBase.fetchall()
            if len(lines):
                pass
            else:
                self.cDataBase.execute('INSERT INTO urlLib(url) VALUES(%s)',(pageUrl,))
                item["name"]=pageName
                item["url"]=pageUrl
                item["html"]=pageHtml
        else:
            self.cDataBase.execute('INSERT INTO urlLib(url) VALUES(%s)',(pageUrl,))
            item["name"] = pageName
            item["url"] = pageUrl
            item["html"] = pageHtml
        self.connDataBase.commit()
        yield item
        #抓取出所有该网页的延伸网页，进行判断并对未爬取的网页进行爬取
        for sel in response.xpath("//ul/li/a").re('href="(/question/.*?.html\?.*?)"'):
            sel = "http://zhidao.baidu.com" + sel
            self.cDataBase.execute("SELECT * FROM urlLib where url=(%s)", (sel,))
            lines = self.cDataBase.fetchall()
            if len(lines) == 0:
                yield Request(url=sel, callback=self.parse)




