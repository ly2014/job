import scrapy
import sys
sys.path.append('..')
from job_spider.items import JobSpiderItem
import os


class Spider58(scrapy.spiders.Spider):
    name = 'spider_58'
    start_urls = ['https://cs.58.com/job/']

    headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.121 Safari/537.36'
    }

    ip = ''
    city = ''
    job = ''

    def parse(self, response):
        with open('param.txt', 'r', encoding='utf-8') as f:
            content = f.read().strip()
            content = content.split('#')
            self.city = content[0]
            self.job = content[1]
        os.remove('param.txt')
        url = 'https://%s.58.com/job/?key=%s' % (self.city, self.job)
        if os.path.exists('ip.txt'):
            with open('ip.txt', 'r', encoding='utf-8') as f:
                self.ip = f.read().strip()
            os.remove('ip.txt')
        if self.ip != '':
            yield scrapy.Request(url=url, headers=self.headers, callback=self.parse1, meta={'proxy': self.ip})
        else:
            yield scrapy.Request(url=url, headers=self.headers, callback=self.parse1)

    def parse1(self, response):
        pages = response.xpath('//i[@class="total_page"]/text()').extract_first()
        if pages:
            pages = int(pages)
        lis = response.xpath('//ul[@id="list_con"]/li')
        item = JobSpiderItem()
        for li in lis:
            title = li.xpath('div[1]/div[1]/a').xpath('string(.)').extract_first().strip()
            print(title)
            item['title'] = title
            company = li.xpath('div[2]/div/a/text()').extract_first().strip()
            print(company)
            item['company'] = company
            yield item
        if pages > 1:
            count = 2
            while count <= pages:
                url = 'https://%s.58.com/job/pn%s/?key=%s&final=1&jump=1' % (self.city, count, self.job)
                if self.ip != '':
                    yield scrapy.Request(url=url, headers=self.headers, callback=self.parse2, meta={'proxy': self.ip})
                else:
                    yield scrapy.Request(url=url, headers=self.headers, callback=self.parse2)
                count += 1

    def parse2(self, response):
        lis = response.xpath('//ul[@id="list_con"]/li')
        for li in lis:
            item = JobSpiderItem()
            title = li.xpath('div[1]/div[1]/a').xpath('string(.)').extract_first().strip()
            print(title)
            item['title'] = title
            company = li.xpath('div[2]/div/a/text()').extract_first().strip()
            print(company)
            item['company'] = company
            yield item
