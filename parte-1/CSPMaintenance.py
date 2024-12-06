from utils.file_processor import process_initial_file
from utils.Map import Map


import sys
import logging
logger = logging.getLogger(__name__)


def main():
    logging.basicConfig(level=logging.INFO)
    routeToInitFile = sys.argv[1]
    data = process_initial_file(route=routeToInitFile)
    print(f"Data has been processed:\n%s\n{data}")

if __name__ == '__main__':
    main()