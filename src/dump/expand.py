def find_swapped_positions(list1, list2):
    """
    Find positions where values have been swapped between two lists.
    Returns a list of tuples containing pairs of positions where values were swapped.
    """
    # First, check if list2 is shorter than list1
    if len(list2) < len(list1):
        print(f"Error: List2 is shorter than List1. Missing values after position {len(list2)-1}")
        return []
    
    # Find positions where values differ
    different_positions = []
    for i in range(len(list1)):
        if i >= len(list2):
            break
        if list1[i] != list2[i]:
            different_positions.append(i)
    
    # Look for swaps among the different positions
    swaps = []
    for i in range(len(different_positions)):
        pos1 = different_positions[i]
        val1_in_list1 = list1[pos1]
        
        # Look for this value in list2 at other different positions
        for j in range(i + 1, len(different_positions)):
            pos2 = different_positions[j]
            val2_in_list1 = list1[pos2]
            
            # Check if values were swapped
            if (list2[pos1] == val2_in_list1 and 
                list2[pos2] == val1_in_list1):
                swaps.append((pos1, pos2))
                
    return swaps

# Function to print results in a friendly way
def print_swaps_analysis(list1, list2):
    swaps = find_swapped_positions(list1, list2)
    
    print(f"List 1: {list1}")
    print(f"List 2: {list2}")
    
    if not swaps:
        if len(list2) < len(list1):
            return
        if list1 == list2:
            print("The lists are identical.")
        else:
            print("Found differences, but no swapped values detected.")
    else:
        print("\nFound the following swaps:")
        for pos1, pos2 in swaps:
            print(f"Values swapped between positions {pos1} and {pos2}:")
            print(f"  Position {pos1}: {list1[pos1]} ↔ {list2[pos1]}")
            print(f"  Position {pos2}: {list1[pos2]} ↔ {list2[pos2]}")

# Example usage
if __name__ == "__main__":
    # Example 1: Simple swap
    list1 = [1, 2, 3, 4, 5]
    list2 = [2, 1, 3, 4, 5]
    print("Example 1:")
    print_swaps_analysis(list1, list2)
    
    print("\nExample 2:")
    # Example 2: Multiple swaps
    list3 = [1, 2, 3, 4, 5, 6]
    list4 = [2, 1, 5, 4, 3, 6]
    print_swaps_analysis(list3, list4)
