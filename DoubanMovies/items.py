# -*- coding: utf-8 -*-

import scrapy

class DoubanmoviesItem(scrapy.Item):

    # 电影名称
    filmtitle = scrapy.Field()
    # 电影评分
    moviemark = scrapy.Field()
    # 导演名称
    moviedirt = scrapy.Field()
    # 电影主演
    movierole = scrapy.Field()
    # 电影类型
    movietype = scrapy.Field()
    # 制片地区
    moviearea = scrapy.Field()
    # 语言类型
    movielang = scrapy.Field()
    # 上映时间
    moviedate = scrapy.Field()
    # 剧情简介
    moviesyno = scrapy.Field()
    # 电影短评
    moviecoms = scrapy.Field()
    # # 电影影评
    # movierews = scrapy.Field()
