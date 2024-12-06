from utils.file_processor import process_initial_file

import sys
import logging
logger = logging.getLogger(__name__)


def main():
    logging.basicConfig(level=logging.INFO)
    routeToInitFile = sys.argv[1]
    process_initial_file(route=routeToInitFile) 

if __name__ == '__main__':
    main()