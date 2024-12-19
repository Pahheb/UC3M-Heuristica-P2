def cartesian_product_n(input_set,n):
    """
    Compute the Cartesian product of a set with itself n times.
    The set contains tuples of two integers.
    
    Args:
        input_set: Set of tuples, where each tuple contains two integers
        n: Number of times to compute the product
        
    Returns:
        List of all possible combinations as lists
        
    Example:
        >>> cartesian_product_n({(1,2), (3,4)}, 2)
        [[(1,2), (1,2)], [(1,2), (3,4)], [(3,4), (1,2)], [(3,4), (3,4)]]
    """
    if n <= 0:
        return [[]]
    
    # Convert set to sorted list for consistent ordering
    # For tuples, we sort based on both elements of the tuple
    elements = sorted(list(input_set), key=lambda x: (x[0], x[1]))
    set_size = len(elements)
    
    # Total number of combinations remains the same
    # If we have k tuples and select n times, we get k^n combinations
    total_combinations = set_size ** n
    
    # Initialize result list
    result = []
    
    # Generate each combination
    for i in range(total_combinations):
        # Current combination
        combination = []
        temp = i
        
        # The base conversion process remains the same
        # But now each selected element is a tuple instead of a number
        for _ in range(n):
            combination.append(elements[temp % set_size])
            temp //= set_size
         
        result.append(combination)
        
    return result

def print_combinations(combinations, n):
    """
    Pretty print the combinations with indices.
    Modified to handle tuples by showing both numbers in each position.
    
    Args:
        combinations: List of combinations to print
        n: Number of elements in each combination
    """
    # Print header with extra space for tuples
    header = "Index |"
    for i in range(n):
        header += f"   Pos{i}    |"
    print(header)
    print("-" * len(header))
    
    # Print combinations, formatting tuples nicely
    for i, combo in enumerate(combinations):
        line = f"{i:5d} |"
        for elem in combo:
            line += f" ({elem[0]},{elem[1]}) |"
        print(line)

# Example usage with detailed output
input_set = {(0,1), (1,0), (-1,0), (0,-1),(0,0)}
n = 30

print("Input set:", input_set)
print(f"Computing {n}-fold Cartesian product...\n")

combinations = cartesian_product_n(input_set,n)
print_combinations(combinations, n)
