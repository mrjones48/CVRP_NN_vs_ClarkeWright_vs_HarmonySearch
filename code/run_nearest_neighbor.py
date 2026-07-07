# Author: Mandy Jones
# Purpose: Runs the Nearest Neighbor algorithm on all 4 data files, 10 times
# each, and saves the results into a CSV file inside the results folder.
# Run this using: "python code/run_nearest_neighbor.py"

import time
from nearest_neighbor import read_vrp_file, nearest_neighbor, total_distance

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

number_of_trials = 10  # how many times to run ea file
all_results = [] # this will hold one line of results for ea data file

# PART 1: RUN THE ALGORITHM ON EACH DATA FILE

for filepath, best_known in data_files:

    print("Running Nearest Neighbor on", filepath)

    # read data file
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
        routes = nearest_neighbor(coords, demands, capacity, depot_id)
        end_time = time.perf_counter()

        time_taken_ms = (end_time - start_time) * 1000
        runtimes.append(time_taken_ms)

    average_runtime = sum(runtimes) / len(runtimes) # calculate the average runtime across all 10 trials

    # calculate the total distance for the routes (however it's the same every time, 
    # so just use the routes from the last trial)
    distance = total_distance(routes, coords)

    # calculate how much worse our distance is than the best-known optimal
    # as a percentage. If there's no best-known value, use "N/A"
    if best_known is not None:
        gap_percent = ((distance - best_known) / best_known) * 100
    else:
        gap_percent = "N/A"
    print("  distance:", round(distance, 2), " routes:", len(routes), " avg runtime (ms):", round(average_runtime, 4))

    # save the file's results so it can be written to the CSV file later
    all_results.append([
        filepath,
        num_customers,
        len(routes),
        round(distance, 2),
        best_known if best_known is not None else "N/A",
        round(gap_percent, 2) if gap_percent != "N/A" else "N/A",
        round(average_runtime, 4),
        number_of_trials,
    ])

# PART 2: SAVE ALL THE RESULTS INTO A CSV FILE

output_file = open("results/nearest_neighbor_results.csv", "w")

# write the header row (column names)
output_file.write("data file,num_customers,num_routes,total_distance,best value,gap_percent,avg_runtime_ms,trials\n")

# write one row per data file
for row in all_results:
    # turn every value into text then join them with commas
    row_as_text = [str(value) for value in row]
    output_file.write(",".join(row_as_text) + "\n")
output_file.close()
print()
print("Results saved to results/nearest_neighbor_results.csv")