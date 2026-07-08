# Author: Mandy Jones
# Purpose: Runs all algorithms: Nearest Neighbor, Clarke-Wright, and Harmony Search on all 4 data files,
# 10 times each, and saves all the results into one combined CSV file inside
# the results folder.
# Run this using: python code/run_algorithms.py

import time
from nearest_neighbor import read_vrp_file, nearest_neighbor, total_distance
from clarke_wright import clarke_wright

# List of data files we want to test, along with the best known optimal
# distance for each one (found in the COMMENT line of each .vrp data file).
# We use this later to calculate how much worse our answer is.
# M-n200-k16 doesn't have a published best value, so I just used None.
data_files = [
    ("data/A-n32-k5.vrp", 784),
    ("data/E-n51-k5.vrp", 521),
    ("data/E-n101-k8.vrp", 815),
    ("data/M-n200-k16.vrp", None),
]

# list of algorithms to run. Each one is a name for the CSV paired
# with the function that runs it
algorithms = [
    ("nearest_neighbor", nearest_neighbor),
    ("clarke_wright", clarke_wright),
]

number_of_trials = 10  # how many times to run each file

# this will hold one row of results for every algorithm + data file combo
all_results = []

# RUN EVERY ALGORITHM ON EVERY DATA FILE

for algorithm_name, algorithm_function in algorithms:

    for filepath, best_known in data_files:

        print(f"Running {algorithm_name} on {filepath}")

        # Read the data file
        coords, demands, capacity, depot_id = read_vrp_file(filepath)
        num_customers = len(coords) - 1  # minus 1 because the depot isn't a customer

        # runs the algorithm 10 times and record how long ea run takes.
        # the Nearest Neighbor gives the same routes and distance every
        # time because it doesn't use any randomness, so that's why I only saved the
        # distance once. but we still keep time of all 10 runs since the exact runtime
        # can vary slightly ea time just from normal computer background activity.
        runtimes = []

        for trial_number in range(number_of_trials):
            start_time = time.perf_counter()
            routes = algorithm_function(coords, demands, capacity, depot_id)
            end_time = time.perf_counter()

            time_taken_ms = (end_time - start_time) * 1000
            runtimes.append(time_taken_ms)

        # calculates the average runtime across all 10 trials
        average_runtime = sum(runtimes) / len(runtimes)

        # calculates the total distance for the routes (however it's the same every time, 
        # so just use the routes from the last trial)
        distance = total_distance(routes, coords)

        # calculates how much worse the distance is than the best known optimal
        # as a percentage. used "N/A" for no best known value
        if best_known is not None:
            gap_percent = ((distance - best_known) / best_known) * 100
        else:
            gap_percent = "N/A"

        print("  distance:", round(distance, 2), " routes:", len(routes), " avg runtime (ms):", round(average_runtime, 4))

        # saves the result to write to CSV later
        all_results.append([
            algorithm_name,
            filepath,
            num_customers,
            len(routes),
            round(distance, 2),
            best_known if best_known is not None else "N/A",
            round(gap_percent, 2) if gap_percent != "N/A" else "N/A",
            round(average_runtime, 4),
            number_of_trials,
        ])


# SAVE ALL THE RESULTS INTO ONE COMBINED CSV FILE

output_file = open("results/all_results.csv", "w")

# writes the header row (the column names)
output_file.write("algorithm,data file,num_customers,num_routes,total_distance,best_value,gap_percent,avg_runtime_ms,trials\n")

# writes one row per algorithm + data file combination
for row in all_results:
    # turns every value into text and then joins them with commas
    row_as_text = [str(value) for value in row]
    output_file.write(",".join(row_as_text) + "\n")

output_file.close()

print()
print("Results saved to results/all_results.csv")
