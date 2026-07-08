
# Author: Mandy Jones
# Purpose: This file reads the CVRPLIB data file, runs the nearest neighbbor algorithm on it, and 
# prints the routes and total distance. 
# You can run this using "python code/nearest_neighbor.py data/A-n32-k5.vrp"
# There are four data options: A-n32-k5.vrp has 31 customers, E-n51-k5.vrp has 50 customers, E-n101-k8.vrp has 100 customers, 
# and M-n200-k16.vrp has 199 customers. If you want to run all four tests at once and save results to CSV file, 
# run "python code/run_nearest_neighbor.py"

import math
import sys

# READ THE DATA FILE

# This function reads the .vrp file and pulls out the following: 
# the customer's coordinates, how much ea customer needs delivered, how 
# much a truck can carry, and which costumer is the depot (the starting and ending point for the truck's route).
def read_vrp_file(filepath):

    coords = {}        # customer_id: (x, y)
    demands = {}       # customer_id: demand
    capacity = None    # how much one truck can carry
    depot_id = None    # which customer_id is the depot
    section = None     # files are split into labeled sections, so this variable keeps track of which section it's reading

    file = open(filepath, "r")  # open file
    line = file.readline()  # read first line
    while line:  # keeps going as long as there is a line. empty string means EOF
        line = line.strip() # strip() removes whitespace, tabs, and newlines

        if line == "" or line == "EOF":
            line = file.readline()
            continue

        if line.startswith("CAPACITY"): # use startswith() bc it has a value attached to it 
            capacity = int(line.split(":")[1].strip())
            line = file.readline()
            continue

        if line == "NODE_COORD_SECTION":
            section = "coords"
            line = file.readline()
            continue

        if line == "DEMAND_SECTION":
            section = "demands"
            line = file.readline()
            continue

        if line == "DEPOT_SECTION":
            section = "depot"
            line = file.readline()
            continue

        if section == "coords":
            parts = line.split() # split() breaks string into a list of substrings, by default it breaks on whitespaces and removes them
            customer_id = int(parts[0])
            x = float(parts[1])
            y = float(parts[2])
            coords[customer_id] = (x, y)

        elif section == "demands":
            parts = line.split()
            customer_id = int(parts[0])
            demand = int(parts[1])
            demands[customer_id] = demand

        elif section == "depot":
            if line == "-1":
                section = None
                line = file.readline()
                continue
            depot_id = int(line)

        line = file.readline()  # moves to next line

    file.close()  # close file

    return coords, demands, capacity, depot_id

# DISTANCE CALCULATION 

# This function calculates the distance between two points using the Pythagorean theorem
def distance_between(point_a, point_b):
    x1, y1 = point_a
    x2, y2 = point_b
    return math.sqrt((x1 - x2) ** 2 + (y1 - y2) ** 2)

# This function adds up the distance traveled across ea route in the solution
def total_distance(routes, coords):
    grand_total = 0.0
    for route in routes:
        for i in range(len(route) - 1):
            grand_total += distance_between(coords[route[i]], coords[route[i + 1]])
    return grand_total


# NEAREST NEIGHBOR ALGORITHM

# This function starts at the depot and then goes to the unvisited customer that is the closest + fits into the truck.
# It repeats this until no more customers fit and then sends the truck home and starts a new one. It keeps going until every customer is visited.
def nearest_neighbor(coords, demands, capacity, depot_id):

    customers_to_visit = set(coords.keys())
    customers_to_visit.remove(depot_id)

    all_routes = [] # ea route is a list of customer IDs, starting and ending at the depot

    while len(customers_to_visit) > 0:
        current_route = [depot_id]
        truck_space_left = capacity
        current_location = depot_id

        while True:
            closest_customer = None
            closest_distance = None

            for customer_id in customers_to_visit:
                customer_demand = demands[customer_id]

                if customer_demand > truck_space_left:
                    continue

                dist = distance_between(coords[current_location], coords[customer_id])

                if closest_distance is None or dist < closest_distance:
                    closest_distance = dist
                    closest_customer = customer_id

            if closest_customer is None:
                break

            current_route.append(closest_customer)
            truck_space_left -= demands[closest_customer]
            customers_to_visit.remove(closest_customer)
            current_location = closest_customer

        current_route.append(depot_id)
        all_routes.append(current_route)

    return all_routes

# RUNS WHEN DIRECTLY EXECUTING FILE

if __name__ == "__main__":

    # check that there is a file to read
    if len(sys.argv) < 2:
        print("Example: python code/nearest_neighbor.py data/A-n32-k5.vrp")

    filepath = sys.argv[1]
    coords, demands, capacity, depot_id = read_vrp_file(filepath)
    routes = nearest_neighbor(coords, demands, capacity, depot_id)
    distance = total_distance(routes, coords)

    print()
    print(f"Customers loaded:  {len(coords) - 1}")
    print(f"Truck capacity:    {capacity}")
    print()
    print(f"Running Nearest Neighbor...")
    print()
    print(f"Routes found:      {len(routes)}")
    print(f"Total distance:    {distance:.2f}")
    print()
    print(f"Routes:")
    for i, route in enumerate(routes, start=1):
        print(f"Truck {i}:  {route}")
