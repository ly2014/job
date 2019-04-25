import json


class JobSpiderPipeline(object):
    def __init__(self):
        self.file = open('data.txt', 'w', encoding='utf-8')

    def process_item(self, item, spider):
        it = {}
        it['title'] = item['title']
        it['company'] = item['company']
        self.file.write(json.dumps(it, ensure_ascii=False))
        self.file.write('@')
        return item

    def close_spider(self, spider):
        self.file.close()
