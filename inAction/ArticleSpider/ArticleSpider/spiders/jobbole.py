# -*- coding: utf-8 -*-
import scrapy
import re
import datetime
from scrapy.http import Request
from urllib import parse
from ArticleSpider.items import ArticlespiderItem
from ArticleSpider.items import ArticleItemLoader
from ArticleSpider.utils.common import get_md5

class JobboleSpider(scrapy.Spider):
    name = "jobbole"
    allowed_domains = ["python.jobbole.com"]
    start_urls = (
        'http://python.jobbole.com/all-posts/',
    )

    def parse(self, response):
        """
        1.获取文章列表页中的文章url并交给scrapy下载后并进行解析
        2.获取下一页的url并交给scrapy进行下载，下载完成后交给parse
        """
        #解析列表页中的所有文章url并交给scrapy下载后进行解析
        post_nodes=response.css("#archive .floated-thumb .post-thumb a")
        for post_node in post_nodes:
            image_url =post_node.css("img::attr(src)").extract_first("")
            post_url =post_node.css("::attr(href)").extract_first("")
            yield Request(url=parse.urljoin(response.url,post_url),meta={"front_image_url":image_url},callback=self.parse_detail)
            '''parse.urljoin(response.url,post_url) 补全域名'''
        #提取下一页并交给scrapy进行下载
        next_url=response.css(".next.page-numbers::attr(href)").extract_first("")
        if next_url:
            yield Request(url=parse.urljoin(response.url,next_url),callback=self.parse)

    def parse_detail(self,response):
        article_item=ArticlespiderItem()
        front_image_url=response.meta.get("front_image_url","")
        item_loader=ArticleItemLoader(item=ArticlespiderItem(),response=response)
        item_loader.add_css("title",".entry-header h1::text")
        item_loader.add_value("url", response.url)
        item_loader.add_value("url_object_id", get_md5.get_md5(response.url))
        item_loader.add_css("create_date", "p.entry-meta-hide-on-mobile::text")
        item_loader.add_value("front_image_url", [front_image_url])
        item_loader.add_css("parise_nums", ".vote-post-up h10::text")
        item_loader.add_css("comment_nums", "a[href='#article-comment'] span::text")
        item_loader.add_css("fav_nums", ".bookmark-btn::text")
        item_loader.add_css("tags", "p.entry-meta-hide-on-mobile a::text")
        item_loader.add_css("content", "div.entry")
        article_item=item_loader.load_item()
        yield article_item
