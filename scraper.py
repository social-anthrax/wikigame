
# from scrapy.spiders import CrawlSpider, Rule
# from scrapy.linkextractors import LinkExtractor
import mysql.connector
from collections import defaultdict
import time
import scrapy
from scrapy.crawler import CrawlerProcess




website = ""
domain = ""
dictOfUrl = defaultdict(list)
if __name__ == "__main__": #checks if its being run as a module or as a standalone
    print("Script must be run as module")
    exit()

class ScraperWithLimit(scrapy.Spider):
    name = "ScraperWithLimit"
    start_urls = [
        #these are all test case websites with known outputs
        # 'https://en.wikipedia.org/wiki/Web_scraping',
        # 'https://en.wikipedia.org/wiki/Pok%C3%A9mon',
        # 'https://www.sqa.org.uk/sqa/70972.html',
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


def runScrape(page="", jumps = 0):  # like runescape but not

    
    if jumps == 0: #checks if the max number of jumps has been modified.
        jumps = input("Please input the max number of jumps to be performed by the scraper \n")
    else:
        jumps = 5

    if page == "": #checks if the page has been passed as a parameter and if it hasnt then 
        website = input("Please input the website you wish to scrape: ")
    else:
        website = page

    domain = website.replace("https://", "").replace("http://", "").split("/", 1)[0]

    ScraperWithLimit.allowed_domains = [domain] #trims away anything making it a url, making it into a domain
    ScraperWithLimit.start_urls = [website]
    ScraperWithLimit.custom_settings = {
        'DEPTH_LIMIT': jumps,
        'DEPTH_PRIORITY': 0,
    }
    process = CrawlerProcess()
    process.crawl(ScraperWithLimit)
    process.start()
    process.stop()
    #region database setup
    mydb = mysql.connector.connect(
        host="localhost",
        user="test",
        password="test",
        database='websites',
        auth_plugin='mysql_native_password'
    )
    mycursor = mydb.cursor()
    # drops the table if it already exists
    
    mycursor.execute("DROP TABLE IF EXISTS `%s`;" % domain)
    time.sleep(.25) #sleeps the thread as the delation actually overlaps with the creation

    # query = "CREATE TABLE `%s`(AutoID INT NOT NULL AUTO_INCREMENT PRIMARY KEY, OriginURL VARCHAR(300) NOT NULL, Hyperlink VARCHAR(300) NOT NULL)"
    # creates a table with the name of the domain being scraped.
    mycursor.execute(
        "CREATE TABLE `%s`(AutoID INT NOT NULL AUTO_INCREMENT PRIMARY KEY, OriginURL VARCHAR(300) NOT NULL, Hyperlink VARCHAR(300) NOT NULL);" % (domain))
    time.sleep(.25) #as stuff is executed asynchronously this pause is needed to make sure the sql statements are executed in correct order
    mydb.commit()
    #endregion

    for originURL, hyperlinks in dictOfUrl.items():
        for item in hyperlinks:
            if item != "" and item != "/":
                if len(item) > 1 or "http" in item: #ignores all anchor links

                    if "http" in item:
                        query = "INSERT INTO `%s` VALUES (NULL, '`%s`', '`%s`')" #backticks are used so that any character can be accepted aka the . in the url. The surrounding '' are used so that mysql doesnt mistake them for table references
                        queryParameters = (
                            domain, originURL, item,)
                        mycursor.execute(query % queryParameters)
                        
                    else:
                        query = "INSERT INTO `%s` VALUES (NULL, '`%s`', '`%s`')"
                        queryParameters = (domain, originURL, domain+item,)
                        mycursor.execute(query % queryParameters)  # appends the domain name to relative paths
                    
                    mydb.commit()
    mycursor.close()
    mydb.close()
    return True #this is done so that there can be confirmation that the program has stopped running
 

    #region legacy
    #legacy code for when output was to a file
    # file = open('yeet.txt', 'w') 
    # for x, y in dictOfUrl.items():
    #     file.write(x+", {")
    #     for item in y:
    #         if item != "" and item != "/":
    #             if item[0] == "/" or "http" in item:
    #                 if "http" not in item:
    #                     file.write(item.replace('//', '') + ", ")
    #                 else:
    #                     file.write(item + ", ")
    #     file.write("}\n")
    # file.close()
    #endregion
