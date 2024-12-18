import os
import re
import sys
import time

from dump import expand

#TODO: Think about base cases and hot to save time by using them

# GLOBAL VARIABLES:
SOLDICT = ["↓", "→", "←", "↑", "w"]
OUTDIR = "src/parte-2/ASTAR-tests/outputs/"
DEBUG = True

# NOTE: The OUTDIR for development is different form the delivery one
# OUTDIR = ".src/parte-2/ASTAR-tests/"

def process_file(filename: str) -> tuple[int, dict[int,list], dict[tuple,str]]:
    """
    This function processes a file with the format
specified and returns a tuple with the data.
    :return (int): Number of planes -> planeNumber
    :return (dict): Each plane initial and final position. -> planeValues
    :return (dict): Map of the aeroport. Each tile with its contents -> map
    """
    planeNumber = 0
    planeValues = {}
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
                planeValues[i - 1] = valuePair
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
        print(f"NOTE: File {filename} processed correctly:\
            \n {planeNumber} planes\n {planeValues} values\n {map} map")

        return planeNumber, planeValues, map

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
                print(f"ERROR --- create_output_files() --- Unvalid character ({value}) in solution")
    if len(solutionMoves) != len(solutionPoints):
        print(f"ERROR --- create_output_files() --- Unvalid solution list (diff total len)")

        for i in range(len(solutionMoves)):
            if len(solutionMoves[i]) + 1 != len(solutionPoints[i]):
                print(f"ERROR --- create_output_files() --- Unvalid solution list (diff list len)")

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
            positionValues:list,
            prev:"State|None",
            cost:float,
            heuristicType:int,
            map: dict,
            planeValues:dict,
            ):

        self.positionValues= positionValues
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

    def constraint_map(self,Values:list[tuple[int,int]]) -> list[tuple[int,int]]:
        return []

    def constraint_same_position(self,Values:list[tuple[int,int]])-> list[tuple[int,int]]:
        return [] 

    def constraint_cross(self,Values:list[tuple[int,int]])-> list[tuple[int,int]]:
        return [] 

    def get_child_cost(self,Values:list[tuple[int,int]]) -> list[float]:
        return []


    def expand_state(self) -> list["State"]:
        """
        This function expands the current state to get all the possible child states/next states.
        Based on the following rules:
        + A plane can move in any direction (up, down, left, right) or wait
        + There cannot be two planes in the same position
        + Two planes cannot cross each other

        :return (list[State]): Sorted list of all the possible child states based on their total cost
        """
        childStates = []
        childValues = []
        # Get all possible valid and non-valid combinations
        childvalues = self.cartesian_product(self.possibleMoves*len(self.planeValues))
        # Apply restrictions for non-valid combinations
        childValues = self.constraint_map(childValues)
        childValues = self.constraint_same_position(childValues)
        childValues = self.constraint_cross(childValues)
       
        # Create ChildStates:
        childCosts = self.get_child_cost(childValues)

        for i in range(len(childValues)):
            childStates.append(State(childValues[i],self,self.cost + childCosts[i],self.heuristicType,self.map,self.planeValues))

        # NOTE: Use the sorted function to sort based on total cost of objects of the class.
        return sorted(childStates, key=lambda x: x.totalCost)

    def heuristic_manhattan(self)-> float:
        """
        Compute the manhattan distance between the
        current position and goal position of each plane,
        then sum all the distances.
        :return (float): Heuristic value
        """

        heuristicValue = 0
        for key in self.planeValues:
            initial = self.planeValues[key][0]
            final = self.planeValues[key][1]
            heuristicValue += abs(final[0] - initial[0]) + abs(final[1] - initial[1])
        return heuristicValue 

    def heuristic_euler(self)-> float:
        return 0


def astar(open:list[State],closed:list[State]= [],goal:bool =False) -> tuple[float,int,State]:
    """
    This function implements the A* algorithm. 
    :param open: Open list of states. Starts with the initial state
    :param closed: Closed list of states. Starts empty
    :param goal: Boolean to check whether the goal has been reached
    :return (float): Initial heuristic value of the first state
    :return (int): Number of expanded nodes
    :return (State): Final state of the problem: Backtrack to get the solution
        -> The get_parse_solution() function will be used to get the solution
    """

    expandedNodes = 0
    currentState:State = open[0]
    initialHeuristic = currentState.heuristicCost
    
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
            expandedNodes += 1
            open = sorted(open + successors)


    if goal:
        return initialHeuristic,expandedNodes,currentState
    else:
        print(f"WARNING - NO SOLUTIONS FOUND")
        sys.exit(1)



#TODO: El código repite la creación de una lista de movimientos para luego reinterpretarla en 
# el método de create_output_files. Se podría eliminar uno de esos dos.

def get_parse_solution(final_state:State) -> tuple[int,list[list[tuple[int,int]]],list[list[str]]]:
    """
    This function returns the solution of the problem as:
    :return (int): Makespan of the solution
    :return (list): List of points for each plane
    :return (list): List of moves for each plane
    """
    return  0,[[]],[]


def main():
    startTime = time.time() # Start the timer for the whole program

    # Get and parse the input file
    filename = sys.argv[1]
    _, planeValues ,map = process_file(filename)
    heuristicType = int(sys.argv[2])

    # --- ALGORITHM
    # Create the initial state with the given data
    initialState = State(planeValues[0], None, 0,heuristicType,map,planeValues)
    startASTARTime=time.time() # Start the timer for the A* algorithm
    initialHeuristic, expandedNodes,finalState= astar([initialState])
    makespan,solutionPoints,solutionMoves = get_parse_solution(finalState)
    endTime=time.time() # Stop all timers
    # Time calculations
    totalASTARTime = endTime- startASTARTime
    totalTime = endTime - startTime
    # --- ALGORITHM
    
    # Print results
    if DEBUG:
        print(f"Total time: {totalTime}")
        print(f"Total ASTAR time: {totalASTARTime}")
        print(f"Makespan: {makespan}")
        print(f"Heuristic Type: {heuristicType}")
        print(f"Initial Heuristic: {initialHeuristic}")
        print(f"Expanded Nodes: {expandedNodes}")

    # Create output files
    create_output_files(filename,totalTime,makespan,heuristicType,initialHeuristic,expandedNodes,solutionMoves,solutionPoints)



if __name__ == "__main__":
    main()
