import logging
import os
from datetime import datetime


def configure_logger():
    # Create logger
    logger = logging.getLogger(__name__)

    # Set logging level
    logger.setLevel(logging.DEBUG)
    # Create logs directory if it doesn't exist
    logs_dir = 'logs'
    os.makedirs(logs_dir, exist_ok=True)

    # Create log file with current date
    log_file_name = f"{logs_dir}/web_app_{datetime.now().strftime('%Y-%m-%d')}.log"

    # Create file handler
    file_handler = logging.FileHandler(log_file_name)

    # Set formatter
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(filename)s - %(funcName)s  - %(message)s')
    file_handler.setFormatter(formatter)

    # Add file handler to logger
    logger.addHandler(file_handler)

    return logger
