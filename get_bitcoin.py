#!/usr/bin/env python
# -*- encoding: utf-8 -*-
# Created on 2019-03-25 12:28:31
# Project: get_bitcoin

from pyspider.libs.base_handler import *


class Handler(BaseHandler):
    crawl_config = {
    }
 

    @every(minutes=24 * 60)
    def on_start(self):
        base_url='https://coinmarketcap.com/zh/currencies/bitcoin/historical-data/?start=#START#&end=#END#'
        year_list=['2015','2016','2017','2018']
        month_list=range(1,13)
        for year in year_list:
            for month in month_list:
                start_date=year+str(month).rjust(2,'0')+'01'
                end_date=year+str(month).rjust(2,'0')+'31'
                self.crawl(base_url.replace('#START#',start_date).replace('#END#',end_date), callback=self.detail_page)

    @config(age=10 * 24 * 60 * 60)
    def index_page(self, response):
        for each in response.doc('a[href^="http"]').items():
            self.crawl(each.attr.href, callback=self.detail_page)

    @config(priority=2)
    def detail_page(self, response):
        return {
            "url": response.url,
            "title": response.doc('title').text(),
            "text_right":response.doc('tr.text-right').text()
        }

