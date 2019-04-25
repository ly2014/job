# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import json


class Job51Pipeline(object):
    def __init__(self):
        self.file = open('data.txt', 'w', encoding='utf-8')

    def process_item(self, item, spider):
        it = {}
        it['title'] = item['title']
        it['company'] = item['company']
        self.file.write(json.dumps(it, ensure_ascii=False) + '@')
        return item

    def close_spider(self, spider):
        self.file.close()
