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
    for plane in planes:
        for slot in range(slots):
            variable_name = f"av_{plane.id}_{plane.model}_{slot + 1}"
            problem.addVariable(variable_name, planeDomain)
            logging.info(f"Variable {variable_name}")
    
    # Restricción: En cada franja horaria (slot), ningún avión puede compartir la misma posición
    for slot in range(slots):
        slot_variables = [f"av_{plane.id}_{plane.model}_{slot + 1}" for plane in planes]
        problem.addConstraint(AllDifferentConstraint(), slot_variables)
        logging.info(f"Restricción AllDifferent añadida para las variables de la franja horaria {slot + 1}: {slot_variables}")
        
    # Restricción 1: Hasta 2 aviones por taller
    for slot in range(slots):
        for position in std_positions + spc_positions:  # Todas las posiciones de talleres
            # Variables que ocupan esta posición en esta franja
            slot_variables = [
                f"av_{plane.id}_{plane.model}_{slot + 1}"
                for plane in planes
            ]
            
            # Añadir una restricción que limite el número de aviones en esta posición
            def max_two_planes(*assigned_positions):
                return sum(pos == position for pos in assigned_positions) <= 2
            
            problem.addConstraint(max_two_planes, slot_variables)
            logging.info(f"Restricción: Hasta 2 aviones en posición {position} para la franja {slot + 1}")

    # Restricción 2: Máximo 1 avión JUMBO por taller
    for slot in range(slots):
        for position in spc_positions:  # Todas las posiciones de talleres
            # Variables que ocupan esta posición en esta franja
            slot_variables = [
                f"av_{plane.id}_{plane.model}_{slot + 1}"
                for plane in planes if plane.model == "JMB"
            ]
            
            # Añadir una restricción que limite el número de aviones JUMBO a 1
            def max_one_jumbo(*assigned_positions):
                return sum(pos == position for pos in assigned_positions) <= 1
            
            problem.addConstraint(max_one_jumbo, slot_variables)
            logging.info(f"Restricción: Máximo 1 avión JUMBO en posición {position} para la franja {slot + 1}")

        
    logging.info("--- Problem Solver Started ---")
    solutions = problem.getSolutions()
    logging.info(f"Número de soluciones encontradas: {len(solutions)}")
    for solution in solutions:
        logging.info(solution)

if __name__ == '__main__':
    main()