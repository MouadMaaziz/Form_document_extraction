from src.documentai_extract import parse_text_from_document, extract_info
import sys
import os
from pathlib import Path
import json
from dotenv import load_dotenv

if __name__ == "__main__":

    
    load_dotenv()
    PROJECT_PATH = Path.cwd()
    INPUT_DATA_PATH = PROJECT_PATH.joinpath(os.getenv("INPUT_FOLDER"))
    OUTPUT_DATA_PATH = PROJECT_PATH.joinpath(os.getenv("OUTPUT_FOLDER"))

    

    if sys.argv[1] == 'parse':
        # Loading the documentai credentials and Cloud project info form .env and json file.
        LOCATION = os.getenv("LOCATION")
        MIME_TYPE = os.getenv("MIME_TYPE")
        PROCESSOR_ID = os.getenv("PROCESSOR_ID")
        INPUT_PDF_FILE = INPUT_DATA_PATH.joinpath(INPUT_DATA_PATH, f'{sys.argv[2]}.pdf') 

        with open(PROJECT_PATH.joinpath('key.json'), 'r') as f:
            json_file = json.load(f)
            PROJECT_ID = json_file.get('project_id')


        parsed_text = parse_text_from_document(INPUT_PDF_FILE,
                                                PROJECT_ID,
                                                PROCESSOR_ID,
                                                OUTPUT_DATA_PATH,
                                                LOCATION,
                                                MIME_TYPE
                                               )
        print("Parsed text from PDF:")





    if sys.argv[1] == 'extract':
        extracted_info = extract_info(sys.argv[2], OUTPUT_DATA_PATH)
        print(f'-------EXTRACTED INFO---------\n\t{sys.argv[2]}')

    
    
    