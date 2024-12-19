import os
import re
import sys
import time
import math

#TODO: Think about base cases and hot to save time by using them

# GLOBAL VARIABLES:
SOLDICT = {(0,-1):"↓",(-1,0): "→", (1,0):"←", (0,1):"↑",(0,0): "w"}
OUTDIR = "./ASTAR-tests/outputs"
# NOTE: The OUTDIR for development is different form the delivery one
# OUTDIR = "./ASTAR-tests/"
DEBUG = True
MAXEXPANSION = 100000



def print_d(data):
    """
    Debug function to print only in debug mode:
    Debug mode -> DEBUG = True
    """
    if DEBUG:
        print(data)


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
                print_d(f"ERROR: {filename} -> Position formatting seems to be wrong")
                sys.exit(1)

        mapLine = 0

        for i in range(planeNumber + 1, len(lines)):
            pattern = r"[ABG]"
            notPattern = r"[^ABG;\n]"
            match = re.findall(pattern, lines[i])
            notMatch = re.findall(notPattern, lines[i])
            if notMatch:
                print_d(f"ERROR: {filename} -> Map formatting seems to be wrong")
                sys.exit(1)
            else:
                if match:
                    for i in range(len(match)):
                        map[(mapLine, i)] = match[i]
                    mapLine += 1
                else:
                    print_d(f"ERROR: {filename} -> No map values found")
                    sys.exit(1)
            
        # Check that forall planes: initial and goal values are valid
        for key in planeValues:
            startGoal = planeValues[key]
            if map.get(startGoal[0]) and map.get(startGoal[1]) and (map[startGoal[0]] == "G" or map[startGoal[1]] =="G"):
                print_d(f"ERROR: {filename} -> Invalid initial or goal value for plane {key}")


        print_d(f"NOTE -- File {filename} processed correctly:\n \
            \n * PLANES:{planeNumber} \n * VALUES: {planeValues} \n * MAP:{map} \n \n")

        return planeNumber, planeValues, map

    except FileNotFoundError:
        print_d(f"ERROR: The file {filename} was not found")
        sys.exit(1)
    except ValueError:
        print_d(f"ERROR: THe file {filename} is not properly encoded")
        sys.exit(1)


def create_output_files(
    filename: str,
    totalTime: float,
    makespan: float,
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
        print_d(f"ERROR --- create_output_files() --- Unvalid heuristicType value")
        return False
    if totalTime < 0:
        print_d(f"ERROR --- create_output_files() --- Unvalid totalTime value (negative)")
        return False
    for element in solutionMoves:
        for value in element:
            if value not in SOLDICT.values():
                print_d(f"ERROR --- create_output_files() --- Unvalid character ({value}) in solution")
    if len(solutionMoves) != len(solutionPoints):
        print_d(f"ERROR --- create_output_files() --- Unvalid solution list (diff total len)")

        for i in range(len(solutionMoves)):
            if len(solutionMoves[i]) + 1 != len(solutionPoints[i]):
                print_d(f"ERROR --- create_output_files() --- Unvalid solution list (diff list len)")

    # Create output filenames
    mapName = os.path.basename(filename).split(".")[0]
    #testDirName = os.path.dirname(filename)
    outputFilename = f"{OUTDIR}/{mapName}_{heuristicType}.output"
    statFilename = f"{OUTDIR}/{mapName}_{heuristicType}.stat"

    # Create stat contents:
    statContents = f"Tiempo total: {totalTime}s\nMakespan: {makespan}\nh inicial: {initialHeuristic}\nNodos expandidos: {expandedNodes}"

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
        with open(outputFilename, "w") as outputFile:
            outputFile.write(str(outputContents))
            print_d(f"NOTE --- Succesfully created {outputFilename}")
    except:
        print_d(f"ERROR --- create_output_files() --- Error while creating .output file")
        return False
    try:
        with open(statFilename, "w") as statFile:
            statFile.write(statContents)
            print_d(f"NOTE --- Succesfully created {statFilename}")
    except:
        print_d(f"ERROR --- create_output_files() --- Error while creating .stat file")
        return False

    return True


class State:
    def __init__(
            self,
            planePositions:list[tuple[int,int]],
            prev:"State|None",
            cost:float,
            heuristicType:int,
            map:dict[tuple[int,int],str],
            planeGoals:list[tuple[int,int]]
            
            ):

        self.planePositions= planePositions
        self.prev = prev
        self.cost = cost
        self.heuristicType = heuristicType
        self.map = map
        self.planeGoals= planeGoals 

    def __str__(self) -> str:
        string = (f"State:\n\
        * planePositions: {self.planePositions}\n\
        * Cost: {self.cost} \n\
        * HeuristicCost: {self.heuristicCost}\n\
        * TotalCost: {self.totalCost}\n\
        * planeGoals: {self.planeGoals}\n")

        return string


    @property
    def heuristicCost(self) -> float:
        # Use euler
        if self.heuristicType == 1:
            return self.heuristic_manhattan()
        # Use manhattan
        elif self.heuristicType == 2:
            return self.heuristic_euclidean()
            #return self.heuristic_euler()
        # Use dikstra
        elif self.heuristicType == 0:
            return 0
        # Use dikstra but print the error
        else:
            print_d("ERROR: Invalid heuristic type")
            return 0

    @property
    def totalCost(self) -> float:
        return self.cost + self.heuristicCost


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

    @property
    def waitCost(self) -> float:
        return 0.5
    @property
    def moveCost(self) ->float:
        return 1

    def heuristic_manhattan(self)-> float:
        """
        Compute the manhattan distance between the
        current position and goal position of each plane,
        then sum all the distances.
        :return (float): Heuristic value
        """

        heuristicValues = []
        for i in range(len(self.planePositions)):
            initial = self.planePositions[i]
            final = self.planeGoals[i]
            heuristicValues.append(abs(final[0] - initial[0]) + abs(final[1] - initial[1]))
        return max(heuristicValues)

    def heuristic_euclidean(self)-> float:
        """
        Compute the euclidean distance between the
        current position and the goal position of each plane.
        :return (float): Heuristic value
        """
        heuristicsValues = []
        for i in range(len(self.planePositions)):
            initial = self.planePositions[i]
            final = self.planeGoals[i]
            heuristicsValues.append(math.sqrt((final[0] - initial[0])**2 + (final[1] - initial[1])**2))
        return max(heuristicsValues)
    
    def heuristic_floydWarshall(self)-> float:
        """
        Compute the Floyd-Warshall algorithm, used for
        calculating the optimal cost between a couple of
        edges.
        :return (float): Heuristic value
        """
        return 0

    def condition_free(self,values:list[tuple[int,int]])-> bool:
        """
        Check that all the positions in the list are 
        free positions in the map.
        All positions are free if they are not "G" in the map.

        :param Values: List of tuples with the positions to check
        """
        for elem in values:
            if self.map[elem] == "G":
                return False
        return True

    def condition_in_map(self,values:list[tuple[int,int]])-> bool:
        """
        Check that all the positions in the list are 
        inside the map.
        :param Values: List of tuples with the positions to check
        """
        for elem in values:
            if not self.map.get(elem):
                return False
        return True

    def condition_same_position(self,values:list[tuple[int,int]])-> bool:
        """
        Check that no two values in the list are the same.
        :param Values: List of tuples with the positions to check
        """
        for i in range(len(values)):
            for j in range(i+1,len(values)):
                if values[i] == values[j]:

                    return False
        return True

    def condition_cross(self,values:list[tuple[int,int]])-> bool:
        """
        Check that no two planes cross each other.Compare the given list
        of values with the current positions of the planes.
        :param Values: List of tuples with the positions to
        """
        
        for i in range(len(values)):
            for j in range(len(self.planePositions)):
                if i == j:
                    continue
                if self.planePositions[j] == values[i] and values[j] == self.planePositions[i]:
                    return False
                    
        return True

    def condition_wait(self,values:list[tuple[int,int]])-> bool:
        """
        Check that a plane can only wiat if the map position is not "A"
        :param Values: List of tuples with the positions to check
        """
        for i in range(len(values)):
            if (values[i] == self.planePositions[i]) and (self.map[values[i]] == "A"):
                return False
        return True


    def get_child_cost(self,values:list[tuple[int,int]]) -> float:
        """
        Given a list of moves of a plane, get the cost of the state change.
        :param Values: List of tuples with the moves of the planes
        """
        totalCost = 0 
        for elem in values:
            if elem == (0,0):
                totalCost += self.waitCost
            else:
                totalCost += self.moveCost

        return totalCost/len(values)

    def operator_move(self) -> tuple[list[list[tuple[int,int]]],list[list[tuple[int,int]]]]:
        """
        Compute the Cartesian product of a set with itself n times,then
        apply the conditions to get the valid combinations.

        :param input_set: Set of tuples, where each tuple contains two integers
        :param n: Number of times to compute the product
        :return (list): List of lists with the valid combinations (childPositionValues)
        :return (list): List of lists with the moves to get the valid combinations (childMoveValues)

        Preconditions:
        * Adjacency: The next position will be adjacent to the current one
        * Free: Checked usig condition_free()
        * Same Position: Checked using condition_same_position()
        * Cross: Checked using condition_cross()
        * Wait: Checked using condition_wait()

        """
        input_set = self.possibleMoves
        n = len(self.planePositions)
        # Initialize result list
        result = ([], [])

        if n <= 0:
            print_d("ERROR -- Plane positions is empty")
            return result
        
        # Convert set to sorted list for consistent ordering
        # For tuples, we sort based on both elements of the tuple
        elements = sorted(list(input_set), key=lambda x: (x[0], x[1]))
        setSize = len(elements)
        
        # Total number of combinations remains the same
        # If we have k tuples and select n times, we get k^n combinations
        totalCombinations = setSize ** n
        
        # Generate each combination
        for i in range(totalCombinations):
            # Current combination
            moves = []
            # List of tuples with the new positions
            positions = []
            temp = i
            
            # The base conversion process remains the same
            # But now each selected element is a tuple instead of a number
            for _ in range(n):
                moves.append(elements[temp % setSize])
                temp //= setSize 
            
            # Apply moves to current position 
            for i in range(len(moves)):
                newPosition = moves[i][0] + self.planePositions[i][0],moves[i][1] + self.planePositions[i][1]
                positions.append(newPosition)

            # Check conditions:
            #print_d(f"MOVES_PRE: {moves}")
            #print_d(f"POS_PRE: {positions}")
            if self.condition_in_map(positions):
                #print_d(f"MOVES_MAP: {moves}")
                #print_d(f"POS_MAP: {positions}")
                if self.condition_free(positions):
                    #print_d(f"MOVES_FREE: {moves}")
                    #print_d(f"POS_FREE: {positions}")
                    if self.condition_same_position(positions):
                        #print_d(f"MOVES_SAME: {moves}")
                        #print_d(f"POS_SAME: {positions}")
                        if self.condition_wait(positions):
                            #print_d(f"MOVES_WAIT: {moves}")
                            #print_d(f"POS_WAIT: {positions}")
                            if self.condition_cross(positions):
                                result[0].append(positions)
                                result[1].append(moves)
                                #print_d(f"MOVES_POST: {moves}")
        return result
   

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
        childCosts = []
        childPositionValues,childMoveValues = self.operator_move()

        # Create ChildStates:
        for elem in childMoveValues:
            childCosts.append(self.get_child_cost(elem))

        for i in range(len(childPositionValues)):
            childStates.append(State(childPositionValues[i],self,self.cost + childCosts[i],self.heuristicType,self.map,self.planeGoals))

        # NOTE: Use the sorted function to sort based on total cost of objects of the class.
        return sorted(childStates, key=lambda x: x.totalCost)

    

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
    
    while len(open) >= 1  or goal:
        currentState = open.pop(0)
        
        if currentState.finalState:
            print_d("NOTE -- Goal reached")
            goal = True
            break

        if currentState in closed:
            continue
        
        if MAXEXPANSION and expandedNodes >= MAXEXPANSION:
            break

        successors = currentState.expand_state()
        open = sorted(open + successors, key=lambda x: x.totalCost)
        expandedNodes += 1
        print_d(f"NOTE -- Expanded Nodes: {expandedNodes}")
        sys.stdout.write("\033[F") # Cursor up one line
        sys.stdout.write("\033[K") # Clear to the end of line
                    

    if goal:
        print_d(f"NOTE -- Finished A* algorithm") 
        return initialHeuristic,expandedNodes,currentState

    elif len(open) == 0:
        print_d(f"WARNING -- NO SOLUTIONS FOUND WITH {expandedNodes} EXPANDED NODES")
        sys.exit(1)

    else:
        print_d(f"WARNING -- EXITED A*")
        sys.exit(1)



#TODO: El código repite la creación de una lista de movimientos para luego reinterpretarla en 
# el método de create_output_files. Se podría eliminar uno de esos dos.

def get_parse_solution(final_state: State) -> tuple[int, list[list[tuple[int, int]]], list[list[str]]]:
    """
    Reconstructs the solution path from the final state by backtracking.
    
    Args:
        final_state: The goal state reached by A*
        
    Returns:
        tuple: (makespan, list of position sequences, list of move sequences)
    """
    # Initialize tracking for each plane
    num_planes = len(final_state.planePositions)
    position_sequences = [[] for _ in range(num_planes)]
    move_sequences = [[] for _ in range(num_planes)]
    
    # Backtrack through states
    current_state = final_state
    makespan = 0
    
    while current_state:
        # Record positions for each plane
        for i in range(num_planes):
            position_sequences[i].insert(0, current_state.planePositions[i])
            
        # Determine moves by comparing consecutive states
        if current_state.prev:
            makespan += 1
            for i in range(num_planes):
                current_pos = current_state.planePositions[i]
                prev_pos = current_state.prev.planePositions[i]
                
                # Calculate move direction
                dx = current_pos[0] - prev_pos[0]
                dy = current_pos[1] - prev_pos[1]
                
                # Convert to move symbol
                if (dx, dy) == (0, 0):
                    move_sequences[i].insert(0, "w")
                elif (dx, dy) == (0, 1):
                    move_sequences[i].insert(0, "→")
                elif (dx, dy) == (0, -1):
                    move_sequences[i].insert(0, "←")
                elif (dx, dy) == (1, 0):
                    move_sequences[i].insert(0, "↓")
                elif (dx, dy) == (-1, 0):
                    move_sequences[i].insert(0, "↑")
                    
        current_state = current_state.prev
        
    return makespan, position_sequences, move_sequences

def heuristic_floydWarshall(map: dict) -> list[list[float]]:
    """
    Compute the Floyd-Warshall algorithm with wall detection.
    Nodes are considered adjacent only if they are Manhattan distance 1 apart
    and at least one of them is not a wall ("G").
    
    Args:
        map (dict): Dictionary where keys are coordinate tuples and values are cell types
        
    Returns:
        list[list[float]]: Distance matrix with minimum costs between nodes
    """
    # Initialize the mapping from node indices to their positions
    n = 1
    nodes = {}
    for i in map.keys():
        nodes[n] = i
        n += 1
    num_nodes = len(nodes)
    
    # Initialize the distance matrix with infinities
    distanceArray = [[float('inf')] * num_nodes for _ in range(num_nodes)]
    
    # Distance from a node to itself is 0
    for i in range(num_nodes):
        distanceArray[i][i] = 0
        
    # Populate the adjacency matrix
    for i in range(1, num_nodes + 1):
        for j in range(1, num_nodes + 1):
            if i != j:
                pos_i = nodes[i]
                pos_j = nodes[j]
                
                # Check if positions are adjacent (Manhattan distance of 1)
                manhattan_dist = abs(pos_i[0] - pos_j[0]) + abs(pos_i[1] - pos_j[1])
                
                if manhattan_dist == 1:
                    # Check if at least one position is not a wall
                    if map[pos_i] != "G" and map[pos_j] != "G":
                        distanceArray[i - 1][j - 1] = 1
                    else:
                        distanceArray[i-1][j-1] = float('inf')
    
    # Floyd-Warshall algorithm
    for k in range(num_nodes):
        for i in range(num_nodes):
            for j in range(num_nodes):
                # Update the distance to the minimum via an intermediate node
                distanceArray[i][j] = min(
                    distanceArray[i][j], 
                    distanceArray[i][k] + distanceArray[k][j]
                )
                
    return distanceArray  # returns the adjacency matrix with the minimum cost


def main():
    startTime = time.time() # Start the timer for the whole program

    # Get and parse the input file
    filename = sys.argv[1]
    _, planeValues ,map = process_file(filename)
    heuristicType = int(sys.argv[2])

    # Get planePositions and planeGoals
    planeInitialPositions = []
    planeGoals= []
    for key in planeValues:
        planeInitialPositions.append(planeValues[key][0])
        planeGoals.append(planeValues[key][1])

    # --- CALL ALGORITHM
    # Create the initial state with the given data
    initialState = State(planeInitialPositions, None, 0,heuristicType,map,planeGoals)
    startASTARTime=time.time() # Start the timer for the A* algorithm
    initialHeuristic, expandedNodes,finalState= astar([initialState])
    makespan,solutionPoints,solutionMoves = get_parse_solution(finalState)
    endTime=time.time() # Stop all timers
    # Time calculations
    totalASTARTime = endTime- startASTARTime
    totalTime = endTime - startTime
    # --- CALL ALGORITHM
    
    # Print results
    output = f"""\n
    --------------------
    Total time: {totalTime} s 
    Total ASTAR time: {totalASTARTime} s
    Makespan: {makespan}
    Heuristic Type: {heuristicType}
    Initial Heuristic: {initialHeuristic}
    Expanded Nodes: {expandedNodes}
    -------------------\n
    """
    print_d(output)

    # Create output files
    if not (create_output_files(filename,totalTime,makespan,heuristicType,initialHeuristic,expandedNodes,solutionMoves,solutionPoints)):
        print_d("WARNING -- Output files not properly created")
    
    # Print floydWarshall heuristic
    print_d(f"HEURISTIC FLOYD-WARSHALL: {heuristic_floydWarshall_2(map)}")


if __name__ == "__main__":
    main()
