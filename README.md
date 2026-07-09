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
This can be done in a command prompt.

Make sure Git is installed: 
  git --version

If you don't have it, go to (https://git-scm.com/download/win) to download the installer. 
If you don't have Python, make sure to download the installer too at (https://www.python.org/downloads/).

Clone the repository:
   git clone https://github.com/mrjones48/CVRP_NN_vs_ClarkeWright_vs_HarmonySearch.git

Change to directory:
   cd CVRP_NN_vs_ClarkeWright_vs_HarmonySearch

Run all experiments and save results to CSV:
   python code/run_algorithms.py
Note: Running this will take a moment because of the Harmony Search algorithm.

Optional:
Run a particular algorithm on a single instance:
   python code/nearest_neighbor.py data/A-n32-k5.vrp

Switch out "A-n32-k5.vrp" with the following to view the results of the other datasets tested: "E-n51-k5", "E-n101-k8", and "M-n200-k16". 
To individually test these data sets with other algorithms, switch "nearest_neighbor" with "clarke_wright" or "harmony_search".

## GenAI Usage Disclosure 
This project used Claude for debugging code, understanding Python concepts, and Git/GitHub troubleshooting. All algorithmic implementation and analysis were completed by the team.
