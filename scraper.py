# Maksim Livingstone
# AH project
# SCN: 120942514

import mysql.connector
from collections import defaultdict
import time
import scrapy
from scrapy.crawler import CrawlerProcess
import sys
#this loads in the credentials for the database.
credentials = open("credentials.txt", "r").readlines()
username = credentials[0].strip().split("=")[1].replace(" ", "")
password = credentials[1].strip().split("=")[1].replace(" ", "")

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
            #this allows for the scraper to create absolute links from relative links
            slashCounter = str(next_page.root).count("../") #this is checking how many directories up the link goes
            if slashCounter > 0: #if it is relative.
                #splits the pages URL by "/" from the right. The slashcounter + 1 is due to the first slash on the right just being the current directory and we want to move up one. 
                #the first item will be the trimmed URL to append to the relative link.
                #we multiply the slash counter by 3 as there are 3 characters in "../" we take away one as we want to keep the last "/" so we don't have to insert one ourselves
                #appends the found URL to the key which is the webpage it was found on
                dictOfUrl[response.url].append(response.url.rsplit("/", slashCounter + 1)[0] + str(next_page.root)[(3*slashCounter) - 1:])
            else:
                dictOfUrl[response.url].append(str(next_page.root))
            yield response.follow(next_page, self.parse)


def runScrape(page="", jumps = 0):  # like runescape but not
    if jumps <= 0: #checks if the max number of jumps has been modified from the default value
        validInput = False
        while validInput == False:
            jumps = input("Please input the max number of jumps to be performed by the scraper \n")
            try: #we only check if the user is inputting text here as the terminal only system checks automatically
                int(jumps) #tries to convert the user input to an integer. If a type error occurs then the input was not an integer and need to be received from user again
                if int(jumps) > 0 and int(jumps)%1 == 0:
                    validInput = True
                    print("Please input a valid positive integer.")
            except ValueError:
                validInput = False
                print("Please input a valid positive integer.")


    if page == "": #checks if the page has been passed as a parameter and if it hasn't then executes the following code
        website = input("Please input the website you wish to scrape: ")
    else:
        website = page

    # trims away anything that trails after the first / and all references to http or https making it into a domain
    domain = website.replace(
        "https://", "").replace("http://", "").split("/", 1)[0]



    #this part starts up the scraper with all the required parameters
    #region scraper start
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
    try:
        mydb = mysql.connector.connect(  # connects to database
                host="localhost",
                user=username,
                password=password,
                database='websites',
                auth_plugin='mysql_native_password'
            )
    except mysql.connector.InterfaceError:
        print("""The connection to the database has been unsuccessful.
Please make sure the sql server is running, and the database has been initialised.
To initialise database please type \"CREATE DATABASE websites;\" in a suitable sql terminal and make sure the admin username and password have been entered into credentials.txt""")
        sys.exit()
    mycursor = mydb.cursor() #initialises cursor so that commands can be sent

    # drops the table if it already exists
    mycursor.execute("DROP TABLE IF EXISTS `%s`;" % domain)
    time.sleep(.25) #sleeps the thread as the deletion actually overlaps with the creation

    # creates a table with the name of the domain being scraped.
    mycursor.execute(
        "CREATE TABLE `%s`(AutoID INT NOT NULL AUTO_INCREMENT PRIMARY KEY, OriginURL VARCHAR(300) NOT NULL, Hyperlink VARCHAR(300) NOT NULL);" % (domain))
    time.sleep(.25) #as stuff is executed asynchronously this pause is needed to make sure the sql statements are executed in correct order
    mydb.commit()
    #endregion

    # backticks are used so that any character can be accepted aka the . in the URL. The surrounding '' are used so that mysql doesn't mistake them for table references
    query = "INSERT INTO `"+ domain + "` VALUES (NULL, %s, %s);"

    if domain[-1] == "/": #this removes a trailing slash at the end of URLs
        domain = domain[:-1]

    #this is so that any values that have the domain appended later will also contain the domains transfer protocol
    if "https://" in website:
        domain = "https://" + domain
    elif "http://" in website:
        domain = "http://" + domain
    print("Writing to database")

    for originURL, hyperlinks in dictOfUrl.items():
        if originURL[-1] == "/":
            originURL = originURL[:-1]
        for item in hyperlinks:
            if item != "" and item != "/":
                if len(item) > 1 or "http" in item: #ignores all anchor links
                    if item[-1] == "/": #removes any trailing slashes.
                        item = item[:-1]

                    if "http" in item:
                        queryParameters = (
                            originURL, item,)
                        mycursor.execute(query, queryParameters)
                        
                    elif item[0] != '#' and item[0] == "/": #if http is not in the item and # is not the first char we can assume that it is a relative link
                        queryParameters = (originURL, domain+item,) #appends the domain name to relative paths
                        # actually executes the sql statement with the parameters place of %s. This method also removes any sql injection attempts
                        mycursor.execute(query, queryParameters)
                        # testFile.write(originURL + ", " + domain + item + "\n") #test statement to see if any of this even works
                    elif item != '#':
                        queryParameters = (originURL, domain+'/'+item,) #appends the domain name and a slash to relative paths that are using interactive link. Seems to be rare but some websites do have it
                        mycursor.execute(query, queryParameters)  
                    mydb.commit() #commits the changes to the database
                elif item == "/": #this is to make sure that a / redirects to the home page.
                    queryParameters = (originURL, domain)
                    mycursor.execute(query, queryParameters)
                    mydb.commit()

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
