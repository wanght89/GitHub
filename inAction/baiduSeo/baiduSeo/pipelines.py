# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import pymysql

class BaiduseoPipeline(object):
    def __init__(self):
        self.conn = pymysql.connect(host="127.0.0.1", user="root", passwd="root", db="zhidaodb")
    def process_item(self, item, spider):
        name=item["name"]
        url=item["url"]
        html=item["html"]
        sql="insert into infoLib (name,url,html) VALUES ('"+name+"','"+url+"','"+html+"')"
        self.conn.query(sql)
        self.conn.commit()
        return item
    def close_spider(self,spider):
        self.conn.close()
