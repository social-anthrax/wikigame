#this is the class that will be used to save each webpage in a noodle map
from collections import defaultdict

class noodlemap():
    def __init__(self):
        self.edges = defaultdict(list)
        #this is a dictionary of all possible NEXT noodles.

    def add_edge(self, origin_noodle, destination_noodle):
        #this makes an assumption that these are bidiredctional
<<<<<<< HEAD
        self.edges[origin_noodle].append(destination_noodle)
        self.edges[destination_noodle].append(origin_noodle)
=======
        self.edges[origin_node].append(destination_node)
        self.edges[destination_node].append(origin_node)
        #needs commenting.
>>>>>>> 664ea4dda000372b00c1dae2ae869696ee7e6ec2

noodles = noodlemap()

#this is a test map

edges = [
    ('X', 'A'),
    ('X', 'B'),
    ('X', 'C'),
    ('X', 'E'),
    ('A', 'B'),
    ('A', 'D'),
    ('B', 'D'),
    ('B', 'H'),
    ('C', 'L'),
    ('D', 'F'),
    ('F', 'H'),
    ('G', 'H'),
    ('G', 'Y'),
    ('I', 'J'),
    ('I', 'K'),
    ('I', 'L'),
    ('J', 'L'),
    ('K', 'Y'),
]

#this adds the edges is into the form that has been defined in the class noodlemap
#
for edge in edges:
    noodles.add_edge(*edge)

print(noodles)

def dijsktra(noodles, initial, final_destination):
    #shortest_paths is a dictionary of noodles
    # where the value is a tuple of previos noodle, and 1
    shortest_paths = {initial: (None, 0)}
    current_noodle = initial
    visited = set() #using a set to make sure i havent visited the node already

    while  current_noodle != final_destination:
        visited.add(current_noodle) #adds the current node to make sure we do not go back to it by accident
        destinations = noodles.edges[current_noodle]
        weight_to_current_noodle = shortest_paths[current_noodle][1]

        for next_noodle in destinations:
            weight = 1 + weight_to_current_noodle 
            if next_noodle not in shortest_paths:
                shortest_paths[next_noodle] = (current_noodle, weight)
            else:
                current_shortest_weight = shortest_paths[next_noodle][1]
                if current_shortest_weight > weight:
                    shortest_paths[next_noodle] = (current_noodle,weight)

        next_noodle = {noodle: shortest_paths[noodle] for noodle in shortest_paths if noodle not in visited}  
        # for noodle in shortest_paths:
        #     if noodle not in visited:
        #         next_noodle = noodle
        #todo: make this work