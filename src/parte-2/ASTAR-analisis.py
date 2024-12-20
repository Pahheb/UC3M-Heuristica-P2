import os
import re
import sys
import matplotlib.pyplot as plt
from collections import defaultdict
from typing import Dict, List, Tuple
from ASTARRodaje import process_file


class Test:
    """
    Class to store and manage test data for each map scenario.
    """
    def __init__(self, name: str, num_planes: int, map_tiles: int, 
                 total_time: float, initial_heuristic: int, 
                 makespan: int, expanded_nodes: int):
        self.name = name
        self.num_planes = num_planes
        self.map_tiles = map_tiles
        self.total_time = total_time
        self.initial_heuristic = initial_heuristic
        self.makespan = makespan
        self.expanded_nodes = expanded_nodes

def process_stat_file(filename: str) -> Tuple[float, int, int, int]:
    """
    Process the .stat file to extract relevant metrics.
    Returns (total_time, makespan, initial_heuristic, expanded_nodes)
    """
    try:
        with open(filename, "r") as file:
            lines = file.readlines()
            
        # Extract values using regex
        time = float(re.search(r"Tiempo total: (.+)s", lines[0]).group(1))
        makespan = int(re.search(r"Makespan: (\d+)", lines[1]).group(1))
        heuristic = int(re.search(r"h inicial: (\d+)", lines[2]).group(1))
        nodes = int(re.search(r"Nodos expandidos: (\d+)", lines[3]).group(1))
        
        return time, makespan, heuristic, nodes
    except (FileNotFoundError, AttributeError, IndexError) as e:
        print(f"Error processing stat file {filename}: {str(e)}")
        sys.exit(1)

def count_map_tiles(map_dict: Dict) -> int:
    """
    Count the total number of valid tiles (non-G) in the map.
    """
    return sum(1 for value in map_dict.values() if value != 'G')

def create_plots(tests: List[Test]):
    """
    Create all required plots for the analysis.
    """
    # 1. Test vs Total Time
    plt.figure(figsize=(12, 6))
    names = [test.name for test in tests]
    times = [test.total_time for test in tests]
    
    plt.bar(names, times)
    plt.title('Total Time per Test')
    plt.xlabel('Test Name')
    plt.ylabel('Time (seconds)')
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig('time_per_test.png')
    plt.close()

    # 2. Time by Number of Planes
    planes_dict = defaultdict(list)
    for test in tests:
        planes_dict[test.num_planes].append(test.total_time)
    
    plt.figure(figsize=(10, 6))
    boxes = plt.boxplot([times for times in planes_dict.values()],
                       labels=[f"{n} planes" for n in planes_dict.keys()])
    plt.title('Distribution of Total Time by Number of Planes')
    plt.xlabel('Number of Planes')
    plt.ylabel('Time (seconds)')
    plt.tight_layout()
    plt.savefig('time_by_planes.png')
    plt.close()

    # 3. Expanded Nodes Comparison
    plt.figure(figsize=(12, 6))
    names = [test.name for test in tests]
    nodes = [test.expanded_nodes for test in tests]
    
    plt.bar(names, nodes)
    plt.title('Expanded Nodes per Test')
    plt.xlabel('Test Name')
    plt.ylabel('Number of Expanded Nodes')
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig('expanded_nodes.png')
    plt.close()

def main():
    # Get all map files in the ASTAR-test directory
    test_dir = "ASTAR-tests"
    output_dir = os.path.join(test_dir, "outputs")
    tests = []

    # Process each map file
    for filename in os.listdir(test_dir):
        if filename.startswith("mapa") and filename.endswith(".csv"):
            # Extract map number (XX) using regex
            map_match = re.search(r"mapa(\d{2})", filename)
            if not map_match:
                continue
                
            map_num = map_match.group(1)
            
            # Skip maps numbered 09 or lower
            if int(map_num) <= 9:
                continue
                
            map_path = os.path.join(test_dir, filename)
            
            # Process map file
            num_planes, plane_values, map_data = process_file(map_path)
            map_tiles = count_map_tiles(map_data)
            
            # Process both stat files for this map
            for variant in [1, 2]:
                stat_filename = f"mapa{map_num}_{variant}.stat"
                stat_path = os.path.join(output_dir, stat_filename)
                
                time, makespan, heuristic, nodes = process_stat_file(stat_path)
                
                # Create test object with simplified name format
                test = Test(
                    name=f"{map_num}_{variant}",
                    num_planes=num_planes,
                    map_tiles=map_tiles,
                    total_time=time,
                    initial_heuristic=heuristic,
                    makespan=makespan,
                    expanded_nodes=nodes
                )
                tests.append(test)
    
    if not tests:
        print("No valid test files found (maps must be numbered greater than 09)")
        sys.exit(1)
    
    # Create all plots
    create_plots(tests)
    
    # Print summary statistics
    print("\nAnalysis Summary:")
    print("-" * 50)
    print(f"Analyzing {len(tests)} tests from maps numbered greater than 09")
    print("-" * 50)
    
    for test in sorted(tests, key=lambda x: x.name):
        print(f"\nTest: {test.name}")
        print(f"Number of planes: {test.num_planes}")
        print(f"Map tiles: {test.map_tiles}")
        print(f"Total time: {test.total_time:.2f}s")
        print(f"Initial heuristic: {test.initial_heuristic}")
        print(f"Makespan: {test.makespan}")
        print(f"Expanded nodes: {test.expanded_nodes}")

if __name__ == "__main__":
    main()
