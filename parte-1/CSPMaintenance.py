from utils.file_processor import process_initial_file
from utils.Map import Map

import sys
import logging
logger = logging.getLogger(__name__)

from constraint import *

def main():
    logging.basicConfig(level=logging.INFO)
    routeToInitFile = sys.argv[1]
    data = process_initial_file(route=routeToInitFile)
    print("Data from the init file has been processed")
    for key in data.keys():
        print(f"{key}: ",data[key],"\n")

    slots = data["franjas"]
    matriz_size = data["matriz_size"]
    std_positions = data["std_positions"]
    spc_positions = data["spc_positions"]  
    prk_positions = data["prk_positions"]
    planes = data["planes"]
    
    planeDomain =[(i, j) for i in range(matriz_size[0]) for j in range(matriz_size[1])]
    
    problem = Problem()
    
    for plane in planes:
        problem.addVariable(plane, planeDomain)

if __name__ == '__main__':
    main()