from flask import Flask, request
import json
import pypinyin
import subprocess
import time
import os

app = Flask(__name__)
baseDir = os.path.dirname(os.path.realpath(__file__))


@app.route('/')
def hello_world():
    return 'Hello World!'


@app.route('/get_58_company', methods=['GET', 'POST'])
def get_58_company():
    data = request.get_data()
    data = json.loads(data)
    if 'ip' in data.keys():
        ip = data['ip']
        with open('job_58/job_spider/ip.txt', 'w', encoding='utf-8') as f:
            f.write(ip)
    city = data['city']
    job = data['job']
    pys = pypinyin.pinyin(city)
    s = ''
    for i in pys:
        s += i[0][0]
    with open('job_58/job_spider/param.txt', 'w', encoding='utf-8') as f:
        f.write(s + '#' + job)
    p = subprocess.Popen("cd job_58/job_spider && scrapy crawl spider_58", shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    while True:
        if subprocess.Popen.poll(p) is None:
            print(p.stdout.readline().strip())
        else:
            p.terminate()
            p.kill()
            break
        time.sleep(0.001)
    items = []
    with open('./job_58/job_spider/data.txt', 'r', encoding='utf-8') as f:
        dt = f.read()
        dt = dt.split('@')
        for i in dt[:-1]:
            items.append(json.loads(i))
    os.remove('./job_58/job_spider/data.txt')
    return json.dumps(items, ensure_ascii=False)


@app.route('/get_51_company', methods=['GET', 'POST'])
def get_51_company():
    data = request.get_data()
    data = json.loads(data)
    if 'ip' in data.keys():
        ip = data['ip']
        with open('job_51/job_spider/ip.txt', 'w', encoding='utf-8') as f:
            f.write(ip)
    city = data['city']
    job = data['job']
    with open('job_51/job_spider/param.txt', 'w', encoding='utf-8') as f:
        f.write(city + '#' + job)
    p = subprocess.Popen("cd job_51/job_spider && scrapy crawl spider_51", shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    while True:
        if subprocess.Popen.poll(p) is None:
            print(p.stdout.readline().strip())
        else:
            p.terminate()
            p.kill()
            break
        time.sleep(0.001)
    items = []
    with open('job_51/job_spider/data.txt', 'r', encoding='utf-8') as f:
        dt = f.read()
        dt = dt.split('@')
        for i in dt[:-1]:
            items.append(json.loads(i))
    os.remove('job_51/job_spider/data.txt')
    return json.dumps(items, ensure_ascii=False)


@app.route('/get_company', methods=['GET', 'POST'])
def get_company():
    data = request.get_data()
    data = json.loads(data)
    company = data['company']
    print(type(data))
    if 'ip' in data.keys():
        ip = data['ip']
        with open('qc_spider/qc_spider/ip.txt', 'w', encoding='utf-8') as f:
            f.write(ip)
    with open('qc_spider/qc_spider/param.txt', 'w', encoding='utf-8') as f:
        f.write(company)
    p = subprocess.Popen("cd qc_spider/qc_spider && scrapy crawl spider_qc", shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    while True:
        if subprocess.Popen.poll(p) is None:
            print(p.stdout.readline().strip())
        else:
            p.terminate()
            p.kill()
            break
        time.sleep(0.1)
    content = ''
    with open('qc_spider/qc_spider/company.txt', 'r', encoding='utf-8') as f:
        content = f.read()
    os.remove('qc_spider/qc_spider/company.txt')
    return content


if __name__ == '__main__':
    app.run()
