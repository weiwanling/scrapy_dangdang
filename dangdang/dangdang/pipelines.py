# -*- coding: utf-8 -*-
import MySQLdb
import re
# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


def table_exists(con,table_name):
    '''在数据库con中判断表table_name是否存在
       存在返回1
    '''
    sql = "show tables;"
    con.execute(sql)
    tables = [con.fetchall()]
    table_list = re.findall('(\'.*?\')',str(tables))
    table_list = [re.sub("'",'',each) for each in table_list]
    if table_name in table_list:
        return 1
    else:
        return 0


class DangdangPipeline(object):
    def process_item(self, item, spider):
        db = MySQLdb.connect(host="localhost", user="root", passwd="6611", db='dangdang', charset='utf8', port=3307)
        cursor = db.cursor()
        if not table_exists(cursor,'tb1'):
            sql1 = """CREATE TABLE tb1 (
                     id INT NOT NULL AUTO_INCREMENT,
                     link VARCHAR(200) NOT NULL ,
                     title VARCHAR(200) NOT NULL,
                     comment VARCHAR(200) NOT NULL,
                     shop  VARCHAR(20) NOT NULL,
                     price VARCHAR(15) NOT NULL,
                     PRIMARY KEY (id)
                     );"""
            cursor.execute(sql1)
        sql2 = """INSERT INTO dangdang.tb1
                            (title,link,comment,shop,price)
                            VALUES
                            (%s, %s, %s, %s, %s);"""

        for i in range(len(item['title'])):
            try:
                #插入数据
                cursor.execute(sql2,(item['title'][i],item['link'][i],item['comment'][i],item['shop'][i],item['price'][i]))

            except Exception as e:
                print('爬取异常：',e)
                db.rollback()
        cursor.close()
        db.commit()

        return item
