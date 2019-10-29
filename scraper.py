import scrapy
from scrapy.crawler import CrawlerProcess


class ScraperWithLimit(scrapy.Spider):
    name = "ScraperWithLimit"
    start_urls = [
        'https://en.wikipedia.org/wiki/Web_scraping',
    ]

    custom_settings = {
        'DEPTH_LIMIT': 2
    }

    def parse(self, response):
        for next_page in response.css('div.mw-parser-output > p > a'):
            yield response.follow(next_page, self.parse)

        for quote in response.css('div.mw-parser-output > p'):
            yield {'quote': quote.extract()}


process = CrawlerProcess()
process.crawl(ScraperWithLimit)
process.start()
