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
            planeValues:dict,
            ):

        self.value = value
        self.prev = prev
        self.cost = cost
        self.heuristicType = heuristicType
        self.map = map
        self.planeValues= planeValues

    @property
    def heuristicCost(self) -> float:
        if self.heuristicType == 1:
            return self.heuristic_manhattan()
        elif self.heuristicType == 2:
            return self.heuristic_euler()
        else:
            print("ERROR: Invalid heuristic type")
            return 0
    @property
    def totalCost(self) -> float:
        return self.cost + self.heuristicCost

    @property
    def planeGoals(self) -> list[tuple[int,int]]:
        planeGoals = []
        for key in self.planePositions:
            planeGoals.append(self.planeValues[key][1])
        return planeGoals

    @property
    def planePositions(self) -> list[tuple[int,int]]:
        planeGoals = []
        for key in self.planePositions:
            planeGoals.append(self.planeValues[key][0])
        return planeGoals

    @property
    def possibleMoves(self) -> list[tuple[int,int]]:
        moves= [(0, 0),    # wait
                (0, 1),    # up
                (0, -1),   # down
                (-1, 0),   # left
                (1, 0)]    # right
        return moves

    @property
    def finalState(self) -> bool: 
        if self.planePositions == self.planeGoals:
            return True
        return False

    # Generate all possible movement combinations
    def cartesian_product(self,lists):
        if not lists:
            return [[]]
        result = []
        for item in lists[0]:
            for rest in self.cartesian_product(lists[1:]):
                result.append([item] + rest)
        return result

    # Apply restrictions

    

    def expand_state(self)-> list[State]:
        childStates = []
        # 1. Get all possible valid and non-valid combinations
        possibleMoves= self.cartesian_product(self.possibleMoves*len(self.planeValues))
       
        # Create ChildStates:

        return child_states.sort()


    def heuristic_manhattan(self)-> float:
        """
        Compute the manhattan distance between the
        current position and goal position of each plane,
        then sum all the distances.
        """

        heuristicValue = 0
        for key in self.planeValues:
            initial = self.planeValues[key][0]
            final = self.planeValues[key][1]
            heuristicValue += abs(final[0] - initial[0]) + abs(final[1] - initial[1])
        return heuristicValue 

    def heuristic_euler(self)-> float:
        pass


def astar(open:list[State],closed:list[State]= [],goal:bool =False) -> tuple[list,list]:
    while len(open) or goal:
        if len(open) == 1:
            currentState:State = open.pop(0)
        else:
            for elem in open: 
                if not(closed.count(elem) >= 1):
                    currentState:State = elem 
                    break
                
        if currentState.finalState:
            goal = True
            break 
        else:
            closed.append(currentState)
            successors = currentState.expand_state
            open = sorted(open + successors)


    if goal:
        return get_solution(currentState)
    else:
        print(f"WARNING - NO SOLUTIONS FOUND")
        return [],[]

def get_solution(final_state:State) -> tuple[list[tuple[int,int]],list[str]]
    return  [],[]


def main():
    filename = sys.argv[1]
    planeNumber, planeValues ,map = process_file(filename)
    heuristicType = int(sys.argv[2])
    initialState = State(planeValues[0], None, 0,heuristicType,map,planeValues)
    astar([initialState])




if __name__ == "__main__":
    main()
