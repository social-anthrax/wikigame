
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

class ScraperWithLimit(scrapy.Spider): #this is largely beyond ah level
    name = "ScraperWithLimit"
    start_urls = [
        #these are all test case websites with known outputs
        # 'https://en.wikipedia.org/wiki/Web_scraping',
        # 'https://en.wikipedia.org/wiki/Pok%C3%A9mon',
    ]

    allowed_domains = [domain]

    custom_settings = {
        'DEPTH_LIMIT': 1,
        'DEPTH_PRIORITY': 0,
    }

    def parse(self, response):
        for next_page in response.css('a::attr(href)'):
            
            dictOfUrl[response.url].append(str(next_page.root)) #appends the found url to the jey which is the webpage it was found on
            yield response.follow(next_page, self.parse)

        


def runScrape(page="", jumps = 0):  # like runescape but not
    if jumps == 0: #checks if the max number of jumps has been modified from the default value
        validInput = False
        while validInput == False:
            jumps = input("Please input the max number of jumps to be performed by the scraper \n")
            try:
                int(jumps) #tries to convert the user input to an integer. If a type error occurs then the input was not an integer and need to be recieved from user again
                validInput = True
            except ValueError:
                validInput = False
                print("Please input a valid positive integer.")
    else:
        jumps = 5 #changes it to what is seen as a reasonable default value


    if page == "": #checks if the page has been passed as a parameter and if it hasnt then 
        website = input("Please input the website you wish to scrape: ")
    else:
        website = page

    # trims away anything that trails the first / and all references to http or https making it into a domain
    domain = website.replace(
        "https://", "").replace("http://", "").split("/", 1)[0]



    #this paret starts up the scraper with all the required parameters
    #region scraper  
    ScraperWithLimit.allowed_domains = [domain] 
    ScraperWithLimit.start_urls = [website]
    ScraperWithLimit.custom_settings = {
        'DEPTH_LIMIT': jumps,
        'DEPTH_PRIORITY': 0,
    }
    process = CrawlerProcess()
    process.crawl(ScraperWithLimit)
    process.start()
    process.stop()
    #endregion
    #region database setup
    mydb = mysql.connector.connect( #connect to database as user test.
        host="localhost",
        user="test",
        password="test",
        database='websites',
        auth_plugin='mysql_native_password'
    )
    mycursor = mydb.cursor() #initiallises cursor so that commands can be sent

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

    # backticks are used so that any character can be accepted aka the . in the url. The surrounding '' are used so that mysql doesnt mistake them for table references
    query = "INSERT INTO `"+ domain + "` VALUES (NULL, %s, %s);"

    #this is so that any values that have the domain appended later will also contain the domains transfer protocol
    if "https://" in website:
        domain = "https://" + domain
    elif "http://" in website:
        domain = "http://" + domain
    print("Writing to database")

    for originURL, hyperlinks in dictOfUrl.items():
        for item in hyperlinks:
            if item != "" and item != "/":
                if len(item) > 1 or "http" in item: #ignores all anchor links
                    if "http" in item:
                        queryParameters = (
                            originURL, item,)
                        mycursor.execute(query, queryParameters)
                        
                    elif item[0] != '#' and item[0] == "/": #if http is not in the item and # is not the first char we can assume that it is a relative link
                        queryParameters = (originURL, domain+item,) #appends the domain name to relative paths
                        mycursor.execute(query, queryParameters)  #actually executes the sql statement with the parameters place of %s. This method also removes any sal injection attempts
                        # testFile.write(originURL + ", " + domain + item + "\n") #test statement to see if any of this even works
                    elif item != '#':
                        queryParameters = (originURL, domain+'/'+item,) #appends the domain name and a slash to relative paths that are using interactive link. Seems to be rare but some websites do have it
                        mycursor.execute(query, queryParameters)  

                    mydb.commit() #commits the changes to the database
    mycursor.close()
    mydb.close()
    return True #this is done so that there can be confirmation that the program has stopped running as problems arose due to seeming asynchronous execution of select statements while values were being inserted
 

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
