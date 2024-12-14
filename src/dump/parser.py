import sys
import re 

def process_file():
    # Get data file
    filename = sys.argv[1]
    # Read the file
    try:
        with open(filename, 'r') as file:
            lines = file.readlines()

        planeNumber = int(lines[0])

        planePositions = []
        for i in range(1,planeNumber+1):
            # Get the (X,X) (X,X) format as 
            #two pairs of values in the list using regex
            pattern = r"\((\d+),(\d+)\)\s+\((\d+),(\d+)\)"
            match = re.search(pattern, lines[i])

            if match:
                # Extracted values
                valuePair =[\
                            (int(match.group(1)), int(match.group(2))),\
                            (int(match.group(3)), int(match.group(4)))\
                            ]
                # Add the values to the list
                planePositions.append(valuePair)
            else:
                print(f"ERROR: {filename} -> Position formatting seems to be wrong")

        map = []
        for i in range(planeNumber+1,len(lines)):
            pattern =  r"[ABG]"
            notPattern= r"[^ABG;\n]"
            match = re.findall(pattern,lines[i])
            notMatch = re.findall(notPattern,lines[i])
            if notMatch:
                print(f"ERROR: {filename} -> Map formatting seems to be wrong")
            else: 
                if match:
                    map.append(match)

        print(planeNumber)
        print(planePositions)
        print(map)

    except FileNotFoundError:
        print(f"ERROR: The file {filename} was not found")
        sys.exit(1)
    except ValueError:
        print(f"ERROR: THe file {filename} is not properly encoded")

process_file()
