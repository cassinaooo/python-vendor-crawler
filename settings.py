"""This module defines the scrapy settings"""

from scrapy.settings import Settings


class WebsiteSettings(Settings):

    """
    Defining the settings for the scraper
    """

    @staticmethod
    def generate_settings_dict():
        """
        Generating the settings dictionary

        :param file_location: temporary file location
        :type file_location: str

        :return: setting dictionary
        """

        settings_dict = {
            "FEED_FORMAT": "jsonlines",
            # "FEED_URI": file_location,
            "DOWNLOAD_MAXSIZE": 1000000,
            "COOKIES_ENABLED": False,
            "RETRY_ENABLED": False,
            "DOWNLOAD_TIMEOUT": 15,
            "AUTOTHROTTLE_ENABLED": True,
            "AUTOTHROTTLE_TARGET_CONCURRENCY": 10,
            "LOG_LEVEL": "DEBUG",
            "DEPTH_LIMIT": 1,
            "DEPTH_PRIORITY": 1,
            "SCHEDULER_DISK_QUEUE": "scrapy.squeues.PickleFifoDiskQueue",
            "SCHEDULER_MEMORY_QUEUE": "scrapy.squeues.FifoMemoryQueue",
            "SCHEDULER_PRIORITY_QUEUE": "scrapy.pqueues.DownloaderAwarePriorityQueue",
            "CLOSESPIDER_ITEMCOUNT": 5,
            "REFERER_ENABLED": False,
            "TELNETCONSOLE_ENABLED": False,
            "USER_AGENT": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        }

        return settings_dict
