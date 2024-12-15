import sys
import re 

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
                planePositions[i-1] = valuePair
            else:
                print(f"ERROR: {filename} -> Position formatting seems to be wrong")
        
        mapLine = 0
        for i in range(planeNumber + 1, len(lines)):
            pattern = r"[ABG]"
            notPattern = r"[^ABG;\n]"
            match = re.findall(pattern, lines[i])
            notMatch = re.findall(notPattern, lines[i])
            if notMatch:
                print(f"ERROR: {filename} -> Map formatting seems to be wrong")
            else:
                if match:
                    for i in range(len(match)):
                        map[(mapLine,i)] = match[i]
            mapLine=+1

        return planeNumber, planePositions, map

    except FileNotFoundError:
        print(f"ERROR: The file {filename} was not found")
        sys.exit(1)
    except ValueError:
        print(f"ERROR: THe file {filename} is not properly encoded")
        sys.exit(1)

def main():
    print(process_file(sys.argv[1]))

if __name__ == "__main__":
    main()
