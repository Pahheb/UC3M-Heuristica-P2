#!/bin/bash
# This script is used to call the ASTAR for each of the test files in the ASTAR-tests folder 

# Global variables
OUTPUT_FOLDER="ASTAR-tests/output/"
# NOTE: Different for development/final version
# OUTPUT_FOLDER="ASTAR-tests/"

# Check all .csv files in the ASTAR-tests folder
for csv_file in ASTAR-tests/*.csv; do
    if [ -f "$csv_file" ]; then
        echo -e "Testing: $csv_file..."
        echo -e "-----------------------------"
        echo -e "CALLS --- heuristicType: 1"
        # Run ASTARRodaje.py with parameter 1
        python3 ASTARRodaje.py "$csv_file" 1
        echo -e "-----------------------------\n"
        echo "CALLS --- heuristicType: 2"
        # Run ASTARRodaje.py with parameter 2
        python3 ASTARRodaje.py "$csv_file" 2
        
        echo -e "------------------------\n\n"
    fi
done

echo "FINISHED TESTING
TEST OUTPUT:
    - Output files are stored under the $OUTPUT_FOLDER folder
    - Output files are named as follows:
        - <mapa#>_<num_h>.output
        - <mapa#>_<num_h>.stat
    - .output contains the solution for each map
    - .stat contains the statistics for each map"
