import scrapy
import os
import sys
sys.path.append('..')
from job_spider.items import Job51Item


class Spider51(scrapy.spiders.Spider):
    name = 'spider_51'
    start_urls = ['https://www.baidu.com/']

    headers = {
        'User - Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko)'
                        ' Chrome/73.0.3683.86 Safari/537.36'
    }

    code = ''
    job = ''
    ip = ''

    def __init__(self):
        self.codes = {}
        with open('city.txt', 'r', encoding='utf-8') as f:
            lines = f.readlines()
            for line in lines:
                line = line.split(':')
                self.codes[line[0]] = line[1]

    def start_requests(self):
        yield scrapy.Request(url=self.start_urls[0], headers=self.headers, callback=self.parse)

    def parse(self, response):
        with open('param.txt', 'r', encoding='utf-8') as f:
            content = f.read().strip()
            content = content.split('#')
            city = content[0]
            self.job = content[1]
        os.remove('param.txt')
        if city in self.codes.keys():
            self.code = self.codes[city]
        else:
            self.code = '000000'
        url = 'https://search.51job.com/list/%s,000000,0000,00,9,99,%s,2,1.html?lang=c&stype=&postchannel=0000' \
              '&workyear=99&cotype=99&degreefrom=99&jobterm=99&companysize=99&providesalary=99&lonlat=0,0&radius=-1' \
              '&ord_field=0&confirmdate=9&fromType=&dibiaoid=0&address=&line=&specialarea=00&from=&welfare='\
              % (self.code, self.job)
        if os.path.exists('ip.txt'):
            with open('ip.txt', 'r', encoding='utf-8') as f:
                self.ip = f.read().strip()
            os.remove('ip.txt')
        if self.ip != '':
            yield scrapy.Request(url=url, callback=self.parse1, headers=self.headers, meta={'proxy': self.ip})
        else:
            yield scrapy.Request(url=url, callback=self.parse1, headers=self.headers)

    def parse1(self, response):
        pages = response.xpath('//div[@class="p_in"]/span[1]/text()').extract_first()
        pages = pages[pages.find('共') + 1:pages.find('页')]
        pages = int(pages)
        print(pages)
        jobs = response.xpath('//div[@id="resultList"]/div[@class="el"]')
        for job in jobs:
            item = Job51Item()
            title = job.xpath('p/span/a/@title').extract_first()
            title = title.strip()
            print(title)
            item['title'] = title
            company = job.xpath('span[1]/a/@title').extract_first()
            company = company.strip()
            print(company)
            item['company'] = company
            yield item
        if pages > 10:
            pages = 10
        p = 2
        while p <= pages:
            url = 'https://search.51job.com/list/%s,000000,0000,00,9,99,%s,2,%s.html?lang=c&stype=&postchannel=0000' \
              '&workyear=99&cotype=99&degreefrom=99&jobterm=99&companysize=99&providesalary=99&lonlat=0,0&radius=-1' \
              '&ord_field=0&confirmdate=9&fromType=&dibiaoid=0&address=&line=&specialarea=00&from=&welfare='\
                  % (self.code, self.job, p)
            p += 1
            if self.ip != '':
                yield scrapy.Request(url=url, callback=self.parse2, headers=self.headers, meta={'proxy': self.ip})
            else:
                yield scrapy.Request(url=url, callback=self.parse2, headers=self.headers)

    def parse2(self, response):
        jobs = response.xpath('//div[@id="resultList"]/div[@class="el"]')
        for job in jobs:
            item = Job51Item()
            title = job.xpath('p/span/a/@title').extract_first()
            title = title.strip()
            print(title)
            item['title'] = title
            company = job.xpath('span[1]/a/@title').extract_first()
            company = company.strip()
            print(company)
            item['company'] = company
            yield item
