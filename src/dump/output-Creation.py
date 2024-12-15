import os
import sys

# GLOBAL VARIABLES:
SOLDICT= ["↓", "→","←","↑","w"]
OUTDIR = "src/dump/tests/outputs/"
def create_output_files(
    filename: str,
    totalTime: float,
    makespan: int,
    heuristicType: int,
    initialHeuristic: float,
    expandedNodes: int,
    solutionMoves: list[list[str]],
    solutionPoints: list[list[tuple[int,int]]],
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
            if len(solutionMoves[i])+1 != len(solutionPoints[i]):
                print(f"ERROR --- create_output_files() --- Unvalid solution list (diff list len)")


    # Create output filenames
    mapName = os.path.basename(filename).split(".")[0]
    testDirName = os.path.dirname(filename)
    outputFilename = f"{testDirName}/{mapName}_{heuristicType}.output"
    statFilename = f"{testDirName}/{mapName}_{heuristicType}.stat"

    # Create stat contents:
    statContents = f"Tiempo total: {totalTime}\nMakespan: {makespan}\nHeurística inicial: {initialHeuristic}\nNodos expandidos: {expandedNodes}"

    # Create output contents:
    outputContents =f""""""
    for i in range(len(solutionMoves)):
        line = f"{solutionPoints[i][0]} "
        for j in range(len(solutionMoves[i])):
            move = solutionMoves[i][j]
            point = solutionPoints[i][j+1]
            line += f"{move}{point} "

        outputContents += f"{line}\n"


    # Create files
    try:
        with open(OUTDIR + outputFilename, "w") as outputFile:
            outputFile.write(str(outputContents))
    except:
        print(f"ERROR --- create_output_files() --- Error creating output file")
        return False
    try:
        with open(OUTDIR + statFilename, "w") as statFile:
            statFile.write(statContents)
    except:
        print(f"ERROR --- create_output_files() --- Error creating stat file")
        return False

    return True


def main():
   
    filename = sys.argv[1]
    create_output_files(filename, 1.0, 1, 1, 1.0, 1, [["↓", "→"], ["←", "↑","w"]],[[(2,3),(2,3),(2,3)],[(2,3),(2,3),(2,3),(2,3)]])


if __name__ == "__main__":
    main()
