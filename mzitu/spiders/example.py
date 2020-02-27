# TODO:  分类，存放于文件夹中，并存储 标题，时间，分类，标签等信息
# 以上是可以拓展的功能，但是由于我不想做了，就不管了Q

# -*- coding: utf-8 -*-
import os
import time
import scrapy
import requests
from scrapy.selector import Selector

from urllib.parse import quote


def get_proxy():
    return requests.get("http://127.0.0.1:5010/get/").json()


def delete_proxy(proxy):
    requests.get("http://127.0.0.1:5010/delete/?proxy={}".format(proxy))


def addOne(url: str):
    if url.count('/') == 3:
        url += '/1'
    return url


def urlToFileName(url: str):
    url = addOne(url)
    url = quote(url)
    url = url.replace('/', '%p')
    filename = 'F:/workspace/data/imgs/'+url+'.jpg'
    return filename


def urlToFinishedFileName(url: str):
    url = addOne(url)
    while url[-1] != '/':
        url = url[0:-1]
    url = url+'9999'
    finishedName = urlToFileName(url)
    return finishedName

headers = {
    'User-Agent': 'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1)',
    'Referer': 'https://www.mzitu.com'
}

def DownloadImg(url, urlOfFileName):
    retry_count = 5
    while True:
        # proxy = get_proxy().get("proxy")

        while retry_count > 0:
            try:
                myResponse = requests.get(url, headers=headers)
                # ,proxies= {"http": "http://{}".format(proxy)})
                break
            except Exception:
                print(myResponse.status_code)
                retry_count -= 1
        if retry_count > 0:
            break

    filename = urlToFileName(urlOfFileName)
    with open(filename, 'wb') as fin:
        fin.write(myResponse.content)

class ExampleSpider(scrapy.Spider):
    name = 'example'
    allowed_domains = ['example.com']
    start_urls = ['http://example.com/']

    def parse(self, response):
        yield {"name1": "value1"}
        pass


class MzituSpider(scrapy.Spider):
    name = 'mzitu'
    allowed_domains = ['mzitu.com', 'i5.mmzztt.com']
    start_urls = ['https://www.mzitu.com/']
    # start_urls=['https://www.mzitu.com/page/240/']

    def parse_detail(self, response):

        # 下载图片
        for url in response.css('div.main-image img::attr(src)').extract():
            print('Downloading:     '+response.url)
            print(time.localtime())
            DownloadImg(url, response.url)

        # 下载完了一组图片
        if '下一组»' in response.css('.pagenavi>a:last-child').extract()[0]:
            with open(urlToFinishedFileName(response.url), 'wb') as fin:
                fin.write(b'finished')
            print(response.url+'   finished')
            return

        # 下载下一张图片
        for url in response.css('.pagenavi>a:last-child::attr(href)').extract():
            # print(response.url+'->'+url)
            # print(int(url.split('/')[-2]))
            yield scrapy.Request(url, callback=self.parse_detail, priority=int(url.split('/')[-2]))

    def parse(self, response):
        # 开始下载每一组
        for url in response.css('#pins li a::attr(href)').extract():
            if os.path.exists(urlToFinishedFileName(url)):
                # print(url + '  already crawled.')
                continue
            # print(url)
            yield scrapy.Request(url, callback=self.parse_detail, priority=int(url.split('/')[-1]))
        # 下一页
        for url in response.css('.next.page-numbers::attr(href)').extract():
            # print(url)
            yield scrapy.Request(url, priority=0)
        pass
