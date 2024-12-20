from parser import process_file


def algorithm_floydWarshall(map_data: dict[tuple[int, int], str]) -> dict[tuple[int, int], dict[tuple[int, int], float]]:
    """
    Compute the Floyd-Warshall algorithm with wall detection.
    Nodes are considered adjacent only if they are Manhattan distance 1 apart
    and at least one of them is not a wall ("G").
    
    Args:
        map_data (Dict[Tuple[int, int], str]): Dictionary mapping positions to their content
            where "G" represents a wall and any other character represents a passable space
            
    Returns:
        Dict[Tuple[int, int], Dict[Tuple[int, int], float]]: Dictionary mapping each position 
        to its minimum distances to all other positions
    """
    # Initialize the mapping from node indices to their positions
    n = 1
    nodes = {}  # Maps index to position
    reverse_nodes = {}  # Maps position to index
    for i in map_data.keys():
        nodes[n] = i
        reverse_nodes[i] = n
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
                    if map_data[pos_i] != "G" and map_data[pos_j] != "G":
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
    
    # Convert the result matrix to a dictionary
    result_dict = {}
    for i in range(1, num_nodes + 1):
        pos_i = nodes[i]
        # Create inner dictionary for each position
        distances_from_i = {}
        for j in range(1, num_nodes + 1):
            pos_j = nodes[j]
            distances_from_i[pos_j] = distanceArray[i-1][j-1]
        result_dict[pos_i] = distances_from_i


    return result_dict

_, positions, map = process_file("src/parte-2/ASTAR-tests/mapa05.csv")
print(algorithm_floydWarshall(map))

