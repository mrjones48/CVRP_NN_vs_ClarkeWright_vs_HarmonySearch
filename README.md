# CVRP: Nearest Neighbor vs. Clarke-Wright vs. Harmony Search

## Team Members
- [Mandy Jones](https://github.com/mrjones48)
- [Tristen Martin](https://github.com/tmartin6985)
- [Tomu Yamashita](https://github.com/Tomu150423)
- Charles Davis

## Problem Description
The CVRP finds optimal vehicle routes to deliver goods to customers while minimizing cost, with each vehicle limited by a fixed capacity. The Nearest Neighbor Heuristic, repeatedly visiting the closest unvisited customer until capacity is reached, serves as a baseline algorithm for comparison.

## Algorithms Implemented
1. Nearest Neighbor Heuristic: This will be used as the baseline algorithm. The vehicle repeatedly visits the closest unvisited customer until capacity is reached.
2. Clarke-Wright Savings Algorithm: Starts with individual routes for each customer and merges routes based on calculated savings.
3. Harmony Search: A metaheuristic that maintains a harmony memory of candidate solutions, generating new solutions through memory consideration, pitch adjustment, and randomization.

## Datasets Used
Benchmark instances from [CVRPLIB](https://vrp.atd-lab.inf.puc-rio.br/), containing customer coordinates and demand data. Problem sizes tested: 25, 50, 100, and 200 customers.

## How to Run the Project

## GenAI Usage Disclosure 
