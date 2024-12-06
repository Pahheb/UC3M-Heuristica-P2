"""
This file contains all the function related with file management, processing and more
"""

import logging
logger = logging.getLogger(__name__)

def process_initial_file(route: str):
    with open(route, "r") as f:
        lines = f.readlines()

    if len(lines) < 6:
        raise ValueError("File does not have enough lines to be correctly processed")

    # 1. Número de franjas horarias
    franjas = int(lines[0].split(":")[1].strip())

    # 2. matrix size (we assume it will always be a square?)
    matriz_size = tuple(map(int, lines[1].strip().split("x")))

    # 3. std mechanic
    std_positions = [
        tuple(map(int, pos.strip("()").split(",")))
        for pos in lines[2].split(":")[1].strip().split()
    ]

    # 4. spc mechanic
    spc_positions = [
        tuple(map(int, pos.strip("()").split(",")))
        for pos in lines[3].split(":")[1].strip().split()
    ]

    # 5. parking pos
    prk_positions = [
        tuple(map(int, pos.strip("()").split(",")))
        for pos in lines[4].split(":")[1].strip().split()
    ]

    # 6. plane data
    planes = []
    for line in lines[5:]:
        plane_data = line.strip().split("-")
        plane = {
            "id": int(plane_data[0]),
            "tipo": plane_data[1],
            "restr": plane_data[2] == "T",  # True para restricciones tipo 2 antes de tipo 1
            "t1": int(plane_data[3]),
            "t2": int(plane_data[4]),
        }
        planes.append(plane)

    # json structures file
    parsed_data = {
        "franjas": franjas,
        "matriz_size": matriz_size,
        "std_positions": std_positions,
        "spc_positions": spc_positions,
        "prk_positions": prk_positions,
        "planes": planes,
    }
    
    return parsed_data