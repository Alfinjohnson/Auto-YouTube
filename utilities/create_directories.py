import os
import logging
from const import EXISTING_TOPICS, OUTPUT_AUDIO, YT_SECRET_FILE, OUTPUT_FINAL_VIDEO, OUTPUT_FINAL_INFO, LOG_PATH, \
    OUTPUT_TMP, OUTPUT_TRANSCRIPT, CREATE_DIRECTORY_IF_NOT_EXIST

# Configure logging
logging.basicConfig(filename=LOG_PATH, level=logging.INFO, format='%(asctime)s - %(levelname)s: %(message)s')


def create_directories():
    create_if_not = CREATE_DIRECTORY_IF_NOT_EXIST

    if create_if_not is True:
        # Ensure that the required directories exist, if not, create them
        directories = [EXISTING_TOPICS, OUTPUT_AUDIO, YT_SECRET_FILE, OUTPUT_FINAL_VIDEO, OUTPUT_FINAL_INFO, LOG_PATH,
                       OUTPUT_TMP, EXISTING_TOPICS, OUTPUT_TRANSCRIPT]
        for directory in directories:
            if not os.path.exists(directory):
                os.makedirs(directory)
                logging.info(f"Created directory: {directory}")
            else:  logging.info(f"directory exists: {directory}")
    else:
        logging.info("Directory creation skipped as per configuration.")


# Call the function to create directories
create_directories()
