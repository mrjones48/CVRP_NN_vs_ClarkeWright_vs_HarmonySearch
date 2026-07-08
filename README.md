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
Data from [CVRPLIB](https://galgos.inf.puc-rio.br/cvrplib/en/instances/1) is used for all three algorithms. 
In particular the algorithms use A-n32-k5, E-n51-k5, E-n101-k8, and M-n200-k16. 

## How to Run the Project
To run all algorithms and save the results to a CSV file (results found in results folder), run "python code/run_algorithms.py" or run each test individually with "python code/nearest_neighbor.py data/A-n32-k5.vrp". This prints out a table with each algorithm and its results for easy comparison. Switch out "A-n32-k5.vrp" with the following to view the results of the other datasets tested: "E-n51-k5", "E-n101-k8", and "M-n200-k16". To individually test these data sets with other algorithms, switch "nearest_neighbor" with the "clarke_wright" or "harmony_search".

## GenAI Usage Disclosure 
This project used Claude (Anthropic) for debugging code, understanding Python concepts, and Git/GitHub troubleshooting. All algorithmic implementation and analysis were completed by the team.
