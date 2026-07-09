# Author: Mandy Jones
# Purpose: Implements the Clarke-Wright Savings Algorithm for CVRP.
# This algorithm starts by assigning each customer their own truck, 
# which travels from the depot to that customer and back.
# For ea pair of customers, the algorithm calculates how much distance
# is saved by combining their two separate trips into one that visits 
# both customers. This will be referred to as the "savings" value. Then, 
# it sorts all savings from biggest to smallest. It will go through the 
# sorted list and merge routes, starting with the biggest savings as
# long as the following conditions are met: 
# - The two customers are at the open ends of their routes, the first or 
#   last customer in the list.
# - They aren't currently in the same route.
# - Combining them doesn't go over the truck's capacity.
# Finally, the algorithm keeps merging until no more valid merges are left. 
# You can run this using "python code/clarke_wright.py data/A-n32-k5.vrp"
# There are four data options: A-n32-k5.vrp has 31 customers, 
# E-n51-k5.vrp has 50 customers, E-n101-k8.vrp has 100 customers, 
# and M-n200-k16.vrp has 199 customers. If you want to run all four tests 
# at once and save results to CSV file (located in results/all_results.csv), 
# run "python code/run_algorithms.py"

import math

# DISTANCE CALCULATION

def distance_between(point_a, point_b):
    x1, y1 = point_a
    x2, y2 = point_b
    return math.sqrt((x1 - x2) ** 2 + (y1 - y2) ** 2)

# FIND WHICH ROUTE A CUSTOMER IS CURRENTLY IN

# This function goes thru ea route and returns the index of the route that contins said customer.
# It returns None if not found. Ideally, this shouldn't happen, but I had it to check for good practice.
def find_route_containing(customer_id, routes):
    for index in range(len(routes)):
        if customer_id in routes[index]:
            return index
    return None

# CLARKE-WRIGHT ALGORITHM

def clarke_wright(coords, demands, capacity, depot_id):

    # makes a list of every customer (except the depot)
    customers = []
    for customer_id in coords:
        if customer_id != depot_id:
            customers.append(customer_id)

    # starts with one route per customer
    # ea route is a list of customer IDs (the depot is added
    # to the start/end at the end of the function)
    routes = []
    for customer_id in customers:
        routes.append([customer_id])

    # calculates savings for every pair of customers
    # stores each one: (savings_amount, customer_1, customer_2)
    savings_list = []
    for i in range(len(customers)):
        for j in range(i + 1, len(customers)):
            customer_1 = customers[i]
            customer_2 = customers[j]

            # calculates how far it is from the depot to each customer
            dist_depot_to_1 = distance_between(coords[depot_id], coords[customer_1])
            dist_depot_to_2 = distance_between(coords[depot_id], coords[customer_2])

            # calculates how far it is between the two customers
            dist_1_to_2 = distance_between(coords[customer_1], coords[customer_2])

            # calculates how much shorter is it to visit both
            # customers in one trip instead of two separate trips
            savings_amount = dist_depot_to_1 + dist_depot_to_2 - dist_1_to_2
            savings_list.append((savings_amount, customer_1, customer_2))

    # sorts the savings from biggest to smallest, so the most
    # beneficial pairs are merged first
    savings_list.sort(key=lambda item: item[0], reverse=True)

    # go thru the sorted savings and try to merge routes
    for savings_amount, customer_1, customer_2 in savings_list:
        route_1_index = find_route_containing(customer_1, routes)
        route_2_index = find_route_containing(customer_2, routes)

        # skip if they're already in the same route
        if route_1_index == route_2_index:
            continue
        route_1 = routes[route_1_index]
        route_2 = routes[route_2_index]

        # check if customer_1 or customer_2 are at open ends
        # if stuck in the middle of a route, don't connect
        customer_1_at_start = (route_1[0] == customer_1)
        customer_1_at_end = (route_1[-1] == customer_1)
        customer_2_at_start = (route_2[0] == customer_2)
        customer_2_at_end = (route_2[-1] == customer_2)

        if not (customer_1_at_start or customer_1_at_end):
            continue

        if not (customer_2_at_start or customer_2_at_end):
            continue

        # check that merging the two routes wont go over capacity
        route_1_demand = sum(demands[c] for c in route_1)
        route_2_demand = sum(demands[c] for c in route_2)
        if route_1_demand + route_2_demand > capacity:
            continue

        # merge the two routes together. line them up so
        # customer_1 and customer_2 end up next to ea other in the merged route
        if customer_1_at_end and customer_2_at_start:
            merged_route = route_1 + route_2
        elif customer_1_at_start and customer_2_at_end:
            merged_route = route_2 + route_1
        elif customer_1_at_end and customer_2_at_end:
            merged_route = route_1 + list(reversed(route_2))
        else:  # customer_1_at_start and customer_2_at_start
            merged_route = list(reversed(route_1)) + route_2

        # remove the two old routes and add the new merged one
        # remove the higher index first so removing one doesn't shift the position of the other
        if route_1_index > route_2_index:
            routes.pop(route_1_index)
            routes.pop(route_2_index)
        else:
            routes.pop(route_2_index)
            routes.pop(route_1_index)
        routes.append(merged_route)

    # add the depot to the start and end of every final route
    final_routes = []
    for route in routes:
        final_routes.append([depot_id] + route + [depot_id])
    return final_routes

# RUNS WHEN DIRECTLY EXECUTING FILE

if __name__ == "__main__":
    import sys
    from nearest_neighbor import read_vrp_file, total_distance

    if len(sys.argv) < 2:
        print("Example: python code/clarke_wright.py data/A-n32-k5.vrp")

    filepath = sys.argv[1]
    coords, demands, capacity, depot_id = read_vrp_file(filepath)
    routes = clarke_wright(coords, demands, capacity, depot_id)
    distance = total_distance(routes, coords)

    print()
    print(f"Customers loaded:  {len(coords) - 1}")
    print(f"Truck capacity:    {capacity}")
    print()
    print("Running Clarke-Wright Savings Algorithm...")
    print()
    print(f"Routes found:      {len(routes)}")
    print(f"Total distance:    {distance:.2f}")
    print()
    print("Routes:")
    for i, route in enumerate(routes, start=1):
        print(f"Truck {i}: {route}")
