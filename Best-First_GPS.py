# REMOVED EXTRA SPACE IN ADJACENCIES.TXT THAT WAS DISRUPTING DATA
# HAYS WAS IN ADJACENCIES BUT NOT IN COORDINATES. REMOVED IT AS IT HAS NO PURPOSE

# the search will use towns closest to destination

# give credit to code not written by you, outside resources are fine

import queue
import math


def adjacent_dict() -> dict:
    """
    Create a dictionary of adjacent cities and adds keys to the dictionary and updates them from
    values that are not represented
    """
    # SETUP FOR LIST TO PLACE CONTENTS OF ADJ CITIES
    adjacent_dict = {}
    fin = open("Adjacencies.txt", 'r+')

    # CREATE LIST CONTAINING LISTS OF ADJ CITIES
    # ALSO CLEAN UP UNWANTED INPUT FORMS
    for line in fin:
        line = line.strip('\n')
        line = line.split(' ')
        key = line[0]
        line.remove(key)
        values = []
        for x in line:
            values.append(x)
        adjacent_dict[key] = values

    fin.close()

    # ALLOWS FOR CITIES NOT IN KEYS OF ADJACENT DICT TO BE RECREATED AS CORRESPONDING KEY VALUES WITH PREVIOUS KEYS AS VALUES
    for key in list(adjacent_dict):
        for item in adjacent_dict[key]:
            if item not in adjacent_dict.keys():
                adjacent_dict.update({item: [key]})
            elif key not in adjacent_dict[item]:
                temp = adjacent_dict[item]
                temp.append(key)
                adjacent_dict.update({item: temp})

    adjacent_dict.pop('Hays')  # THIS WAS REMOVED BECAUSE IT WAS NOT IN COORDINATES
    return adjacent_dict


def coordinates_dict() -> dict:
    """
    Creates a dictionary with key as city name and values as coordinates
    """
    # SETUP FOR DICT TO PLACE COORDINATES OF CITIES
    coord_dict = {}
    fin = open("coordinates.txt", 'r+')

    # CREATE DICT OF CITIES WITH CORRESPONDING CITIES
    for line in fin:
        line = line.strip('\n')
        line = line.split(' ')
        coord_dict[line[0]] = line[1], line[2]

    return coord_dict


def distance_two_cities(goal: str, test: str) -> float:
    """
    Gets the distance between two cities
    """
    goal_coord = coord_dict[goal]
    test_coord = coord_dict[test]
    x = float(goal_coord[0]) - float(test_coord[0])
    y = float(goal_coord[1]) - float(test_coord[1])
    x = x * x
    y = y * y
    distance = math.sqrt(x + y)
    return distance


def best_first_search(goal: str, current: str) -> list:
    """
    Best-First-Search(Grah g, Node start)
    1) Create an empty PriorityQueue
       PriorityQueue pq;
    2) Insert "start" in pq.
       pq.insert(start)
    3) Until PriorityQueue is empty
          u = PriorityQueue.DeleteMin
          If u is the goal
             Exit
          Else
             Foreach neighbor v of u
                If v "Unvisited"
                    Mark v "Visited"
                    pq.insert(v)
             Mark u "Examined"
    End procedure

    This algorithm is from geeksforgeeks.org
    I formatted my idea for best first search with it

    This best first search starts with the start city and travels by going to the closest adjacent cities to the goal
    until the goal is reached

    """
    # SET UP EMPTY PRIORITY QUEUE
    p_queue = queue.PriorityQueue()
    # SET FIRST LOCATION IN VISITED LIST
    visited = [current]
    # LOOPS UNTIL PATH IS FOUND
    while True:
        cities = adj_dict[current]
        # LOOPS TO FIND CLOSEST CITY TO DESTINATION IN ADJACENT CITIES
        for city in cities:
            # IF THE CITY HAS ALREADY BEEN VISITED IT IS IGNORED, THIS IS TO COVER FOR DEAD ENDS (LOCAL MAX/MIN)
            if city in visited:
                pass
            # IF NOT THEN IT IS ADDED TO THE QUEUE (ALSO ALLOWS FOR BACKTRACKING)
            else:
                distance_city = (distance_two_cities(goal, city), city)
                p_queue.put(distance_city)

        place = p_queue.get()
        visited.append(place[1])

        # IF THE GOAL IS IN THE VISITED LIST THEN THE FUNCTION IS COMPLETE
        if visited[-1] == goal:
            break
        else:
            current = visited[-1]

    # VISITED SHOULD CONSIST OF ALL THE CITIES THAT HAD BEEN TRAVELLED TO
    return visited


def get_start() -> str:
    """
    This is to get the starting city
    """
    while True:
        try:
            city = input("Where are you starting from? --> ")
            if city not in coord_dict.keys():
                raise IOError
            return city
        except:
            print("Must be valid location from current database. Try again.")


def get_end() -> str:
    """
    This is to get the ending city
    """
    while True:
        try:
            city = input("What is your destination city? --> ")
            if city not in coord_dict.keys():
                raise IOError
            return city
        except:
            print("Must be valid location from current database. Try again.")


def loop_again() -> str:
    """
    This is to get user input for another trip
    """
    choices = ['Y', 'y', 'N', 'n']
    while True:
        choice = input("Would you like to take another trip? ('Y', 'N') --> ")
        if choice not in choices:
            print("Invalid answer. Please enter 'Y' or 'N'")
        else:
            if choice == 'Y' or choice == 'y':
                return True
            else:
                return False


def distance_total(places: list) -> int:
    """
    Calculate distance between visited cities
    """
    distance = 0
    # THESE CONVERSIONS ALLOW FOR APPROXIMATE KANSAS GEOGRAPHIC INFORMATION
    lat_mile_converter = 69
    lon_mile_converter = 54
    # DISTANCE FORMULA FORMATTED FOR DISTANCES BETWEEN CITIES
    for x in range(len(places) - 1):
        city_1 = coord_dict[places[x]]
        city_2 = coord_dict[places[x + 1]]
        lat = float(city_1[0]) - float(city_2[0])
        lon = float(city_1[1]) - float(city_2[1])
        lat = lat * lat_mile_converter
        lon = lon * lon_mile_converter
        lat = lat * lat
        lon = lon * lon
        dist = math.sqrt(lat + lon)
        distance += dist

    return distance


def check_specs():
    """
    This is going to be to check the speculations of the data used to create this program
    """
    print("\nThis is all the information for the adjacent city data that has been reformed and taken in\n")
    print(adj_dict)
    print(adj_dict.keys())
    print("The data has", len(adj_dict.keys()), "keys in it")

    print("\nThis is all the information for the coordinate data that has been taken in\n")
    print(coord_dict)
    print(coord_dict.keys())
    print("The data has", len(adj_dict.keys()), "keys in it")



if __name__ == "__main__":

    adj_dict = adjacent_dict()
    coord_dict = coordinates_dict()

    check_specs()

    print()

    while True:

        start = get_start()
        end = get_end()

        path = best_first_search(end, start)

        print("\nYour path to your destination will be found below\n")

        for city in path:
            if city != path[-1]:
                print(city, " -> ", end="", flush=True)
            else:
                print(city)

        print("\nThe approximate distance to travel is", round(distance_total(path), 2), "miles.\n")

        again = loop_again()

        if not again:
            break
