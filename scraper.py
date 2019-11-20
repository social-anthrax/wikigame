import scrapy
import json
from scrapy.crawler import CrawlerProcess
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from collections import defaultdict


website= input("Please input the website you wish to scrape: ")
domain = website.replace("https://", "").replace("http://", "").split("/", 1)[0]


class ScraperWithLimit(scrapy.Spider):

    name = "ScraperWithLimit"
    start_urls = [
        #these are all test case websites with known outputs
        # 'https://en.wikipedia.org/wiki/Web_scraping',
        # 'https://en.wikipedia.org/wiki/Pok%C3%A9mon',
        # 'https://www.sqa.org.uk/sqa/70972.html',
        website,
    ]

    allowed_domains = [domain]

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


# class MySpider(CrawlSpider):
#     name = 'example.com'
#     allowed_domains = ['www.sqa.org.uk']
#     start_urls = ['https://www.sqa.org.uk/sqa/70972.html']
#     custom_settings = {
#         'DEPTH_LIMIT': 1,
#         'DEPTH_PRIORITY': -1,
#         'LOG_FILE': "test.txt",
#         'LOG_LEVEL': "INFO"
#     }
#     rules = (
#         # Extract links matching 'category.php' (but not matching 'subsection.php')
#         # and follow links from them (since no callback means follow=True by default).
#         # Rule(LinkExtractor(allow=(), deny=())),

#         # Extract links matching 'item.php' and parse them with the spider's method parse_item
#         Rule(LinkExtractor(allow=()), callback='parse_item'),
#     )

#     def parse_item(self, response):
#         self.logger.info('Hi, this is an item page! %s', response.url)
#         item = scrapy.Item()
#         item['name'] = response.xpath('//td[@id="item_name"]/text()').get()
#         item['description'] = response.xpath(
#             '//td[@id="item_description"]/text()').get()
#         item['link_text'] = response.meta['link_text']
#         return item






# if __name__ == "__main__":
    
dictOfUrl = defaultdict(list)
# website = "www.george-heriots.com"
process = CrawlerProcess()
process.crawl(ScraperWithLimit)
process.start()

process.stop()

file = open('yeet.txt', 'w')
for x, y in dictOfUrl.items():
    file.write(x+", {")
    for item in y:
        item = item[52:-1]
        if item[0] == "/" or "http" in item:
            if "http" not in item:
                file.write(item.replace('//', '') + ", ")
            else:
                file.write(item + ", ")
        file.write("}\n")
file.close()
