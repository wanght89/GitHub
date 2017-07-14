# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy
import datetime
import re
import w3lib
from scrapy.loader import ItemLoader
from scrapy.loader.processors import MapCompose,TakeFirst,Join
from ArticleSpider.utils.common import extract_num
from ArticleSpider.settings import SQL_DATETIME_FORMAT,SQL_DATE_FORMAT
from w3lib.html import remove_tags
def add_jobbole(value):
    return value+"-bobby"

def date_covert(value):
    try:
        create_date=datetime.datetime.strptime(value,'%Y/%m/%d').date()
    except Exception as e:
        create_date=datetime.datetime.now().date()
    return create_date

def get_nums(value):
    match_re=re.match(",*?(\d+).*",value)
    if match_re:
        nums=int(match_re.group(1))
    else:
        nums=0
    return nums

def return_value(value):
    return value

def remove_comment_tag(value):
    #去掉tag中提取的评论
    if "评论" in value:
        return ""
    else:
        return value


class ArticleItemLoader(ItemLoader):
    # define the fields for your item here like:
    # name = scrapy.Field()
    default_output_processor=TakeFirst()

class ArticlespiderItem(scrapy.Item):
    title =scrapy.Field()
    create_date=scrapy.Field(
        input_processor=MapCompose(date_covert),
    )
    url=scrapy.Field()
    url_object_id=scrapy.Field()
    front_image_url=scrapy.Field(
        output_processor=MapCompose(return_value)
    )
    front_image_path=scrapy.Field()
    parise_nums=scrapy.Field(
        input_processor=MapCompose(get_nums)
    )
    comment_nums = scrapy.Field(
        input_processor=MapCompose(get_nums)
    )
    fav_nums = scrapy.Field(
        input_processor=MapCompose(get_nums)
    )
    tags=scrapy.Field(
        input_processor=MapCompose(remove_comment_tag),
        output_procesor=Join(",")
    )
    content=scrapy.Field()
    def get_insert_sql(self):
        insert_sql = """
                insert into jobbole_article(title,url,url_object_id,create_date,fav_nums,front_image_url,parise_nums,comment_nums,tags,content)
                 VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
                """

        front_image_url=""
        if self["front_image_url"]:
            front_image_url=self["front_image_url"][0]
        params=(self["title"],self["url"],self["url_object_id"],self["create_date"],self["fav_nums"],front_image_url,self["parise_nums"],self["comment_nums"],self["tags"],self["content"])
        return insert_sql,params
