# Import necessary functions and modules
from src.documentai_extract import (
    parse_from_pdf, extract_patterns, get_tables, process_form_data
)
from  src.document_info import  get_info
import sys
import os
from pathlib import Path
import json
from dotenv import load_dotenv



if __name__ == "__main__":
    # Load documentai credentials and Cloud project info from environment variables and a JSON file.
    load_dotenv()
    PROJECT_PATH = Path.cwd()
    PDF_FILE_PATH = PROJECT_PATH.joinpath(os.getenv("INPUT_FOLDER"))
    OUTPUT_DATA_PATH = PROJECT_PATH.joinpath(os.getenv("OUTPUT_FOLDER"))

    # Read the project ID from a JSON file
    with open(PROJECT_PATH.joinpath('key.json'), 'r') as f:
        json_file = json.load(f)
        PROJECT_ID = json_file.get('project_id')

    LOCATION = os.getenv("LOCATION")
    MIME_TYPE = os.getenv("MIME_TYPE")
    PROCESSOR_ID = os.getenv("PROCESSOR_ID")
    INPUT_PDF_FILE = PDF_FILE_PATH.joinpath(f'{sys.argv[2]}.pdf')
    PROCESSOR_VERSION = os.getenv("PROCESSOR_VERSION")

    # Determine the action based on the command line argument
    action = sys.argv[1]

    # Execute the appropriate action
    if action == 'parse':
        parse_from_pdf(
            INPUT_PDF_FILE,
            PROJECT_ID,
            PROCESSOR_ID,
            OUTPUT_DATA_PATH,
            LOCATION,
            MIME_TYPE
        )
        print(f'****** PARSED DOCUMENT ******\n\t{sys.argv[2]}')


    if action == 'process':
        if len(sys.argv) > 3 and sys.argv[3]:
            process_form_data(sys.argv[2], OUTPUT_DATA_PATH, sys.argv[3])
            
        else:
            process_form_data(sys.argv[2], OUTPUT_DATA_PATH, 0)
        print(f'****** GENERATED RESULTS ******\n\t{sys.argv[2]}')

    if action == 'document_info':
        get_info(INPUT_PDF_FILE, OUTPUT_DATA_PATH)
        print(f'****** EXTRACTED METADATA ******\n\t{sys.argv[2]}')


    if action == 'tables':
        get_tables(sys.argv[2], OUTPUT_DATA_PATH)
        print(f'****** EXTRACTED TABLES ******\n\t{sys.argv[2]}')


    if action == 'patterns':
        extract_patterns(sys.argv[2], OUTPUT_DATA_PATH)
        print(f'****** EXTRACTED PATTERNS ******\n\t{sys.argv[2]}')
