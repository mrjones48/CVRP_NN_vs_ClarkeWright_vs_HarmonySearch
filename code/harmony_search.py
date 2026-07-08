# Author: Tristen Martin
# Purpose: Implements the Harmony Search metaheuristic for CVRP.
# This algorithm keeps a memory of candidate solutions, creates new ones by
# reusing parts of the best routes, and occasionally adjusts the choices to
# explore new route orders.
# You can run this using "python code/harmony_search.py data/A-n32-k5.vrp"
# There are four data options: A-n32-k5.vrp has 31 customers, E-n51-k5.vrp has 50 customers, E-n101-k8.vrp has 100 customers, 
# and M-n200-k16.vrp has 199 customers. If you want to run all four tests at once and save results to CSV file, 
# run "python code/run_algorithms.py"

import math
import sys

from nearest_neighbor import read_vrp_file, total_distance


def distance_between(point_a, point_b):
	x1, y1 = point_a
	x2, y2 = point_b
	return math.sqrt((x1 - x2) ** 2 + (y1 - y2) ** 2)


def build_routes_from_sequence(customer_sequence, demands, capacity, depot_id):
	# turn customer order into feasible routes by starting a new truck
	# whenever the next customer would exceed capacity
	routes = []
	current_route = [depot_id]
	current_load = 0

	for customer_id in customer_sequence:
		if current_load + demands[customer_id] > capacity:
			current_route.append(depot_id)
			routes.append(current_route)
			current_route = [depot_id]
			current_load = 0

		current_route.append(customer_id)
		current_load += demands[customer_id]

	current_route.append(depot_id)
	routes.append(current_route)
	return routes


def score_sequence(sequence, demands, capacity, depot_id, coords):
	routes = build_routes_from_sequence(sequence, demands, capacity, depot_id)
	return routes, total_distance(routes, coords)


def improve_sequence(sequence, demands, capacity, depot_id, coords, attempts=12):
	# Try deterministic adjacent swaps and keep improvements.
	best_sequence = sequence[:]
	best_distance = score_sequence(best_sequence, demands, capacity, depot_id, coords)[1]

	if len(best_sequence) < 2:
		return best_sequence

	improvements_used = 0
	while improvements_used < attempts:
		candidate_best_sequence = None
		candidate_best_distance = best_distance

		for index in range(len(best_sequence) - 1):
			candidate_sequence = best_sequence[:]
			candidate_sequence[index], candidate_sequence[index + 1] = candidate_sequence[index + 1], candidate_sequence[index]
			candidate_distance = score_sequence(candidate_sequence, demands, capacity, depot_id, coords)[1]
			if candidate_distance < candidate_best_distance:
				candidate_best_sequence = candidate_sequence
				candidate_best_distance = candidate_distance

		if candidate_best_sequence is None:
			break

		best_sequence = candidate_best_sequence
		best_distance = candidate_best_distance
		improvements_used += 1

	return best_sequence


def deterministic_sequence(customers, sequence_index):
	# generate diverse but deterministic starting harmonies
	rotation = sequence_index % len(customers)
	sequence = customers[rotation:] + customers[:rotation]
	if sequence_index % 2 == 1:
		sequence = list(reversed(sequence))
	return sequence


def interval_from_rate(rate):
	if rate <= 0:
		return None
	if rate >= 1:
		return 1
	return max(1, int(round(1.0 / rate)))


def improvise_sequence(harmony_memory, customers, coords, harmony_memory_consideration_rate, pitch_adjustment_rate, iteration_number):
	# build one new harmony customer-by-customer
	# harmony memory consideration reuses an order from a stored solution,
	# and pitch adjustment nudges the choice toward a nearby customer
	harmony_sequences = [sequence for _, sequence in harmony_memory]
	remaining_customers = customers[:]
	sequence = []
	memory_interval = interval_from_rate(harmony_memory_consideration_rate)
	pitch_interval = interval_from_rate(pitch_adjustment_rate)
	step = 0

	while remaining_customers:
		use_memory = harmony_memory and memory_interval is not None and ((iteration_number + step) % memory_interval == 0)

		if use_memory:
			source_index = (iteration_number + step) % len(harmony_sequences)
			source_sequence = harmony_sequences[source_index]
			chosen_customer = next((customer_id for customer_id in source_sequence if customer_id in remaining_customers), None)
			if chosen_customer is None:
				chosen_customer = remaining_customers[0]
		else:
			chosen_customer = remaining_customers[0]

		apply_pitch = pitch_interval is not None and ((iteration_number + step) % pitch_interval == 0)
		if len(remaining_customers) > 1 and apply_pitch:
			chosen_customer = min(
				remaining_customers,
				key=lambda customer_id: distance_between(coords[chosen_customer], coords[customer_id]),
			)

		sequence.append(chosen_customer)
		remaining_customers.remove(chosen_customer)
		step += 1

	return sequence


# HARMONY SEARCH ALGORITHM

def harmony_search(
	coords,
	demands,
	capacity,
	depot_id,
	harmony_memory_size=10,
	number_of_iterations=200,
	harmony_memory_consideration_rate=0.9,
	pitch_adjustment_rate=0.25,
):

	customers = []
	for customer_id in coords:
		if customer_id != depot_id:
			customers.append(customer_id)
	customers.sort()

	harmony_memory = []

	# Initialize harmony memory using random feasible harmonies only.
	# This keeps Harmony Search fully self-contained (no seeding from other algorithms).
	while len(harmony_memory) < harmony_memory_size:
		start_sequence = deterministic_sequence(customers, len(harmony_memory))
		harmony_memory.append((score_sequence(start_sequence, demands, capacity, depot_id, coords)[1], start_sequence))

	# Keep the memory sorted so the best harmony is always first and the worst is last.
	harmony_memory.sort(key=lambda item: item[0])

	# Each iteration tries one new candidate and replaces the worst memory entry if it is better.
	for iteration_number in range(number_of_iterations):
		new_sequence = improvise_sequence(
			harmony_memory,
			customers,
			coords,
			harmony_memory_consideration_rate,
			pitch_adjustment_rate,
			iteration_number,
		)
		new_sequence = improve_sequence(new_sequence, demands, capacity, depot_id, coords)
		new_distance = score_sequence(new_sequence, demands, capacity, depot_id, coords)[1]

		if new_distance < harmony_memory[-1][0]:
			harmony_memory.append((new_distance, new_sequence))
			harmony_memory.sort(key=lambda item: item[0])
			harmony_memory = harmony_memory[:harmony_memory_size]

	# Return the best solution found in memory.
	return score_sequence(harmony_memory[0][1], demands, capacity, depot_id, coords)[0]


# RUNS WHEN DIRECTLY EXECUTING FILE

if __name__ == "__main__":
	if len(sys.argv) < 2:
		print("Example: python code/harmony_search.py data/A-n32-k5.vrp")
		sys.exit(1)

	filepath = sys.argv[1]
	coords, demands, capacity, depot_id = read_vrp_file(filepath)
	routes = harmony_search(coords, demands, capacity, depot_id)
	distance = total_distance(routes, coords)

	print()
	print(f"Customers loaded:  {len(coords) - 1}")
	print(f"Truck capacity:    {capacity}")
	print()
	print("Running Harmony Search...")
	print()
	print(f"Routes found:      {len(routes)}")
	print(f"Total distance:    {distance:.2f}")
	print()
	print("Routes:")
	for i, route in enumerate(routes, start=1):
		print(f"Truck {i}: {route}")
