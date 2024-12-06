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
    logging.info("Data from the init file has been processed")
    for key in data.keys():
        logging.info("%s: %s", key, data[key])

    slots = data["franjas"]
    matriz_size = data["matriz_size"]
    std_positions = data["std_positions"]
    spc_positions = data["spc_positions"]  
    prk_positions = data["prk_positions"]
    planes = data["planes"]
    
    planeDomain =[(i, j) for i in range(matriz_size[0]) for j in range(matriz_size[1])]
    
    problem = Problem()
    logging.info("--- Creation of variable and domain asignation ---")
    for idx, plane in enumerate(planes):
        # create a variable name depending on the slot and model, each plane has n slots
        if plane.model == "STD":
            for slot in range(slots):
                variable_name = f"av_{plane.id}_STD_{slot + 1}"
                if variable_name not in problem._variables:
                    problem.addVariable(variable_name, planeDomain)
                    logging.info(f"Variable {variable_name}")
        elif plane.model == "JMB":
            for slot in range(slots):
                variable_name = f"av_{plane.id}_JMB_{slot + 1}"
                if variable_name not in problem._variables:
                    problem.addVariable(variable_name, planeDomain)
                    logging.info(f"Variable {variable_name}")

if __name__ == '__main__':
    main()