# -*- coding: utf-8 -*-
from openpyxl import Workbook

class DoubanmoviesPipeline(object):

    def __init__(self):

        # 创建excel表格保存数据
        self.workbook = Workbook()
        self.booksheet = self.workbook.active
        self.booksheet.append(['电影名称', '评分', '导演',
                               '主演', '电影类型', '制片地区',
                               '语言类型', '上映时间', '剧情简介',
                               '短评(top20)'])

    def process_item(self, item, spider):

        DATA = [
            item['filmtitle'], item['moviemark'], item['moviedirt'],
            item['movierole'], item['movietype'], item['moviearea'],
            item['movielang'], item['moviedate'], item['moviesyno'],
            item['moviecoms']]
        self.booksheet.append(DATA)
        self.workbook.save('./results.xls')

        return item
