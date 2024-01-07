"""This module defines all the objects necessary to control the app"""

import os
import json
from scrapy import signals
from scrapy.crawler import CrawlerRunner
from twisted.internet import reactor

from spider import GenericSpider
from settings import WebsiteSettings


class MyCrawlerRunner(CrawlerRunner):
    """
    Crawler object that collects items and returns output after finishing crawl.
    """

    def crawl(self, crawler_or_spidercls, reactor, *args, **kwargs):
        """
        Launch a crawl and return output as deferred

        :param crawler_or_spidercls: scrapy crawler
        :type crawler_or_spidercls: cls

        :return: deferred object with crawled output
        """

        # keep all items scraped
        self.items = []

        # create crawler (Same as in base CrawlerProcess)
        crawler = self.create_crawler(crawler_or_spidercls)

        # handle each item scraped
        crawler.signals.connect(self.item_scraped, signals.item_scraped)

        # create Twisted.Deferred launching crawl
        dfd = self._crawl(crawler, *args, **kwargs)

        # add callback - when crawl is done or error cal return_items

        dfd.addCallback(self.return_items)
        dfd.addErrback(self.return_items)

        dfd.addTimeout(360, reactor)

        return dfd

    def item_scraped(self, item, response, spider):
        """
        Append each individual item scraped

        :param item: scrapy item
        :type item: cls

        :return: None
        """

        self.items.append(item)

    def return_items(self, result, **kwargs):
        """
        Return scrapy items

        :return scrapy items
        """

        print(f"spider stopped. collected {len(self.items)} itens")
        print(result)

        return self.items


def return_spider_output(output):
    """
    Turns scrapy output into dictionaries
    :param output: items scraped by CrawlerRunner
    :type output: dict

    :return: json with list of items
    """

    # this just turns items into dictionaries
    return [dict(item) for item in output]
