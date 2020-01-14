# -*- coding: utf-8 -*-
import scrapy
import time
from scrapy.http import Request, FormRequest
import re
from ..items import ShijiazhuangItem
import requests
import random


# 验证日期的有效性
def isValidTime(date):
    try:
        time.strptime(date, "%Y.%m.%d")
        return True
    except Exception:
        return False


# def generateCookie():
#     url = "https://www.duxiu.com/?lsu=shr"
#     session = requests.Session()
#     response = session.get(url,allow_redirects=False)
#     print(session.cookies.get_dict())
#     return session.cookies.get_dict()

def getANewCookie():
    url = "http://www.duxiu.com/loginhl.jsp?send=true&UserName=shr&PassWord=shr"
    res = requests.get(url)
    c = res.request.headers["Cookie"]
    cookies = dict(([l.split("=") for l in c.split("; ") if l != ""]))
    cookies['selfPageSize'] = 50   #每一页50条
    #print(cookies)
    return cookies


# def extract_cookies(cookie):
#     """从浏览器或者request headers中拿到cookie字符串，提取为字典格式的cookies"""
#     cookies = dict(([l.split("=")  for l in cookie.split("; ") if l != ""]))
#     return cookies

# def getRandomCookie():
#     cookieList = []
#     with open("cookies.txt", "r") as f:
#         for l in f.readlines():
#             cookieList.append(l)
#     idx = random.randint(0, len(cookieList) - 1)
#     cookies = extract_cookies(cookieList[idx])
#     print("cookies:",cookies)
#     return cookies

class ShijiazhuangSpiderSpider(scrapy.Spider):
    # 爬虫名
    name = 'shijiazhuang_spider'
    max_retries = 10

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.retries = {}
        self.cookies = getANewCookie()

    # 允许域名
    allowed_domains = ['newspaper.duxiu.com', 'duxiu.com']

    # 浏览器用户代理
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.88 Safari/537.36',
        "Connection": "keep - alive"
    }

    # 入口URL
    # start_urls = ['https://newspaper.duxiu.com/searchNP?sw=%E6%97%A5%E6%8A%A5&allsw=&channel=searchNP&bCon=&ecode=utf-8&searchtype=&Field=7']

    def start_requests(self):

        # 指定cookie
        # cookies = {
        #     'cookiecheck': 'true',
        #     'AID_dsr': '3946',
        #     'superlib': '""',
        #     'msign_dsr': '1575907448146',
        #     '__dxca': '52e86bfb-232f-4c6c-8e20-94921ee4ee1d',
        #     'DSSTASH_LOG': 'C%5f1%2dUN%5f3946%2dUS%5f0%2dT%5f1576914115704',
        #
        #     'search_uuid': '7a73513a%2dd985%2d4115%2daea2%2d953f40a86048',
        #     'UM_distinctid': '16f3f07e42d7e4-0a4886c8dc43f6-6701b35-1fa400-16f3f07e42e403',
        #     'duxiu':'userName%5fdsr%2c%3dshr%2c%21userid%5fdsr%2c%3d10321%2c%21char%5fdsr%2c%3d%2c%21metaType%2c%3d0%2c%21dsr%5ffrom%2c%3d1%2c%21logo%5fdsr%2c%3dunits%5flogo%2flogo%5fexp%2ejpg%2c%21logosmall%5fdsr%2c%3dunits%5flogo%2flogosmall%5fexp%2ejpg%2c%21title%5fdsr%2c%3d%u8bfb%u79c0%u4f53%u9a8c%u7248%2c%21url%5fdsr%2c%3d%2c%21compcode%5fdsr%2c%3d%2c%21province%5fdsr%2c%3d%u5176%u5b83%2c%21readDom%2c%3d0%2c%21isdomain%2c%3d3%2c%21showcol%2c%3d0%2c%21hu%2c%3d0%2c%21areaid%2c%3d0%2c%21uscol%2c%3d0%2c%21isfirst%2c%3d2%2c%21istest%2c%3d1%2c%21cdb%2c%3d0%2c%21og%2c%3d0%2c%21ogvalue%2c%3d0%2c%21testornot%2c%3d0%2c%21remind%2c%3d0%2c%21datecount%2c%3d3659%2c%21userIPType%2c%3d1%2c%21lt%2c%3d1%2c%21ttt%2c%3dduxiu%2c%21enc%5fdsr%2c%3d2EA1730CDC7539E87B603370ECEA1C6A',
        #     'CNZZDATA2088844':'cnzz_eid%3D574293950-1576909844-https%253A%252F%252Fbook.duxiu.com%252F%26ntime%3D1577340355',
        #     'JSESSIONID':'431733BA4027212AB0D870198404ECC4.jour5210',
        #     'route':'7392bbfdcb077b54dcbb895cc671ca15',
        #     'fresh_dsr':'1577343194300'
        # }

        # urls = [
        #     #石家庄日报搜索
        #     #'https://newspaper.duxiu.com/searchNP?sw=%E7%9F%B3%E5%AE%B6%E5%BA%84%E6%97%A5%E6%8A%A5&allsw=%23%2C07%E6%97%A5%E6%8A%A5&channel=searchNP&bCon=&ecode=utf-8&searchtype=&Field=7'
        #     #日报搜索
        #     #'https://newspaper.duxiu.com/searchNP?sw=%E6%97%A5%E6%8A%A5&allsw=&channel=searchNP&bCon=&ecode=utf-8&searchtype=&Field=7'
        #     #石家庄日报日期搜索
        #     'https://newspaper.duxiu.com/searchNP?channel=searchNP&np_id=320700000846&date=2019.11.01',
        #     'https://newspaper.duxiu.com/searchNP?channel=searchNP&np_id=320700000846&date=2019.11.02'
        # ]

        # 按照日期生成新的拼接URL
        base_url = "https://newspaper.duxiu.com/searchNP?channel=searchNP&np_id=320700000846&date="
        urls = []

        for day in range(1, 32):  # 日期范围
            for month in range(1, 13):  # 月份范围
                for year in range(2003, 2020):  # 年份范围
                    date = "%04d.%02d.%02d" % (year, month, day)
                    if isValidTime(date) == True:
                        urls.append(base_url + date)

        for url in urls:
            yield scrapy.Request(url=url,  cookies=self.cookies, meta={'dont_redirect': True, 'handle_httpstatus_list': [302]},
                                 callback=self.parse, dont_filter=True)

    # 默认解析方法
    def parse(self, response):
        # headers = {
        #     'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.88 Safari/537.36',
        #     "Connection": "keep - alive"
        # }

        print("=====response=====", response.status)
        if response.status == 302:
            retries = self.retries.setdefault(response.url, 0)
            print("======response.url=====", response.url)

            if retries < self.max_retries:
                self.retries[response.url] += 1
                self.cookies = getANewCookie()
                yield scrapy.Request(url=response.url, cookies=self.cookies, meta={'dont_redirect': True, 'handle_httpstatus_list': [302]},
                                     callback=self.parse, dont_filter=True)
            else:
                return
        else:

            # item文件导入
            shijiazhuang_item = ShijiazhuangItem()
            # 解析第一条ul下的新闻
            news_list1 = response.xpath("//div[@class='journal']/ul/li")
            shijiazhuang_item['news_title'] = news_list1.xpath("./dl/dt/a/text()").extract_first()
            shijiazhuang_item['news_time'] = news_list1.xpath("./dl/dd[1]/a[1]/font/text()").extract_first()
            shijiazhuang_item['news_source'] = news_list1.xpath("./dl/dd[1]/a[2]/font/text()").extract_first()
            shijiazhuang_item['news_content'] = news_list1.xpath("./dl/dd[2]/text()[2]").extract_first()
            # 将数据yield到pipelines中去，对数据进行清洗或存储
            yield shijiazhuang_item
            # print(shijiazhuang_item)

            # 循环li新闻条目
            news_list = response.xpath("//div[@class='journal']/li")
            for i_item in news_list:
                # 写详细XPATH对数据进行解析
                shijiazhuang_item['news_title'] = i_item.xpath("./dl/dt/a/text()").extract_first()
                shijiazhuang_item['news_time'] = i_item.xpath("./dl/dd[1]/a[1]/font/text()").extract_first()
                shijiazhuang_item['news_source'] = i_item.xpath("./dl/dd[1]/a[2]/font/text()").extract_first()
                shijiazhuang_item['news_content'] = i_item.xpath("./dl/dd[2]/text()[2]").extract_first()
                # 将数据yield到pipelines中去，对数据进行清洗或存储
                yield shijiazhuang_item
                # print(shijiazhuang_item)

            # 解析下一页规则，取到下一页xpath
            #next_link = response.xpath("//a[@class='next']/@href").extract_first(default='not-found')
            next_link = response.xpath("//a[@class='next']/@href").extract()
            if next_link is not None:
                next_link = next_link[0]
                #print("123" + next_link)
                print("翻页了！！！！！！！！！！")
                yield scrapy.Request("https://newspaper.duxiu.com/" + next_link, cookies=self.cookies,
                                     meta={'dont_redirect': True, 'handle_httpstatus_list': [302]},  callback=self.parse,
                                     dont_filter=True)
