# You will need to solve a relaxed version of the NYC instance where we do not have the energy
# constraint. You can use any algorithm we discussed in the lectures. Note that this is equivalent to
# solving the shortest path problem.

import json
from queue import PriorityQueue


class Node:
    id  = ""
    coord = ()
    children = []

    childrenObj = []

    def __init__(self,id):
        self.id = id
    def set_children(self,children_list):
        self.children = children_list
    def get_children(self):
        return self.children
    def set_coord(self, Xpos, Ypos):
        self.coord  = (Xpos,Ypos)
    def get_coord(self):
        return self.coord
    def get_id(self):
        return self.id



class Edge: 
    id = ""
    FromNode = ""
    ToNode = ""
    dist = 0
    cost = 0

    ToObj = None

    def __init__(self,id):
        self.id = id
        arr = id.split(',')
        self.FromNode = arr[0]
        self.ToNode = arr[1]
    
    def get_id(self):
        return self.id
    def get_FromNode(self):
        return self.FromNode
    def get_ToNode(self):
        return self.ToNode
    def set_dist(self, distance):
        self.dist = distance
    def get_dist(self):
        return self.dist
    def set_cost(self, cost):
        self.cost = cost
    def get_cost(self):
        return self.cost



def Task1(startNodeStr,endNodeStr,Nodes,Edges):
    startNodeObj = Nodes[startNodeStr]
    visited = set()
    q = PriorityQueue()
    q.put((0,[startNodeObj.get_id()]))

    while not q.empty():
        #pull data from top of q
        currData = q.get()
        #print(currData)
        distance = currData[0]
        items = currData[1]
        currNode = Nodes[items[-1]]
        #add into set of visited node
        visited.add(currNode.get_id())
        #node 
        if len(items) <= 0 :
            continue
        else:
            
            #end loop if reach endNode
            if (currNode.get_id() == endNodeStr):
                return currData

            #insert children of currNode 
            if len(currNode.get_children()) != 0:
                for x in currNode.get_children():
                    #check if already visited
                    if not x in visited:
                        childNode = Nodes[x]
                        str = currNode.get_id() + "," + childNode.get_id()
                        edgeObj = Edges[str]

                        #prep data to be placing q
                        totaldist = edgeObj.get_dist() + distance
                        arr = items.copy()
                        arr.append(edgeObj.get_ToNode())
                        q.put((totaldist, arr))
            
    return 0


def Task2(startNodeStr,endNodeStr,Nodes,Edges,Energylimit):
    startNodeObj = Nodes[startNodeStr]
    visited = set()
    q = PriorityQueue()
    q.put((0,[startNodeObj.get_id()]))

    while not q.empty():
        #pull data from top of q
        currData = q.get()
        #print(currData)
        energy = currData[0]
        items = currData[1]
        currNode = Nodes[items[-1]]
        
        #add into set of visited node
        visited.add(currNode.get_id())

        #node 
        if len(items) <= 0 :
            continue
        else:

            #end loop if reach endNode
            if (currNode.get_id() == endNodeStr):
                return currData

            #insert children of currNode
            if len(currNode.get_children()) != 0:
                for x in currNode.get_children():
                    #check if already visited
                    if not x in visited:
                        childNode = Nodes[x]
                        str = currNode.get_id() + "," + childNode.get_id()
                        edgeObj = Edges[str]

                        #prep data to be placing q
                        totalenergy = edgeObj.get_cost() + energy
                        
                        arr = items.copy()
                        arr.append(edgeObj.get_ToNode())
                        if(totalenergy < Energylimit):
                            q.put((totalenergy, arr))
            
    return 0

def Task3(startNodeStr,endNodeStr,Nodes,Edges,Energylimit, Kenergy,Kdistance):
    startNodeObj = Nodes[startNodeStr]
    visited = set()
    q = PriorityQueue()
    q.put((0,0,0,[startNodeObj.get_id()]))

    while not q.empty():
        #pull data from top of q
        currData = q.get()
        #print(currData)
        totalenergy = currData[0]
        energy = currData[1]
        distance = currData[2]
        items = currData[3]
        currNode = Nodes[items[-1]]
        
        #add into set of visited node
        visited.add(currNode.get_id())

        #node 
        if len(items) <= 0 :
            continue
        else:


            #end loop if reach endNode
            if (currNode.get_id() == endNodeStr):
                return currData

            #insert children of currNode
            if len(currNode.get_children()) != 0:
                for x in currNode.get_children():
                    #check if already visited
                    if not x in visited:
                        childNode = Nodes[x]
                        str = currNode.get_id() + "," + childNode.get_id()
                        edgeObj = Edges[str]

                        #prep data to be placing q
                        distance  = edgeObj.get_dist()
                        score = energy*Kenergy  + distance*Kdistance
                        #for the childrens
                        totalenergy = edgeObj.get_cost() + energy

                        arr = items.copy()
                        arr.append(edgeObj.get_ToNode())
                        if(totalenergy < Energylimit):
                            q.put((score, totalenergy, distance, arr))
            
    return 0


def printout(pathArr):
    if(len(pathArr) > 1):
        edgeCount = 1
        totalDist = 0 
        totalEnergy = 0
        path = pathArr

        pathStr = "S->" + path[0] + "->"
        while edgeCount < len(path):
            EdgeInstanceId = path[edgeCount - 1] + "," + path[edgeCount]
            EdgeInstanceObj = Edges.get(EdgeInstanceId)
            totalDist = totalDist + EdgeInstanceObj.get_dist()
            totalEnergy = totalEnergy + EdgeInstanceObj.get_cost()
            pathStr = pathStr + path[edgeCount] + "->"
            edgeCount+= 1
            #print(pathStr)
        pathStr = pathStr + "E"

        print("Shortest path:",pathStr)
        print("Shortest distance:",totalDist)
        print("Total energy cost:",totalEnergy)
    else:
        pathStr = "S->" + pathArr[0] + "->E"
        print("Shortest path:",pathStr)
        print("Shortest distance:",0)
        print("Total energy cost:",0)

if __name__  == '__main__':

    coord = json.load(open('Data/Coord.json',)) 
    cost = json.load(open('Data/Cost.json',))
    dist  = json.load(open('Data/Dist.json',))
    g = json.load(open('Data/G.json',))

    Nodes = {}
    Edges = {}

    for x in coord.keys(): 
        Nodes[x] = Node(x)
    for x in Nodes.values():
        x.set_coord(coord[x.get_id()][0],coord[x.get_id()][1])
        x.set_children(g[x.get_id()])

    for y in cost.keys():
        Edges[y] = Edge(y)
    for y in Edges.values():
        y.set_cost(cost[y.get_id()])
        y.set_dist(dist[y.get_id()])

    Task1out = Task1("1","50",Nodes,Edges)
    Task2out = Task2("1","50",Nodes,Edges,287932)
    Task3out = Task3("1","50",Nodes,Edges,287932, 0.5, 0.5)


    printout(Task1out[1])
    printout(Task2out[1])
    printout(Task3out[3])
        

