from src.documentai_extract import parse_from_pdf, extract_info, get_tables, get_field_value
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

    with open(PROJECT_PATH.joinpath('key.json'), 'r') as f:
            json_file = json.load(f)
            PROJECT_ID = json_file.get('project_id')

    LOCATION = os.getenv("LOCATION")
    MIME_TYPE = os.getenv("MIME_TYPE")
    PROCESSOR_ID = os.getenv("PROCESSOR_ID")
    INPUT_PDF_FILE = INPUT_DATA_PATH.joinpath(INPUT_DATA_PATH, f'{sys.argv[2]}.pdf')
    PROCESSOR_VERSION = 'rc'



    if sys.argv[1] == 'parse':
        """ Loading the documentai credentials and Cloud project info form .env and json file.
        #general parser  cdf0d0066d96355 or form parser  330d9636fe52f1db
        """
        parse_from_pdf(INPUT_PDF_FILE,
                                    PROJECT_ID,
                                    PROCESSOR_ID,
                                    OUTPUT_DATA_PATH,
                                    LOCATION,
                                    MIME_TYPE,
                                    
        )
        print(f"Parsed text from PDF:\t {sys.argv[2]}")


    if sys.argv[1] == 'extract':
        extracted_info = extract_info(sys.argv[2], OUTPUT_DATA_PATH)
        print(f'-------EXTRACTED INFO---------\n\t{sys.argv[2]}')


    if sys.argv[1] == 'tables':
        
        get_tables(sys.argv[2],
                    OUTPUT_DATA_PATH
        )

        print(f'-------EXTRACTED TABLES---------\n\t{sys.argv[2]}')


    if sys.argv[1] == 'fieldvalue':
        
        get_field_value(sys.argv[2],
                    OUTPUT_DATA_PATH
        )

        print(f'-------EXTRACTED Fields and Values---------\n\t{sys.argv[2]}')