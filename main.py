# Import necessary functions and modules
from src.documentai_extract import (
    parse_from_pdf, extract_patterns, get_tables, get_field_value
)
from  src.document_info import  get_info
import sys
import os
from pathlib import Path
import json
from dotenv import load_dotenv

if __name__ == "__main":
    print("Entering __main__ block...")
    # Load documentai credentials and Cloud project info from environment variables and a JSON file.
    load_dotenv()
    PROJECT_PATH = Path.cwd()
    INPUT_DATA_PATH = PROJECT_PATH.joinpath(os.getenv("INPUT_FOLDER"))
    OUTPUT_DATA_PATH = PROJECT_PATH.joinpath(os.getenv("OUTPUT_FOLDER"))

    # Read the project ID from a JSON file
    with open(PROJECT_PATH.joinpath('key.json'), 'r') as f:
        json_file = json.load(f)
        PROJECT_ID = json_file.get('project_id')

    LOCATION = os.getenv("LOCATION")
    MIME_TYPE = os.getenv("MIME_TYPE")
    PROCESSOR_ID = os.getenv("PROCESSOR_ID")
    INPUT_PDF_FILE = INPUT_DATA_PATH.joinpath(f'{sys.argv[2]}.pdf')
    PROCESSOR_VERSION = os.getenv("PROCESSOR_VERSION")

    # Determine the action based on the command line argument
    action = sys.argv[1]

    # Execute the appropriate action
    if action == 'parse':
        print("parsing_PDF")
        parse_from_pdf(
            INPUT_PDF_FILE,
            PROJECT_ID,
            PROCESSOR_ID,
            OUTPUT_DATA_PATH,
            LOCATION,
            MIME_TYPE
        )
        print(f"Parsed text from PDF:\t {sys.argv[2]}")



    if action == 'document_info':
        get_info(INPUT_PDF_FILE, OUTPUT_DATA_PATH)


    if action == 'tables':
        get_tables(sys.argv[2], OUTPUT_DATA_PATH)
        print(f'-------EXTRACTED TABLES---------\n\t{sys.argv[2]}')

    if action == 'fieldvalue':
        get_field_value(sys.argv[2], OUTPUT_DATA_PATH)
        print(f'-------EXTRACTED Fields and Values---------\n\t{sys.argv[2]}')

    if action == 'extract':
        extract_patterns(sys.argv[2], OUTPUT_DATA_PATH)
        print(f'-------EXTRACTED PATTERNS---------\n\t{sys.argv[2]}')
