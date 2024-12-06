"""
This file contains all the function related with file management, processing and more
"""

import logging
logger = logging.getLogger(__name__)

def process_initial_file(route: str):
    f  = open(route, "r")
    logger.info("Initial file given:\n\n%s", f.read())
