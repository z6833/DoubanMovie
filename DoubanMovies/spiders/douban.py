# -*- coding: utf-8 -*-
import re
import json
import scrapy

from DoubanMovies.items import DoubanmoviesItem

class DoubanSpider(scrapy.Spider):
    name = 'douban'
    allowed_domains = ['movie.douban.com']
    # start_urls = ['http://movie.douban.com/']

    start = 0

    # 指定参数
    formdata = {
        'sort': 'U',
        'range': '0, 10',
        'tags': '电影',
        'start': '0',
        'countries': '中国大陆'  # 这里只抓取中国大陆地区，其他地区可做相应修改
    }

    base_url = 'https://movie.douban.com/j/new_search_subjects'

    def start_requests(self):

        # 构造初始请求url
        url = self.base_url + '?' + 'sort={}&range={}&tags={}&start={}&countries={}'.format(
            self.formdata['sort'], self.formdata['range'], self.formdata['tags'],
            self.formdata['start'], self.formdata['countries']
        )

        # 发起请求
        yield scrapy.Request(
            url=url,
            callback=self.parse,
            meta={'formdata': self.formdata}
        )


    def parse(self, response):
        """
        豆瓣默认返回json格式的数据
        :param response:
        :return:
        """
        formdata = response.meta['formdata']

        # 将json格式的数据转化为字典
        data_list = json.loads(response.body.decode())['data']

        # 数据解析
        for data in data_list:

            # 从json数据中解析基本信息
            item = DoubanmoviesItem()
            item['filmtitle'] = data['title']
            item['moviemark'] = data['rate']
            item['moviedirt'] = ' '.join(data['directors'])
            item['movierole'] = ' '.join(data['casts'])

            # 拿到详情页链接，获取影评等信息
            detail_url = data['url']
            yield scrapy.Request(
                url=detail_url,
                callback=self.parse_detail,
                meta={'item': item, 'formdata': formdata}
            )

        if not self.start == 1000:  # 抓取1020条数据
            self.start += 20
            formdata = self.formdata
            formdata['start'] = str(self.start)

            url = self.base_url + '?' + 'sort={}&range={}&tags={}&start={}&countries={}'.format(
            formdata['sort'], formdata['range'], formdata['tags'],
            formdata['start'], formdata['countries'])

            yield scrapy.Request(
                url=url,
                callback=self.parse,
                meta={'formdata': formdata}
            )

    def parse_detail(self, response):
        """
        从详情页解析其他信息
        :param response:
        :return:
        """
        formdata = response.meta['formdata']
        item = response.meta['item']

        item['movietype'] = '/'.join(response.xpath("//div[@id='info']/span[@property='v:genre']/text()").extract())
        item['moviearea'] = formdata['countries']
        item['movielang'] = ''.join(re.findall('<span class="pl">语言:</span>(.*?)<br/>', response.body.decode()))
        item['moviedate'] = '/'.join(response.xpath("//div[@id='info']/span[@property='v:initialReleaseDate']/text()").extract())
        item['moviesyno'] = response.xpath("//div[@id='link-report']/span[1]/text()").extract_first().strip()

        # 新页面解析电影短评
        coms_url = response.xpath("//div[@id='comments-section']/div[1]/h2/span/a/@href").extract_first()
        yield scrapy.Request(
            url=coms_url,
            callback=self.parse_coms,
            meta={'item': item}
        )

    def parse_coms(self, response):
        """
        解析电影短评top20，将20条短评以//拼接成一个字符串
        :param response:
        :return:
        """
        item = response.meta['item']

        # 提取短评top20
        coms_list = response.xpath("//div[@id='comments']/div[@class='comment-item']/div[@class='comment']/p/span/text()").extract()
        item['moviecoms'] = '//'.join(coms_list)

        yield item



