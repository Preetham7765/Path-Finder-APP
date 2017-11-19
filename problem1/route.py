#!/usr/bin/env python

# put your routing program here!

'''
Abstraction

State Space : Set of all cities given in road-segments.txt
Initial State : Start city
Goal State : End city
Successor Function : Set of all neighbour cities of a given city
Cost Function : Distance - gives the shortest distance between two cities
                Time - gives the shortest time within which we can reach from one city to another
                Segment - gives the shortest distance between two cities with minimum number of turns.
Heuristic-function : Straight line distance between two cities(distance)
                     Straight line distance between two cities/Max speed limit in US which is 80mph(time).
                     min cost of the segment/cost of the current segment(segment).


BFS :-
Breadth First Search algorithm searches the graph at various depth giving the shallowest node higher preference over the
deepest node. BFS searches breadth wise expanding the children of the current node before going to a level below. This
can be implemented using the "QUEUE"(FIFO) as our fringe where in immediate neighbour cities at current level are expanded
and then the cities in the next level.

DFS:-
Depth First Search algorithm searches the graph at various depth expanding the depth node first before expanding the shallowest
node at every level. This can be implemented using "STACK" as our fringe where in last neighbour city which is added to the fringe is
explored first thereby going the search depth wise.

Uniform Cost Search:-
UCS is similar to Djkstra's shortest path algorithm where in the algorithm expands the city which has the least  cummulative cost
value from the start_city city. This Greedy technique is implemented using a priority queue as our fringe where in the city with the
least cummulative cost has the highest priority. UCS behaves like BFS when the cost of the every edge from one city to snother is same

A*star :-
A*star search is similar to UCS but a heuristic value is added to the cummulative cost at every level. This heuristic value tells
us about the cost to reach the end_city from the current node. This is implemented using a priority queue as our fringe where in the city
with least sum of cummulative and heuristic value is given the highest priority.


Performance

Which search algorithm seems to work best for each routing options?
Segments :- BFS, UCS and Astar gives the optimal value, BFS taking least time to give the optimal solution. We can optimize the
            heuristic function of Astar to get much better results.

Distance :- UCS and Astar gives the optimal solution when the two cities are not far apart. As the distance between the two cities
            increases there is a slight difference between UCS and Astar since the heuristic to handle intersection is not
            optimal since it uses the greedy technique that is it finds the one with minimum value of heuristic amongest its
            neighbour. However UCS takes sometime to reach the goal state. With better handling of heuristic at intersection, Astar
            will give the best solution amongest all other searching techniques.

Time      :-UCS and Astar gives the optimal solution when the two cities are not far apart. As the distance between the two cities
            increases there is a slight difference between UCS and Astar since the heuristic to handle intersection is not very
            much optimal since it uses the greedy technique that is finds the one with minimum value of heuristic amongest its
            neighbour. However UCS takes sometime to reach the goal state. With better handling of heuristic at intersection, Astar
            will give the best solution amongest all other searching techniques.




Which algorithm is fastest in terms of the amount of computation time required by your program,
 and by how much, according to your experiments?

 Astar gives the fatest optimal solution in terms of computation time. Astar has a heuristic value which gives an approximation
 of how far the current_city is from the end city and thereby getting close to end-city with less number of cities visited.
 The worst case input for Astar is when all the edges have same cost then its time complexity becomes O(b^d) where b is the
 branching values and d is the depth of the shallowest solution. Thus Astar's runninng time will always be less than a O(b^d).
 Here are some values for inputs Bloomington,Indiana to San Diego,California where distance is the cost_function taken as
 an average over 10 loops.

 Astar : 0.274 seconds
 BFS : 0.791 seconds
 Uniform : 0.757 seconds
 DFS: 0.383 seconds

 Which algorithm requires the least memory, and by how much, according to your experiments?
 Assumming memory as the size of the fringe at any point of time, Depth First search requires least memory amongst
 the search algorithms. Worst case DFS will have O(b*d) number of nodes in the fringe where d is the maximum
 depth of the tree and b is the branching factor. In case of BFS,UCS and Astar for worst case since we are expanding
 and pushing children of each and every node into the fringe the number of nodes in the fringe can get exponential that
 is O(b^d)wher b is the branching factor and d is the depth of the tree. Thus DFS will require lesser memory than
 any other algorithms.

 Which heuristic function(s) did you use, how good is it, and how might you make it/them better?

 Segments: This heuristic function returns length of minimum segment in the entire map divided by the length ofthe
            current segment. Maximum value of this ratio is 1 when current segment length is same as the minimum
            length. Thus this value never overestimates and it is admissible.
 Distance : Straight line distance between any two points gives the shortest distance. Here the goal is to find the shortest distance
           between any two cities and this distance can never go below the straight line distance. Hence we can argue that the
           heuristic function can never over estimate the distance between any two cities. Thus this heuristic is admissible.
 Time    :  The Straight line distance between two point divided by the Maximum speed limit in US that is 80 mph is the heuristic value.
           Since distance can't be no lesser than shortest distance and speed can never go beyond 80mph, this ratio will not
           overestimate the actual optimal path.


Note: Here the heuristic values for intersection is got by using the greedy technique wherein we assign the neighbour with the
least heuristic value is assigned. If there is another intersection which is neighbour of the current intersection we simply ignore
We can recursively go down to neighbours of neighbours to get the minimum heuristic value.

'''



import sys
import math
import heapq
import time
import copy

max_speed = 80 #max speed limit in USA
minimum_value_segment = 99999 # Initial value of minimum_value_segment

'''

read input from command line

'''
def readinput():

    try:
        start_city =sys.argv[1]
        end_city = sys.argv[2]
        algo = sys.argv[3]
        cost_function = sys.argv[4]
    except IndexError:
        print("Too few arguments given. Please give the following arguments")
        print("[start-city] [end-city] [routing-algorithm] [cost-function]")
        sys.exit(0)

    return start_city,end_city,algo,cost_function

'''
Function Name: get_road_segement_data
Description : Reads road-segment.txt and city-gps.txt and converts into dictionary of cities
containing city name and their neighbours
Parameters: NONE
Return Value: dictionary of road map and gps values

'''

def get_road_segement_data():
    road_map = {}
    global minimum_value_segment
    filehandle = open('road-segments.txt','r')
    for line in filehandle.readlines():
        city_detail = line.split(" ");


        if(len(city_detail) <5):
            print(len(city_detail))

        if(city_detail[2] == '0'):
            city_detail[2] = '30'

        if(city_detail[3] == '0' or city_detail[3] == ''):
            city_detail[3] = '30'

        city_detail[3] = float(city_detail[2])/float(city_detail[3])

        if(int(city_detail[2]) < minimum_value_segment):
            minimum_value_segment = int(city_detail[2])

        if city_detail[0] in road_map.keys():
            road_map[city_detail[0]].append(city_detail[1:])
        else:
            dest_cities = []
            dest_cities.append(city_detail[1:])
            road_map[city_detail[0]] = dest_cities

        city = [city_detail[0]] + city_detail[2:]
        if city_detail[1] in road_map.keys():
            road_map[city_detail[1]].append(city)
        else:
            dest_cities = []
            dest_cities.append(city)
            road_map[city_detail[1]] = dest_cities

    filehandle.close()

    filehandle = open('city-gps.txt','r')
    gps_values = {}
    for line in filehandle.readlines():
        city_gps_value = line.split(' ')
        gps_values[city_gps_value[0]] = [city_gps_value[1]]
        gps_values[city_gps_value[0]].append(city_gps_value[2])

    filehandle.close()

    return road_map,gps_values

'''
Function Name: bfs
Description : This performs bfs given a start and end city
Parameters : Map, start and end city, cost_function
return value : Path from start city to end city
'''

def bfs(graph,start_city,end_city,cost_function):

    fringe = []
    fringe.append([start_city])
    explored = []
    while(len(fringe) > 0):
        current_path = fringe.pop(0)
        successor_cities = graph[current_path[-1]]
        for city in successor_cities:
            if(city[0] not in explored):
                if(city[0] == end_city):
                    current_path.append(end_city)
                    #print(current_path)
                    return current_path
                explored.append(city[0])
                newpath = list(current_path)
                newpath.append(city[0])
                fringe.append(newpath)
    return None


'''
check if city is there in fringe or not

'''


def check_fringe(city,fringe):
    for path in fringe:
        if(path[-1] == city):
            return True
    return False

'''
Function Name: uniform_cost_search
Description : This performs uniform cost search given a start and end city
Parameters : Map, start and end city, cost_function
return value : Path from start city to end city'''

def uniform_cost_search(graph,start_city,end_city,cost_function):

    fringe = []
    fringe.append((0,[start_city]))
    explored = []
    explored.append(start_city)
    time = 0
    distance = 0
    index = 0
    if(cost_function == 'distance'):
        index =1
    elif(cost_function == 'time'):
        index = 2
    while(len(fringe)>0):
        current_node = heapq.heappop(fringe)
        cost = current_node[0]
        current_path = current_node[1]
        current_city = current_path[-1]
        if(current_city == end_city):
            return current_path

        #explored.append(current_city
        for city in graph[current_city]:
            if cost_function == 'segments':
                new_cost = cost + 1
            else:
                new_cost = cost + float(city[index])

            if ((city[0] not in explored) and ( not check_fringe(city[0],fringe))):
                new_path = list(current_path)
                new_path.append(city[0])
                heapq.heappush(fringe,[new_cost,new_path])
                explored.append(city[0])
            else:
                for i,tup in enumerate(fringe):
                    if city[0] == tup[1][-1]:
                        if new_cost < tup[0]:
                            fringe.pop(i)
                            heapq.heapify(fringe)
                            new_path = list(current_path)
                            new_path.append(city[0])
                            heapq.heappush(fringe,[new_cost,new_path])
    return None

'''
Function Name: dfs
Description : This performs dfs  given a start and end city
Parameters : Map, start and end city, cost_function
return value : Path from start city to end city

'''

def dfs(graph,start_city,end_city,cost_function):

    fringe = []
    fringe.append([start_city])
    explored = []
    while(len(fringe) > 0):
        current_path = fringe.pop()
        successor_cities = graph[current_path[-1]]
        for city in successor_cities:
            if(city[0] not in explored):
                if(city[0] == end_city):
                    current_path.append(end_city)
                    #print(current_path)
                    return current_path
                explored.append(city[0])
                newpath = list(current_path)
                newpath.append(city[0])
                fringe.append(newpath)
    return None

'''
    Converts degrees to radians

'''

def convert_to_radians(val):
    return math.radians(val)

'''
Function Name: get_heuristic
Description : generates heuristic values for all the cities using haversine distance
Parameters : map, gps values containing latitude and longitude values, end_city and cost_function
Return value : heuristic table

'''

def get_heuristic(graph,gps_values,end_city,cost_function):


    # haversine distance formula reference :http://www.movable-type.co.uk/scripts/latlong.html

    heuristic_table = {}
    try:
        lat2,long2 = gps_values[end_city]
    except KeyError:
        print("No gps entries for end_city")
        heuristic_table[end_city] = 0
        min_cost=9999
        close_city = ""
        for city in graph[end_city]:
            if(cost_function == 'distance'):
                if(int(city[1]) < min_cost and city[0] in gps_values):
                    min_cost = int(city[1])
                    close_city = city[0]
            elif(cost_function == 'time'):
                cost = float(city[2])/float(max_speed)
                if(cost < min_cost and city[0] in gps_values):
                    min_cost = cost
                    close_city = city[0]
            elif(cost_function == 'segments'):
                cost = (float(minimum_value_segment)/float(city[1]))
                if(cost < min_cost and city[0] in gps_values):
                    min_cost = cost
                    close_city = city[0]
        lat2,long2 = gps_values[close_city]

    lat2 = convert_to_radians(float(lat2))
    long2 = convert_to_radians(float(long2))

    for city_gps_value in gps_values:
         lat1,long1 = gps_values[city_gps_value]
         lat1 = convert_to_radians(float(lat1))
         long1 = convert_to_radians(float(long1))
         delta_lat = abs(lat1 - lat2)
         delta_long = abs(long1 - long2)

         temp = (math.sin(delta_lat/2) * math.sin(delta_lat/2))+\
         math.cos(lat1) * math.cos(lat1) * (math.sin(delta_long/2) * math.sin(delta_long/2))
         distance = 6371 * 2 * math.atan2(math.sqrt(temp),math.sqrt(1-temp)) * 0.621371
         if(cost_function == 'distance'):
             heuristic_table[city_gps_value] = distance
         elif(cost_function == 'time'):
             heuristic_table[city_gps_value] = float(distance)/float(max_speed)
         elif(cost_function == 'segments'):
             if(distance == 0):
                 heuristic_table[city_gps_value] = 0
             else:
                 heuristic_table[city_gps_value] =  (float(minimum_value_segment)/float(distance))
    #for i,j in heuristic_table.items():
    #    print(i + "---->" + str(j))

    return heuristic_table

'''
    Function name: get_heuristic_intersection
    Description : Calculates heuristic value for intersection using greedy technique
    Parameters : map, heuristic_table, intersection
    return : heuristic value of the intersection


'''

def get_heuristic_intersection(graph,heuristic_table,city):
    queue = []
    queue.append(city)
    visited = []
    h_of_s = 99999
    #while(len(queue)>0):
        #curr_city = queue.pop(0)
    #for neighbour in graph[curr_city]:
    for neighbour in graph[city]:
    #    if neighbour[0] not in visited:
        #    visited.append(neighbour[0])
        try:
            if(h_of_s > heuristic_table[neighbour[0]]):
                h_of_s = heuristic_table[neighbour[0]]
        except KeyError:
            #for next_neighbour in graph[neighbour[0]]:
            #    queue.append(next_neighbour[0])
            #h_of_s = 0
            continue

    #print("********************h_of_s*************  %s"%h_of_s)
    return h_of_s
'''

Function Name: astar
Description : This performs astar search given a start and end city
Parameters : Map,gps_values for heuristic calculation, start and end city, cost_function
return value : Path from start city to end city

'''

def astar(graph,gps_values,start_city,end_city,cost_function):

    index = 0
    if(cost_function == 'distance'):
        index = 1
    elif(cost_function == 'time'):
        index = 2
    heuristic_table = get_heuristic(graph,gps_values,end_city,cost_function)
    fringe = []
    distance =0
    time = 0
    try:
        fringe.append((heuristic_table[start_city],0,[start_city]))
    except KeyError:
        h_of_s_start = get_heuristic_intersection(graph,heuristic_table,start_city)
        fringe.append((h_of_s_start,0,[start_city]))
    visited = []
    visited.append(start_city)
    while(len(fringe)>0):
        current_node = heapq.heappop(fringe)
        current_path = current_node[2]
        current_city = current_path[-1]
        #print(current_city)
        if cost_function != 'segments':
            visited.append(current_city)
        cost_value = current_node[1]
        #print(cost_value)
        if(current_city == end_city):
            #print(current_path)
            #print(cost_value)
            return current_path
        #visited.append(current_city)
        for city in graph[current_city]:
            if(cost_function == 'segments'):
                g_of_s = 1
            else:
                g_of_s = float(city[index])
            try:
                h_of_s = heuristic_table[city[0]]
            except KeyError:
                h_of_s = get_heuristic_intersection(graph,heuristic_table,city[0])
            #print(h_of_s,g_of_s,city[0])
            new_cost_value = cost_value + g_of_s
            f_of_s = new_cost_value + h_of_s


            if ((city[0] not in visited) and ( not check_fringe(city[0],fringe))):
                new_path = list(current_path)
                new_path.append(city[0])
                heapq.heappush(fringe,(f_of_s,new_cost_value,new_path))
                visited.append(city[0])
            else:
                for i,tup in enumerate(fringe):
                    if city[0] == tup[2][-1]:
                        if f_of_s < tup[0]:
                            fringe.pop(i)
                            heapq.heapify(fringe)
                            new_path = list(current_path)
                            new_path.append(city[0])
                            heapq.heappush(fringe,(f_of_s,new_cost_value,new_path))
    return None

'''
   Function Name: Trace path
   Description : Trace the path returned by search algorithm and prints in machine and human readable format.
   Parameter: Input Map and path
   Return value : NULL
'''
def trace_path(graph,path):

    total_distance = 0
    total_time = 0
    path_string = path[0] + " "
    str1 = ""
    print("".ljust(165,"_"))
    print("\n")
    print("Start City\t\t\t\t Highway\t\t   End City\t\t\t\t Distance(miles)\t\tTime(minutes)")
    print("\n")
    print("".ljust(165,"_"))
    print("\n")
    for i,city in enumerate(path[0:-1]):
        for neighbour in graph[city]:
            if(neighbour[0] == path[i+1]):
                print("%s %s %s %s %s"\
                %(city.ljust(40),neighbour[3].strip().ljust(20),neighbour[0].ljust(45),neighbour[1].ljust(30),str(int(round(neighbour[2] * 60))).ljust(10)))
                total_distance = total_distance + float(neighbour[1])
                total_time += float(neighbour[2])
                path_string+= neighbour[0]
                path_string+= " "
                print("\n")
    print(str(total_distance) + " " + str(total_time) + " " + path_string.strip())

'''
main function
'''

def main():
    start_city,end_city,algo,cost_function = readinput()

    if(start_city == end_city):
        print("Source and Destination is the same city.")
        return

    if(algo != 'bfs' and algo != 'dfs' and algo != 'uniform' and algo != 'astar'):
        print("**************Please enter proper cost function**************** ")
        print("Expected values for routing algorithm.")
        print("bfs\tdfs\tuniform\t   astar")
        print("Your Input"+ " " + algo)
        return

    if(cost_function != 'segments' and cost_function != 'distance' and cost_function != 'time'):
        print("**************Please enter proper cost function**************** ")
        print("Expected values for Cost Function.")
        print("segments\tdistance\ttime")
        print("Your Input"+ " " +cost_function)
        return



    graph,gps_values = get_road_segement_data()
    if(algo == 'bfs'):
        path = bfs(graph,start_city,end_city,cost_function)
    elif(algo == 'dfs'):
        path = dfs(graph,start_city,end_city,cost_function)
    elif(algo == 'uniform'):
        path = uniform_cost_search(graph,start_city,end_city,cost_function)
    elif(algo == 'astar'):
        path = astar(graph,gps_values,start_city,end_city,cost_function)

    if(path == None):
        print("There is no path between %s and %s"%(start_city,end_city))
        return
    trace_path(graph,path)

if __name__ == "__main__":
    main()
