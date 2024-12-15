import os
import re
import sys

#TODO: Think about base cases and hot to save time by using them

# GLOBAL VARIABLES:
SOLDICT = ["↓", "→", "←", "↑", "w"]
OUTDIR = "src/parte-2/ASTAR-tests/outputs/"
# NOTE: The OUTDIR for development is different form the delivery one
# OUTDIR = ".src/parte-2/ASTAR-tests/"

def process_file(filename: str) -> tuple[int, dict, dict]:
    """
    This function processes a file with the format
    specified and returns a tuple with the data.
    :return (int): Number of planes
    :return (list): Each plane initial and final position.
        + First plane has the data in position 0 and so on
    :return (list): Map of the aeroport. Each row in the input
        is represented as a list.
    """
    planeNumber = 0
    planePositions = {}
    map = {}
    # Get data file
    # Read the file
    try:
        with open(filename, "r") as file:
            lines = file.readlines()
        planeNumber = int(lines[0])

        for i in range(1, planeNumber + 1):
            # Get the (X,X) (X,X) format as
            # two pairs of values in the list using regex
            pattern = r"\((\d+),(\d+)\)\s+\((\d+),(\d+)\)"
            match = re.search(pattern, lines[i])

            if match:
                # Extracted values
                valuePair = [
                    (int(match.group(1)), int(match.group(2))),
                    (int(match.group(3)), int(match.group(4))),
                ]
                # Add the values to the list
                planePositions[i - 1] = valuePair
            else:
                print(f"ERROR: {filename} -> Position formatting seems to be wrong")
                sys.exit(1)

        mapLine = 0
        for i in range(planeNumber + 1, len(lines)):
            pattern = r"[ABG]"
            notPattern = r"[^ABG;\n]"
            match = re.findall(pattern, lines[i])
            notMatch = re.findall(notPattern, lines[i])
            if notMatch:
                print(f"ERROR: {filename} -> Map formatting seems to be wrong")
                sys.exit(1)
            else:
                if match:
                    for i in range(len(match)):
                        map[(mapLine, i)] = match[i]
            mapLine = +1

        return planeNumber, planePositions, map

    except FileNotFoundError:
        print(f"ERROR: The file {filename} was not found")
        sys.exit(1)
    except ValueError:
        print(f"ERROR: THe file {filename} is not properly encoded")
        sys.exit(1)


def create_output_files(
    filename: str,
    totalTime: float,
    makespan: int,
    heuristicType: int,
    initialHeuristic: float,
    expandedNodes: int,
    solutionMoves: list[list[str]],
    solutionPoints: list[list[tuple[int, int]]],
) -> bool:
    """
    This function creates two output files with the results and
    the statistics of the algorithm when solving the given problem.

    :param filename: Name of the input file
    :param totalTime: Total time used by the algorithm
    :param makespan: Makespan of the solution
    :param initialHeuristic: Initial heuristic value
    :param expandedNodes: Number of expanded nodes
    """

    # Parameter check:
    if heuristicType != 1 and heuristicType != 2:
        print(f"ERROR --- create_output_files() --- Unvalid heuristicType value")
        return False
    if totalTime < 0:
        print(f"ERROR --- create_output_files() --- Unvalid totalTime value (negative)")
        return False
    for element in solutionMoves:
        for value in element:
            if value not in SOLDICT:
                print(
                    f"ERROR --- create_output_files() --- Unvalid character ({value}) in solution"
                )
    if len(solutionMoves) != len(solutionPoints):
        print(
            f"ERROR --- create_output_files() --- Unvalid solution list (diff total len)"
        )

        for i in range(len(solutionMoves)):
            if len(solutionMoves[i]) + 1 != len(solutionPoints[i]):
                print(
                    f"ERROR --- create_output_files() --- Unvalid solution list (diff list len)"
                )

    # Create output filenames
    mapName = os.path.basename(filename).split(".")[0]
    testDirName = os.path.dirname(filename)
    outputFilename = f"{testDirName}/{mapName}_{heuristicType}.output"
    statFilename = f"{testDirName}/{mapName}_{heuristicType}.stat"

    # Create stat contents:
    statContents = f"Tiempo total: {totalTime}\nMakespan: {makespan}\nHeurística inicial: {initialHeuristic}\nNodos expandidos: {expandedNodes}"

    # Create output contents:
    outputContents = f""""""
    for i in range(len(solutionMoves)):
        line = f"{solutionPoints[i][0]} "
        for j in range(len(solutionMoves[i])):
            move = solutionMoves[i][j]
            point = solutionPoints[i][j + 1]
            line += f"{move}{point} "

        outputContents += f"{line}\n"

    # Create files
    try:
        with open(OUTDIR+outputFilename, "w") as outputFile:
            outputFile.write(str(outputContents))
    except:
        return False
    try:
        with open(OUTDIR+statFilename, "w") as statFile:
            statFile.write(statContents)
    except:
        return False

    return True


class State:
    def __init__(
            self,
            value:list,
            prev:State,
            cost:float,
            heuristicType:int,
            map: dict,
            planePositions:dict,
            ):

        self.value = value
        self.prev = prev
        self.cost = cost
        self.heuristicType = heuristicType
        self.map = map
        self.planePositions = planePositions

    @property
    def heuristicCost(self):
        return self.__heuristicCost

    @heuristicCost.setter
    def heuristicCost(self, heuristicCost:float):
        if type(heuristicCost) != float:
            raise TypeError("ERROR --- StateClass --- Heuristic cost must be a float")
        else:
            self.__heuristicCost = self.heuristic(self.heuristicType)


    def expand_state(self)-> list[State]:
        print(self.heuristicCost)
        child_states = []

        def operator_move() -> list[State]:
            pass
        def operator_wait() -> list[State]:
            pass

        return child_states.sort()


    def heuristic(self,heuristicType:int)-> float:

        if heuristicType == 1:
            return self.heuristic_manhattan()

        elif heuristicType==2:
            return self.heuristic_euler()

    def heuristic_manhattan(self)-> float:
        pass 

    def heuristic_euler(self)-> float:
        pass


def astar(cerrada:list,abierta:list,exito:bool =False):


    pass


def main():
    filename = sys.argv[1]
    planeNumber, planePositions,map = process_file(filename)
    heuristicType = sys.argv[2]


if __name__ == "__main__":
    main()
