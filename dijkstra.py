#this is the class that will be used to save each webpage in a node map
from collections import defaultdict

class nodemap():
    def __init__(self):
        self.edges = defaultdict(list)
        #this is a dictionary of all possible NEXT nodes.

    def add_edge(self, origin_node, destination_node):
        #this makes an assumption that these are bidiredctional
        self.edges[origin_node].append(destination_node)
        self.edges[destination_node].append(origin_node)

nodes = nodemap()

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

#this adds the edges is into the form that has been defined in the class nodemap
#
for edge in edges:
    nodes.add_edge(*edge)

print(nodes)

def dijsktra(nodes, initial, final_destination):
    #shortest_paths is a dictionary of nodes
    # where the value is a tuple of previos node, and 1
    shortest_paths = {initial: (None, 0)}
    current_noodle = initial
    visited = set() #using a set to make sure i havent visited the node already

    while  current_noodle != final_destination:
        visited.add(current_noodle) #adds the current node to make sure we do not go back to it by accident
        destinations = nodes.edges[current_noodle]
        weight_to_current_noodle = shortest_paths[current_noodle][1]

        for next_noodle in destinations:
            weight = 1 + weight_to_current_noodle 
            if next_noodle not in shortest_paths:
                shortest_paths[next_noodle] = (current_noodle, weight)
            else:
                




