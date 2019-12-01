#Maksim Livingstone

#120942514

#region imports and set up
from collections import defaultdict
import os
import sys
import importlib
import scraper
import mysql.connector
importlib.reload(scraper)
sys.setrecursionlimit(15000) #changes the recursion limit as there are a lot of values being modified in the merge sort



#endregion

def cls(): #allows the clearing of the terminal so that things can be displayed cleanly
    os.system('cls' if os.name == 'nt' else 'clear') #checks for OS type and then uses appropriate clear command for said OS
# now, to clear the screen all you need to type is: cls()

# import scraper.py
class noodlemap():
    #region declaration
        def __init__(self):
            self.__edges = defaultdict(list)
            self.__Matrix = [["" for y in range(0,1)]
                           for x in range(0,1)] #this initialises the 2d array as private, as python naming convention states the a double underscore is a private variable.
            
            #this is a dictionary of all possible NEXT noodles.
    #endregion
    #region setters
        def __addEdge(self, origin_noodle, destination_noodle):

            #adds new nodes with the nodes they lead to. The path is assumed to be in one direction.           

            self.__edges[origin_noodle].append(destination_noodle)
        
        def loadCSV(self,filename):    #currently used for loading a .csv instead of a database for testing purposes.
            lines = open(filename, 'r').readlines()
            
            #as python variables are hard typed, this is declaring a 2d array populated entirely by zeros
            
            cols_count = 2
            rows_count = len(lines)
            self.__Matrix = [["" for x in range(rows_count)] for y in range(cols_count)]

            i_d1= 0 #index of dimension 1
            i_d2 = 0 # index of dimension 2
            for singleLine in lines:
                singleLine = singleLine.replace(" ","") #makes sure that there is no unnecessary spaces in the csv
                i_d1 = 0
                for y in singleLine.strip().split(','): #splits up the two arguments and removes any new line characters.
                    self.__Matrix[i_d1][i_d2] = y
                    i_d1 += 1
                i_d2 += 1 
            
            for index in range(0, rows_count):

                self.__addEdge(self.__Matrix[0][index], self.__Matrix[1][1]) #adds to the dictionary of edges
    
        def loadDatabase(self, tableName):
            mydb = mysql.connector.connect( #connects to database
                host="localhost",
                user="test",
                password="test",
                database='websites',
                auth_plugin='mysql_native_password'
            )
            mycursor = mydb.cursor()

            mycursor.execute(
                "SELECT IF EXISTS OriginalURL, Hyperlink FROM `%s`" % tableName)

            #as python variables are hard typed, this is declaring a 2d array populated entirely by zeros
            cols_count = 2
            rows_count = len(mycursor.fetchall())
            self.__Matrix = [
                ["" for x in range(rows_count)] for y in range(cols_count)]

            i_d1 = 0  # index of dimension 1
            i_d2 = 0  # index of dimension 2
            for row in mycursor.fetchall():
                i_d1 = 0
                # splits up the two arguments and removes any new line characters.
                for value in row:
                    self.__Matrix[i_d1][i_d2] = value
                    i_d1 += 1
                i_d2 += 1

            for index in range(0, rows_count):
                # adds to the dictionary of edges
                self.__addEdge(self.__Matrix[0][index], self.__Matrix[1][1])

    
    #endregion

    #region getters
        def dijkstra(self, initial, final_destination):
            #shortest_paths is a dictionary of noodles
            #where the value is a tuple of previous noodle, and 1
            shortest_paths = {initial: (None, 0)}
            current_noodle = initial
            visited = set() #using a set to make sure node has not been visited already.

            while  current_noodle != final_destination:
                visited.add(current_noodle) #adds the current node to make sure we do not go back to it by accident
                destinations = noodles.__edges[current_noodle]

                for next_noodles in destinations:
                    if next_noodles not in shortest_paths: #checks if node has been passed yet
                        shortest_paths[next_noodles] = (current_noodle, 1)
                    else:
                        current_shortest_weight = shortest_paths[next_noodles][1]
                        if current_shortest_weight > 1:
                            shortest_paths[next_noodles] = (current_noodle,1)

                
                possible_noodle = defaultdict(list) #initialises an empty dictionary
                for noodle in shortest_paths:
                    if noodle not in visited:
                        possible_noodle[noodle] = shortest_paths[noodle]
                        
                
                if not possible_noodle: #if the next possible nodes is empty
                    return "No route can be found from %s to %s" % (initial, final_destination)
                current_noodle = min(possible_noodle, key=lambda k: possible_noodle[k][1])        #this part goes back through the destinations on shortest_paths 

            path = [] #initialises an list/array
            while current_noodle is not None:
                path.append(current_noodle)
                next_noodles =  shortest_paths[current_noodle][0]
                current_noodle = next_noodles
            #iterates through the path list with a step of -1, aka backwards
            path = path[::-1]
            return path
        
        def returnMap(self, sort=True):
            unsorted_list = list(self.__edges) #creates an "array" of the keys of the __edges dictionary.
            if sort == True:
                sorted_list = defaultdict(list)
                for key in self.MergeSort(unsorted_list): #populates dictionary with values using now sorted keys
                    sorted_list[key] = self.__edges[key]
                return sorted_list
            #region insertSort
                # this is a insertion sort as proof of understanding of advanced higher concepts
            #     for start_value in range(1, len(unsorted_list)): #a standard insertion sort
                    
            #         for current_value in range(start_value, 0, -1):
            #             for letter in range(0 ,min(len(unsorted_list[current_value]), len(unsorted_list[current_value - 1]))): #finds the lowest length of the two URLs and loops for that amount so to not go over the limit.
            #                 if ord(((unsorted_list[current_value])[letter]).lower()) < ord(((unsorted_list[current_value-1])[letter]).lower()): #if the letters are the same then the next letter is selected so that they are still alphabetical.
            #                     temp_lower = unsorted_list[current_value]
            #                     unsorted_list[current_value]= unsorted_list[current_value-1]
            #                     unsorted_list[current_value - 1]=temp_lower
            #                     break

            #                 elif len(unsorted_list[current_value]) < len(unsorted_list[current_value - 1]) and ord(((unsorted_list[current_value])[letter]).lower()) == ord(((unsorted_list[current_value-1])[letter]).lower()): #if the values are equal and the length is different it sorts them into the correct order of shortest first for readability
            #                     temp_lower = unsorted_list[current_value]
            #                     unsorted_list[current_value] = unsorted_list[current_value-1]
            #                     unsorted_list[current_value - 1] = temp_lower
                
            #     sorted_list = defaultdict(list)
            #     for key in unsorted_list:
            #         sorted_list[key] = self.__edges[key]
            # return sorted_list
            #endregion

        #region mergeSort
        def MergeSort(self, array):  # this is the python implementation of the pseudocode for the top down implementation of a merge sort on https://en.wikipedia.org/wiki/Merge_sort
            if len(array) <= 1:
                return array
            
            #Recursive case. First, divide the list into equal-sized sub lists
            #consisting of the first half and second half of the list.
            #This assumes lists start at index 0.
            left = []
            right = []
            counter = 0
            for value in array:
                if counter < len(array)//2:
                    left.append(value)
                else:
                    right.append(value)
                counter += 1
            #now recursively sort both sub lists
            left = self.MergeSort(left)
            right = self.MergeSort(right)

            sorted_list = defaultdict(list)

            #now merge both sorted sub lists
            return self.merge(left,right)
            
            
        def merge(self, left,right):
            result = []
            # result.append("test")

            while len(left) != 0 and len(right) != 0:
                # finds the lowest length of the two URLs and loops for that amount so to not go over the limit.
                for letter in range(0, min(len(left[0]), len(right[0]))):
                    
                        # if the letters are the same then the next letter is selected so that they are still alphabetical.
                    if ord(left[0][letter].lower()) < ord(right[0][letter].lower()): #ord gets the ascii value of the letter.
                        result.append(left.pop(0))
                        break
                        
                    elif ord(left[0][letter].lower()) > ord(right[0][letter].lower()):
                        result.append(right.pop(0))
                        break

                    #if the values are equal and the length is different it sorts them into the correct order of shortest first for readability
                    elif len(left[0]) < len(right[0]) and ord((left)[0][letter].lower()) == ord((right)[0][letter].lower()):
                        result.append(left.pop(0))
                        break
                    
                    elif len(left[0]) > len(right[0]) and ord((left)[0][letter].lower()) == ord((right)[0][letter].lower()):
                        result.append(right.pop(0))
                        break
                    

                        
            #Either left or right may have elements left; consume them.
            #(Only one of the following loops will actually be entered.)
            while len(left) != 0:
                result.append(left.pop(0)) #append the first value in the left array and remove the value at index 0
            
            while len(right) != 0:
                # append the first value in the right array and remove it
                result.append(right.pop(0))
            
            return result
        #endregion
        
        #endregion

class ui():
    #region setters
    def __init__(self, section):
        self.sectionName = section
        self.__contents = ""
        self.__prompt = ""
        self.__commands = defaultdict(list)

    # the kwargs is used to get a dictionary of functions that can be called by typing in the key. Instructions on how to do so were found here: https://stackoverflow.com/questions/9205081/is-there-a-way-to-store-a-function-in-a-list-or-dictionary-so-that-when-the-inde
    # use of kwargs was helped by https://www.digitalocean.com/community/tutorials/how-to-use-args-and-kwargs-in-python-3
    def setContents(self, contentsText):
        self.__contents = contentsText
        

    def setCommands(self, prompt, **kwargs):
        self.__prompt = prompt
        for key, value in kwargs.items():
            self.__commands[key.lower()] = value

    #endregion

    #region getters
    def showUi(self, acceptCommands=True):
        cls()
        print(self.__contents)
        if acceptCommands == True:
            userInput = input(self.__prompt + "   ")
            if userInput.lower() in self.__commands:
                self.__commands[userInput.lower()]()
            else:
                print("Please select a valid option.")
                input() #waits for user to press enter to continue
                self.showUi()


#the procedures bellow simplify the processes
#region simplification
def scrape():
    scraper.runScrape()
def pathfinder():
    start = input(
        "Please input The webpage you wish the path to begin with. \n")
    end = input("Please input the webpage you wish the path to terminate at. \n")
    if input("Would you like to reindex the database? (y/n) \n")[0].lower() == "y":
        scraper.runScrape(start)
    domain = start.replace(
        "https://", "").replace("http://", "").split("/", 1)[0]
    
    noodles.loadCSV(start)
    print(noodles.dijkstra(start,end)) 

def sort():
    if input("Would you like to reindex the database? (y/n) \n")[0].lower() == "y":
        start = input("Please enter the start page to begin scraping. \n")
        scraper.runScrape(start)

    domain = start.replace(
        "https://", "").replace("http://", "").split("/", 1)[0]
    noodles.loadCSV(domain) #loads csv file into the noodle object using the loadCSV method

    write_to_file = input("Do you wish to write output to file? (y/n) \n")
    cls() #clears screen
    if write_to_file.lower() == "y":
        writeFileName = input("Please input the name of the file you wish to write output to \n")
        openedFile = open(writeFileName, "w")
        if writeFileName[-4:] == ".csv": #if the file is a csv then it will write as if it is a csv
            #loops through the dictionary printing the key followed by a comma and then appends the values stored at that key
            for key, array in noodles.returnMap().items(): #gets the resulting dictionary of the result of the merge sort and then puts the key and array of the key into their respective variable by using the item() predefined procedure
                openedFile.write(key)
                for value in array:
                    openedFile.write(", " + value)
                openedFile.write("\n")
                print("%s: %s" % (key, array))
        else:
            for key, array in noodles.returnMap().items():
                openedFile.write("%s: %s \n" % (key, array))
                print("%s: %s" % (key, array))
    else:
        for key, array in noodles.returnMap().items():
            print("%s: %s" % (key, array))
    
def quit():
    print("Exiting")
    input()
    sys.exit()  # quits program      

def help():
    #TODO please for the love of god do this
    print("no")
#endregion

noodles = noodlemap()
try: #this try catch statement tries to get arguments passed in command line. If there are none then this will cause an error and UI mode is enabled.
    if sys.argv[1].lower() == "pathfinder": #sys.argv[0] is the name of the file being run
        noodles.loadCSV("map.csv")
        if sys.argv[2].lower() == "-r": #for when scaper is fully implemented
            scraper.runScrape(sys.argv[3])
            
            print(noodles.dijkstra(sys.argv[3], sys.argv[4]))
        else:
            print(noodles.dijkstra(sys.argv[2], sys.argv[3]))
    elif sys.argv[1].lower() == "returnmap":
        if sys.argv[2].lower() == "-r":
            scraper.runScrape(sys.argv[3])
        sort()
    else: 
        print("Command not recognised")
        sys.exit() #quits program
except IndexError: #catches index error caused by non existent sys.argv
    noodles = noodlemap()
    mainMenu = ui("MainMenu")  # instantiates UI object
    mainMenu.setContents('Welcome to PathFinder! To see help, type: help \n Options: \n pathfinder: Finds a path between two URLs \n ReturnMap: View all found links.')
    mainMenu.setCommands('Pick option', pathfinder=pathfinder,  returnMap=sort, help=help, quit=quit)
    mainMenu.showUi()

