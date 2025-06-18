"""
Logger setup for S3Commander
"""

import logging
import os

def setup_logging(log_file: str = "s3commander.log"):
    log_level = os.environ.get("S3COMMANDER_LOGLEVEL", "INFO").upper()
    logging.basicConfig(
        level=log_level,
        format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
        handlers=[
            logging.FileHandler(log_file),
            logging.StreamHandler()
        ]
    )
    return logging.getLogger("S3Commander") 