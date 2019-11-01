import scrapy
import json
from scrapy.crawler import CrawlerProcess
from collections import defaultdict

import scrapy
from scrapy.crawler import CrawlerProcess


class ScraperWithLimit(scrapy.Spider):
    
    name = "ScraperWithLimit"
    start_urls = [
        # 'https://en.wikipedia.org/wiki/Web_scraping',
        # 'https://en.wikipedia.org/wiki/Pok%C3%A9mon',
        # 'https://www.george-heriots.com/',
        'https://www.sqa.org.uk/sqa/70972.html',
    ]

    allowed_domains = ['www.sqa.org.uk']

    custom_settings = {
        'DEPTH_LIMIT': 1,
        'DEPTH_PRIORITY': -1,
    }

    def parse(self, response):
        for next_page in response.css('a::attr(href)'):
            # 56 is the first character at which the actual url starts and the -3 cuts off the last 3 characters of the string: eg <Selector xpath='descendant-or-self::a/@href' data='http://www.mysqa.org.uk/'> becomes http://www.mysqa.org.uk/
            dictOfUrl[response.url].append(str(next_page))
            # file.write(str(next_page)[55:-1] + '\n')
            yield response.follow(next_page, self.parse)

        # file.write(response.url + "\n")
        

class ScraperWithDuplicateRequests(scrapy.Spider):
    

    name = "ScraperWithDuplicateRequests"
    start_urls = [
        'https://en.wikipedia.org/wiki/Web_scraping',
    ]
    
    custom_settings = {
        'DEPTH_PRIORITY': 1,
        'DEPTH_LIMIT': 2
    }

    def parse(self, response):
        
        for next_page in response.css('p > a::attr(href)').extract_first():
            if next_page is not None:
                next_page = response.urljoin(next_page)
               
                yield scrapy.Request(next_page, callback=self.parse, dont_filter=True)
        
        for quote in response.css('div.mw-parser-output > p'):
            quote = quote.extract()
            
            yield {'quote': quote}
        
        
dictOfUrl = defaultdict(list)
process = CrawlerProcess()
process.crawl(ScraperWithLimit)
process.start()

process.stop()

file = open('yeet.txt', 'a')
for x,y in dictOfUrl.items():
    file.write(x+", {" )
    for item in y:
        file.write(item[50:-1].replace('//', '') + ", ")
    file.write("}\n")
file.close()

