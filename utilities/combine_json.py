import os
import json
import logging

from main.utilities.const import OUTPUT_FINAL_INFO, LOG_PATH


class Logger:
    def __init__(self, log_file):
        self.log_file = log_file
        logging.basicConfig(filename=self.log_file, level=logging.INFO)

    def log_info(self, message):
        logging.info(message)

    def log_error(self, message):
        logging.error(message)


def combine_json_files(directory, output_file, log_file):
    logger = Logger(log_file)
    logger.log_info("Starting JSON file combination.")

    combined_data = []

    try:
        for filename in os.listdir(directory):
            if filename.endswith('.json'):
                file_path = os.path.join(directory, filename)

                try:
                    with open(file_path, 'r') as file:
                        json_data = json.load(file)
                        combined_data.append(json_data)
                except Exception as e:
                    error_message = f"Error loading JSON file '{file_path}': {str(e)}"
                    logger.log_error(error_message)

        with open(output_file, 'w') as outfile:
            json.dump(combined_data, outfile)
            logger.log_info(f"Combined JSON data written to '{output_file}'.")

    except Exception as e:
        error_message = f"Error combining JSON files: {str(e)}"
        logger.log_error(error_message)

    logger.log_info("JSON file combination complete.")


# Example usage:
combine_json_files(OUTPUT_FINAL_INFO, OUTPUT_FINAL_INFO + 'combined.json', LOG_PATH)
