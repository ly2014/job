import scrapy
import json
import os


class QCSpider(scrapy.spiders.Spider):
    name = 'spider_qc'
    start_urls = ['https://www.qichacha.com']

    headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.121 Safari/537.36'
    }

    cookies = {'QCCSESSID': '4765d0u7jt08dueah5i8u62bd3', ' UM_distinctid': '169c42cd71381e-00013830db0b4a-9333061-1fa400-169c42cd71446d', ' zg_did': '%7B%22did%22%3A%20%22169c42cd71b12d-03c2b8b14ddefa-9333061-1fa400-169c42cd71ccb4%22%7D', ' hasShow': '1', ' Hm_lvt_3456bee468c83cc63fb5147f119f1075': '1553774467', ' _uab_collina': '155377446737172155248168', ' acw_tc': '672bd2d115537744701656461e8e012fee6d7ff11235df6b0a7c182bfc', ' zg_de1d1a35bfa24ce29bbf2c7eb17e6c4f': '%7B%22sid%22%3A%201553780426430%2C%22updated%22%3A%201553780427337%2C%22info%22%3A%201553774466878%2C%22superProperty%22%3A%20%22%7B%7D%22%2C%22platform%22%3A%20%22%7B%7D%22%2C%22utm%22%3A%20%22%7B%7D%22%2C%22referrerDomain%22%3A%20%22%22%7D', ' CNZZDATA1254842228': '1597558151-1553773203-https%253A%252F%252Fwww.baidu.com%252F%7C1553778603', ' Hm_lpvt_3456bee468c83cc63fb5147f119f1075': '1553780428'}

    ip = ''

    def parse(self, response):
        with open('param.txt', 'r', encoding='utf-8') as f:
            company = f.read().strip()
        os.remove('param.txt')
        url = 'https://www.qichacha.com/search?key=%s' % company
        if os.path.exists('ip.txt'):
            with open('ip.txt', 'r', encoding='utf-8') as f:
                self.ip = f.read().strip()
            os.remove('ip.txt')
        if self.ip != '':
            yield scrapy.Request(url=url, headers=self.headers, callback=self.parse1, meta={'proxy': self.ip})
        else:
            yield scrapy.Request(url=url, headers=self.headers, callback=self.parse1)

    def parse1(self, response):
        url = response.xpath('//section[@id="searchlist"]//a[@class="ma_h1"]/@href').extract_first()
        url = 'https://www.qichacha.com' + url
        print(url)
        if self.ip != '':
            yield scrapy.Request(url=url, headers=self.headers, callback=self.parse2, cookies=self.cookies,
                                 meta={'proxy': self.ip})
        else:
            yield scrapy.Request(url=url, headers=self.headers, callback=self.parse2, cookies=self.cookies)

    def parse2(self, response):
        item = {}
        l_person = response.xpath('//section[@id="Cominfo"]/table[1]/tr[2]/td[1]/div/div[1]/div[2]/a/h2/text()').extract_first().strip()
        print(l_person)
        item['l_person'] = l_person
        r_code = response.xpath('//section[@id="Cominfo"]/table[2]/tr[4]/td[2]/text()').extract_first().strip()
        print(r_code)
        item['r_code'] = r_code
        code = response.xpath('//section[@id="Cominfo"]/table[2]/tr[3]/td[2]/text()').extract_first().strip()
        print(code)
        item['code'] = code
        capital = response.xpath('//section[@id="Cominfo"]/table[2]/tr[1]/td[2]/text()').extract_first().strip()
        print(capital)
        item['capital'] = capital
        b_time = response.xpath('//section[@id="Cominfo"]/table[2]/tr[2]/td[4]/text()').extract_first().strip()
        print(b_time)
        item['b_time'] = b_time
        c_type = response.xpath('//section[@id="Cominfo"]/table[2]/tr[5]/td[2]/text()').extract_first().strip()
        print(c_type)
        item['c_type'] = c_type
        scope = response.xpath('//section[@id="Cominfo"]/table[2]/tr[11]/td[2]/text()').extract_first().strip()
        print(scope)
        item['scope'] = scope
        address = response.xpath('//section[@id="Cominfo"]/table[2]/tr[10]/td[2]/text()').extract_first().strip()
        print(address)
        item['address'] = address
        term = response.xpath('//section[@id="Cominfo"]/table[2]/tr[9]/td[4]/text()').extract_first().strip()
        print(term)
        item['term'] = term
        status = response.xpath('//section[@id="Cominfo"]/table[2]/tr[2]/td[2]/text()').extract_first().strip()
        print(status)
        item['status'] = status
        shareholder = ''
        shareholders = response.xpath('//section[@id="partnerslist"]/table/tr')[1:]
        for holder in shareholders:
            name = holder.xpath('td[2]/table/tr/td[2]/a/h3/text()').extract_first().strip()
            print(name)
            proportion = holder.xpath('td[3]/text()').extract_first().strip()
            print(proportion)
            amount = holder.xpath('td[4]/text()').extract_first().strip()
            print(amount)
            shareholder = shareholder + name + ',' + proportion + ',' + amount + '#'
        shareholder = shareholder[:-1]
        item['shareholder'] = shareholder
        print(shareholder)
        member = ''
        members = response.xpath('//section[@id="Mainmember"]/table/tr')[1:]
        for m in members:
            name = m.xpath('td[2]/div/a[1]/h3/text()').extract_first().strip()
            print(name)
            position = m.xpath('td[3]/text()').extract_first().strip()
            print(position)
            member = member + name + ',' + position + '#'
        member = member[:-1]
        item['member'] = member
        print(member)
        record = ''
        records = response.xpath('//section[@id="Changelist"]/table/tr')[1:]
        for r in records:
            r1 = r.xpath('td[2]/text()').extract_first().strip()
            print(r1)
            r2 = r.xpath('td[3]').xpath('string(.)').extract_first().strip()
            print(r2)
            r3 = r.xpath('td[4]').xpath('string(.)').extract_first().strip()
            print(r3)
            r4 = r.xpath('td[5]').xpath('string(.)').extract_first().strip()
            print(r4)
            record = record + r1 + '|' + r2 + '|' + r3 + '|' + r4 + '#'
        record = record[:-1]
        item['record'] = record
        print(record)
        with open('company.txt', 'w', encoding='utf-8') as f:
            f.write(json.dumps(item, ensure_ascii=False))
