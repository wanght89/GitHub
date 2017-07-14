# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

import pymysql
from lagou.settings import MYSQL_HOST,MYSQL_USER,MYSQL_PASSWD,MYSQL_DB
class LagouPipeline(object):
    def __init__(self):
        self.conn=pymysql.connect(MYSQL_HOST,MYSQL_USER,MYSQL_PASSWD,MYSQL_DB,charset="utf8",use_unicode=True)
        self.cursor=self.conn.cursor()
    def process_item(self, item, spider):
        insert_sql="""
        INSERT INFO lagou_job(job_id,title,url,salary,job_city,work_years,degree_need,job_type,publish_time,job_advantage,job_desc,job_addr,company_url,company_name)
        VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
        """
        self.cursor.execute(insert_sql,item["job_id"],item["title"],item["url"],item["salary"],item["job_city"],item["work_years"],item["degree_need"],item["job_type"],item["publish_time"],
                            item["job_advantage"],item["job_desc"],item["job_addr"],item["company_url"],item["company_name"])
        self.conn.commit()
        return item
