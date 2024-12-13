import sys

def main():
    # Ensure proper usage
    if len(sys.argv) != 3:
        print("Usage: python sum.py <filename> <operation>")
        print("<operation>: 1 for sum, 2 for multiplication")
        sys.exit(1)

    # Retrieve the arguments
    filename = sys.argv[1]
    try:
        operation = int(sys.argv[2])
        if operation not in [1, 2]:
            raise ValueError
    except ValueError:
        print("Error: <operation> must be 1 for sum or 2 for multiplication")
        sys.exit(1)

    try:
        # Read the file
        with open(filename, 'r') as file:
            lines = file.readlines()

        # Ensure the file has exactly two lines
        if len(lines) != 2:
            print("Error: The file must contain exactly two lines, each with a number.")
            sys.exit(1)

        # Convert lines to numbers
        num1 = float(lines[0].strip())
        num2 = float(lines[1].strip())

        # Perform the operation
        if operation == 1:
            result = num1 + num2
            print(f"The sum is: {result}")
        elif operation == 2:
            result = num1 * num2
            print(f"The product is: {result}")

    except FileNotFoundError:
        print(f"Error: The file '{filename}' was not found.")
        sys.exit(1)
    except ValueError:
        print("Error: The file must contain valid numbers on each line.")
        sys.exit(1)

if __name__ == "__main__":
    main()

