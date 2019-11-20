
# from scrapy.spiders import CrawlSpider, Rule
# from scrapy.linkextractors import LinkExtractor
from collections import defaultdict
import scrapy
from scrapy.crawler import CrawlerProcess


website = "https://www.sqa.org.uk/sqa/70972.html"
domain = "www.sqa.org.uk"
dictOfUrl = defaultdict(list)


# def runScrape(page = ""): #like runescape but not

# if page == "":
#     website = input("Please input the website you wish to scrape: ")
# else:
#     website = page



class ScraperWithLimit(scrapy.Spider):
    name = "ScraperWithLimit"
    start_urls = [
        #these are all test case websites with known outputs
        # 'https://en.wikipedia.org/wiki/Web_scraping',
        # 'https://en.wikipedia.org/wiki/Pok%C3%A9mon',
        # 'https://www.sqa.org.uk/sqa/70972.html',
        # website,
    ]

    allowed_domains = [domain]

    custom_settings = {
        'DEPTH_LIMIT': 1,
        'DEPTH_PRIORITY': 0,
    }

    def parse(self, response):
        for next_page in response.css('a::attr(href)'):
            # 56 is the first character at which the actual url starts and the -3 cuts off the last 3 characters of the string: eg <Selector xpath='descendant-or-self::a/@href' data='http://www.mysqa.org.uk/'> becomes http://www.mysqa.org.uk/
            dictOfUrl[response.url].append(str(next_page.root))
            # file.write(str(next_page)[55:-1] + '\n')
            yield response.follow(next_page, self.parse)

        # file.write(response.url + "\n")



ScraperWithLimit.allowed_domains = [website.replace("https://", "").replace("http://", "").split("/", 1)[0]] #trims away anything making it a url, making it into a domain
ScraperWithLimit.start_urls = [website]
process = CrawlerProcess()
process.crawl(ScraperWithLimit)
process.start()
process.stop()

file = open('yeet.txt', 'w')
for x, y in dictOfUrl.items():
    file.write(x+", {")
    for item in y:
        # item = item[52:-1]
        if item != "" and item != "/":
            if item[0] == "/" or "http" in item:
                if "http" not in item:
                    file.write(item.replace('//', '') + ", ")
                else:
                    file.write(item + ", ")
    file.write("}\n")
file.close()
