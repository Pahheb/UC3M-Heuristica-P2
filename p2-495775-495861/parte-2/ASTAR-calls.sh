#!/bin/bash
# This script is used to call the ASTAR for each of the test files in the ASTAR-tests folder 

for csv_file in "ASTAR-tests/*.csv"; do
    if [ -f "$csv_file" ]; then
        echo "Testing: $csv_file..."
        
        # Run ASTARRodaje.py with parameter 1
        python ASTARRodaje.py "$csv_file" 1
        
        # Run ASTARRodaje.py with parameter 2
        python ASTARRodaje.py "$csv_file" 2
        
        echo "------------------------"
    fi
done

echo "FINISHED TESTING\n
- TEST OUTPUT: \n
    - Output files are stored under the ASTAR-tests\output folder\n
    - Output files are named as follows: \n
        - <mapa#>_<num_h>.output\n
        - <mapa#>_<num_h>.stat\n
    - .output contains the solution for each map\n
    - .stat contains the statistics for each map\n
