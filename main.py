from src.documentai_extract import parse_text_from_document, extract_info
import sys
import os
from pathlib import Path
import json
from dotenv import load_dotenv

if __name__ == "__main__":

    
    
    PROJECT_PATH = Path.cwd()
    INPUT_DATA_PATH = PROJECT_PATH.joinpath('data')
    OUTPUT_DATA_PATH = PROJECT_PATH.joinpath('output')

    


    if sys.argv[1] == 'parse':
        # Loading the documentai credentials and Cloud project info form .env and json file.
        load_dotenv()
        PROCESSOR_ID = os.getenv("PROCESSOR_ID") 

        with open(PROJECT_PATH.joinpath('key.json'), 'r') as f:
            json_file = json.load(f)
            PROJECT_ID = json_file.get('project_id')


        parsed_text = parse_text_from_document(sys.argv[2], PROJECT_ID,PROCESSOR_ID, INPUT_DATA_PATH, OUTPUT_DATA_PATH)
        print("Parsed text from PDF:")





    if sys.argv[1] == 'extract':
        extracted_info = extract_info(sys.argv[2], OUTPUT_DATA_PATH)
        print(f'-------EXTRACTED INFO---------\n\t{sys.argv[2]}')

    
    
    