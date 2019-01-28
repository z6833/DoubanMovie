# -*- coding: utf-8 -*-
from DoubanMovies.settings import USER_AGENTS as ua
import random

class DoubanmoviesDownloaderMiddleware(object):

    def process_request(self, request, spider):
        """
                给每一个请求随机分配一个代理
                :param request:
                :param spider:
                :return:
                """
        user_agent = random.choice(ua)
        request.headers['User-Agent'] = user_agent
