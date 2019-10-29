import scrapy
import json
from scrapy.crawler import CrawlerProcess

import scrapy
from scrapy.crawler import CrawlerProcess


class ScraperWithLimit(scrapy.Spider):
    name = "ScraperWithLimit"
    start_urls = [
        'https://en.wikipedia.org/wiki/Web_scraping',
    ]

    custom_settings = {
        'DEPTH_LIMIT': 1
    }

    def parse(self, response):
        file = open('yeet.txt', 'a')
        for next_page in response.css('div.mw-parser-output > p >       a'):
            yield response.follow(next_page, self.parse)

        file.write(response.url + "\n")
        # for quote in response.css('div.mw-parser-output > p'):
            # yield {'quote': quote.extract()}

class ScraperWithDuplicateRequests(scrapy.Spider):
    

    name = "ScraperWithDuplicateRequests"
    start_urls = [
        'https://en.wikipedia.org/wiki/Web_scraping',
    ]
    custom_settings = {
        'DEPTH_LIMIT': 2
    }

    def parse(self, response):
        
        for next_page in response.css('div.mw-parser-output > p > a::attr(href)').extract_first():
            if next_page is not None:
                next_page = response.urljoin(next_page)
               
                yield scrapy.Request(next_page, callback=self.parse, dont_filter=True)
        
        for quote in response.css('div.mw-parser-output > p'):
            quote = quote.extract()
            
            yield {'quote': quote}
        
        
process = CrawlerProcess()
process.crawl(ScraperWithLimit)
process.start()
process.stop()

