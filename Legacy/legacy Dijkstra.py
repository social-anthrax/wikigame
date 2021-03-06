# Proof of itteration of Dijkstra.py

from collections import defaultdict
# import scraper.py


class noodlemap():
    #region declaration
        def __init__(self):
            self.__edges = defaultdict(list)
            self.__Matrix = [[0 for y in range(0, 1)]
                           for x in range(0, 1)]  # this initialises the 2d array as private, as python naming convention states the a double underscore is a private variable.

            #this is a dictionary of all possible NEXT noodles.
    #endregion
    #region setters
        def __add_edge(self, origin_noodle, destination_noodle):

            #adds new nodes witht the nodes they lead to. The path is assumed to be in one direction.

            self.__edges[origin_noodle].append(destination_noodle)

        def load(self, filename):    
            lines = open(filename, 'r').readlines()

            #as in python variables are hard typed, this is declaring a 2d array populated entirely by zeros

            cols_count = 2
            rows_count = len(lines)
            self.__Matrix = [[0 for x in range(cols_count)]
                                               for y in range(rows_count)]

            i_d1 = 0 #index of dimension 1
            i_d2 = 0  # index of dimension 2
            for singleLine in lines:
                singleLine = singleLine.replace(" ", "") #makes sure that there is no unnecessary spaces in the csv
                i_d2 = 0
                for y in singleLine.strip().split(','):  # splits up the two arguments and removes any new line characters.
                    self.__Matrix[i_d1][i_d2] = y
                    i_d2 += 1
                i_d1 += 1

            for index in range(0, rows_count):

                self.__add_edge(self.__Matrix[index][0], self.__Matrix[index][1])  # adds to the dictionary of edges

    #endregion
    #region getters
        def dijsktra(self, initial, final_destination):
            #shortest_paths is a dictionary of noodles
            # where the value is a tuple of previos noodle, and 1
            shortest_paths = {initial: (None, 0)}
            current_noodle = initial
            visited = set()  # using a set to make sure i havent visited the node already

            while current_noodle != final_destination:
                visited.add(current_noodle)  # adds the current node to make sure we do not go back to it by accident
                destinations = noodles.__edges[current_noodle]

                for next_noodles in destinations:
                    if next_noodles not in shortest_paths:  # checks if node has been passed yet
                        shortest_paths[next_noodles] = (current_noodle, 1)
                    else:
                        current_shortest_weight = shortest_paths[next_noodles][1]
                        if current_shortest_weight > 1:
                            shortest_paths[next_noodles] = (current_noodle, 1)


                possible_noodle = defaultdict(list)  # initialises an empty dictionary
                for noodle in shortest_paths:
                    if noodle not in visited:
                        possible_noodle[noodle] = shortest_paths[noodle]


                if not possible_noodle:  # if the next possible nodes is empty
                    return "No route can be found from %s to %s" % (initial, final_destination)
                current_noodle = min(possible_noodle, key=lambda k: possible_noodle[k][1])  # this part goes back through the destinations on shortest_paths 

            path = []  # initialises an list/array
            while current_noodle is not None:
                path.append(current_noodle)
                next_noodles = shortest_paths[current_noodle][0]
                current_noodle = next_noodles
            #itterates through the path list with a step of -1, aka backwards
            path = path[::-1]
            return path

        def returnMap(self):
            unsortedlist = list(self.__edges)  # creates an "array" of the keys of the __edges dictionary.

            for startvalue in range(1, len(unsortedlist)):

                for currentValue in range(startvalue, 0, -1):
                    for letter in range(0 , min(len(unsortedlist[currentValue]), len(unsortedlist[currentValue - 1]))): #finds the lowest length of the two urls and loops for that amount so to not go over the limit.
                        if ord(((unsortedlist[currentValue])[letter]).lower()) < ord(((unsortedlist[currentValue-1])[letter]).lower()):  # if the letters are the same then the next letter is selected so that they are still alphabetical.
                            tempLower = unsortedlist[currentValue]
                            tempHigher = unsortedlist[currentValue - 1]
                            unsortedlist[currentValue - 1] = tempLower
                            unsortedlist[currentValue] = tempHigher
                            break

                        elif len(unsortedlist[currentValue]) < len(unsortedlist[currentValue - 1]) and ord(((unsortedlist[currentValue])[letter]).lower()) == ord(((unsortedlist[currentValue-1])[letter]).lower()):  # if the values are equal and the length is different it sorts them into the correct order of shortest first for readability
                            tempLower = unsortedlist[currentValue]
                            tempHigher = unsortedlist[currentValue - 1]  # remove one of these as this is unnecessary
                            unsortedlist[currentValue - 1] = tempLower
                            unsortedlist[currentValue] = tempHigher

            sortedList = defaultdict(list)
            for key in unsortedlist:
                sortedList[key] = self.__edges[key]
            return sortedList

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
            self.__commands[key] = value

    #endregion

    #region getters
    def showUi(self, acceptCommands=True):
        print(self.__contents)
        if acceptCommands == True:
            userInput = input(self.__prompt + "   ")
            if userInput in self.__commands:
                self.__commands[userInput]()
            else:
                print("Please select a valid option.")

#the proceedures bellow simplify the proccesses

def scrape():
    import subprocess
    subprocess.Popen("scraper.py", shell=True)


def pathfinder():
    start = input(
        "Please input The webpage you wish the path to begin with. \n")
    end = input("Please input the webpage you wish the path to terminate at. \n")
    noodles.load('map.csv')
    print(noodles.dijsktra(start, end)) 


def sort():
    noodles.load('map.csv')
    print(noodles.returnMap())


def help():
    print("do this")


noodles = noodlemap()
mainMenu = ui("MainMenu")  # instanciates UI object
mainMenu.setContents(
        'Welcome to PathFinder! To see help, type: help \n Options: \n pathfinder: Finds a path between two urls \n sort. Url link finder.')
mainMenu.setCommands('Pick option', pathfinder=pathfinder,
                     sort=sort, help=help)
mainMenu.showUi()
