# -*- coding: utf-8 -*-
import scrapy
from scrapy.http import Request,FormRequest
import re
from shijiazhuang.items import ShijiazhuangItem

class ShijiazhuangSpiderSpider(scrapy.Spider):
    #爬虫名
    name = 'shijiazhuang_spider'
    #允许域名
    allowed_domains = ['newspaper.duxiu.com']
    #入口URL
    #start_urls = ['https://newspaper.duxiu.com/searchNP?sw=%E6%97%A5%E6%8A%A5&allsw=&channel=searchNP&bCon=&ecode=utf-8&searchtype=&Field=7']

    def start_requests(self):
        # 浏览器用户代理
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36'
        }
        #指定cookie
        cookies = {
            'UM_distinctid':'16ef08d7d502b-094a4fc1b727c4-7711a3e-1fa400-16ef08d7d5183c',
            'cookiecheck':'true',
            'duxiu':'userName%5fdsr%2c%3dshr%2c%21userid%5fdsr%2c%3d10321%2c%21char%5fdsr%2c%3d%2c%21metaType%2c%3d0%2c%21dsr%5ffrom%2c%3d1%2c%21logo%5fdsr%2c%3dunits%5flogo%2flogo%5fexp%2ejpg%2c%21logosmall%5fdsr%2c%3dunits%5flogo%2flogosmall%5fexp%2ejpg%2c%21title%5fdsr%2c%3d%u8bfb%u79c0%u4f53%u9a8c%u7248%2c%21url%5fdsr%2c%3d%2c%21compcode%5fdsr%2c%3d%2c%21province%5fdsr%2c%3d%u5176%u5b83%2c%21readDom%2c%3d0%2c%21isdomain%2c%3d3%2c%21showcol%2c%3d0%2c%21hu%2c%3d0%2c%21areaid%2c%3d0%2c%21uscol%2c%3d0%2c%21isfirst%2c%3d2%2c%21istest%2c%3d1%2c%21cdb%2c%3d0%2c%21og%2c%3d0%2c%21ogvalue%2c%3d0%2c%21testornot%2c%3d0%2c%21remind%2c%3d0%2c%21datecount%2c%3d3664%2c%21userIPType%2c%3d1%2c%21lt%2c%3d1%2c%21ttt%2c%3dduxiu%2c%21enc%5fdsr%2c%3dCE2FC809DD6A63BA6C276BA2C632AE75',
            'AID_dsr':'3946',
            'superlib':'""',
            'msign_dsr':'1576914115704',
            'search_uuid':'b433e633%2dcf92%2d475b%2dbbd6%2d92d487c2b481',
            'DSSTASH_LOG':'C%5f1%2dUN%5f3946%2dUS%5f0%2dT%5f1576914115714',
            '__dxca':'52e86bfb-232f-4c6c-8e20-94921ee4ee1d',
            'CNZZDATA2088844':'cnzz_eid%3D574293950-1576909844-https%253A%252F%252Fbook.duxiu.com%252F%26ntime%3D1576920584',
            'JSESSIONID':'32A9C4C9DDEFB8BA98441E3DB21940EC.jour5210',
            'route':'7392bbfdcb077b54dcbb895cc671ca15',
            'fresh_dsr':'1576922428894'

        }
        urls = [
            'https://newspaper.duxiu.com/searchNP?sw=%E7%9F%B3%E5%AE%B6%E5%BA%84%E6%97%A5%E6%8A%A5&allsw=%23%2C07%E6%97%A5%E6%8A%A5&channel=searchNP&bCon=&ecode=utf-8&searchtype=&Field=7'
            #'https://newspaper.duxiu.com/searchNP?sw=%E6%97%A5%E6%8A%A5&allsw=&channel=searchNP&bCon=&ecode=utf-8&searchtype=&Field=7'
        ]
        for url in urls:
            yield scrapy.Request(url=url, headers=headers, cookies=cookies, callback=self.parse)

    # 默认解析方法
    def parse(self, response):
        # item文件导入
        shijiazhuang_item = ShijiazhuangItem()
        # 解析第一条ul下的新闻
        news_list1 = response.xpath("//div[@class='journal']/ul/li")
        shijiazhuang_item['news_title'] = news_list1.xpath("./dl/dt/a/text()").extract_first()
        shijiazhuang_item['news_time'] = news_list1.xpath("./dl/dd[1]/a[1]/text()").extract_first()
        #shijiazhuang_item['news_source'] = news_list1.xpath("./dl/dd[1]/a[2]/text()").extract_first() + news_list1.xpath("./dl/dd[1]/a[2]/font/text()").extract_first()
        shijiazhuang_item['news_content'] = news_list1.xpath("./dl/dd[2]/text()[2]").extract_first()
        # 将数据yield到pipelines中去，对数据进行清洗或存储
        yield shijiazhuang_item
        print(shijiazhuang_item)

        # 循环li新闻条目
        news_list = response.xpath("//div[@class='journal']/li")
        for i_item in news_list:
            #写详细XPATH对数据进行解析
            shijiazhuang_item['news_title'] = i_item.xpath("./dl/dt/a/text()").extract_first()
            shijiazhuang_item['news_time'] = i_item.xpath("./dl/dd[1]/a[1]/text()").extract_first()
            #shijiazhuang_item['news_source'] = i_item.xpath("./dl/dd[1]/a[2]/text()").extract_first()+i_item.xpath("./dl/dd[1]/a[2]/font/text()").extract_first()
            shijiazhuang_item['news_content'] = i_item.xpath("./dl/dd[2]/text()[2]").extract_first()
            #将数据yield到pipelines中去，对数据进行清洗或存储
            yield shijiazhuang_item
            print(shijiazhuang_item)

        # 解析下一页规则，取到下一页xpath
        next_link = response.xpath("//a[@class='next']/@href").extract()
        page_count = 0
        if next_link and page_count < 3:
            page_count += 1
            print(page_count)
            next_link = next_link[0]
            yield scrapy.Request("https://newspaper.duxiu.com/" + next_link, callback=self.parse)



