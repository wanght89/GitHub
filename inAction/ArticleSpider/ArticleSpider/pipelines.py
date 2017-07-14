# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

import pymysql
from MySQLdb import cursors
class ArticlespiderPipeline(object):
    def __init__(self):
        self.conn=pymysql.connect('127.0.0.1','root','root','article_spider',charset="utf8",use_unicode=True)
        self.cursor=self.conn.cursor()

    def process_item(self, item, spider):
        insert_sql ="""
        insert into jobbole_article(title,url,create_date,fav_nums,content) VALUES(%s,%s,%s,%s,%s)
        """
        self.cursor.execute(insert_sql,(item["title"],item["url"],item["create_date"],item["fav_nums"],item["content"]))
        self.conn.commit()
        return item

from twisted.enterprise import adbapi
class MySqlTwistedPipline(object):
    def __init__(self,dbpool):
        self.dbpool=dbpool
    @classmethod
    def from_settings(cls,settings):
        '''传入settings的参数'''
        dbparms=dict(
            host=settings["MYSQL_HOST"],
            db=settings["MYSQL_DBNAME"],
            user=settings["MYSQL_USER"],
            passwd=settings["MYSQL_PASSWORD"],
            charset='utf8',
            cursorclass=cursors.DictCursor,
            use_unicode=True
        )
        dbpool=adbapi.ConnectionPool("MySQLdb",**dbparms)
        return cls(dbpool)
    def process_item(self,item,spider):
        #使用twisted将mysql插入变成异步进行
        query=self.dbpool.runInteraction(self.do_insert,item)
        query.addErrback(self.handle_error,item,spider)   #处理异常

    def handle_error(self,failure,item,spider):
        #处理异步插入的异常
        print(failure)
    def do_insert(self,cursor,item):
        #执行具体的插入
        #根据不同的item构建不同的sql语句并插入到mysql中
        insert_sql,params=item.get_insert_sql()
        print(insert_sql,params)
        cursor.execute(insert_sql,params)
