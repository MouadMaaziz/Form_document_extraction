
import os
from pathlib import Path
import re
import json
import sys

import pandas as pd

from google.cloud import documentai_v1 as documentai
from google.api_core.client_options import ClientOptions
import proto


import spacy
import en_core_web_trf

from . import form_regex as fr



#nlp = spacy.load("en_core_web_sm")




def parse_text_from_document(INPUT_PDF_FILE, PROJECT_ID, PROCESSOR_ID, OUTPUT_DATA_PATH, LOCATION, MIME_TYPE):
    """Extracting text from pdf files using google's OCR."""

    client = documentai.DocumentProcessorServiceClient(
        client_options=ClientOptions(api_endpoint=f'{LOCATION}-documentai.googleapis.com')
    )

    RESOURCE_NAME = client.processor_path(PROJECT_ID, LOCATION, PROCESSOR_ID)

    with open(INPUT_PDF_FILE, "rb") as image:
        image_content = image.read()

    raw_document = documentai.RawDocument(content=image_content, mime_type=MIME_TYPE)

    request = documentai.ProcessRequest(name=RESOURCE_NAME, raw_document=raw_document)
   
    result = client.process_document(request=request)
    

    document_object = result.document
    print("Document processing complete.")

    json_string = type(result).to_json(result)

    # Store the extracted text into a .txt file
    output_text_file = OUTPUT_DATA_PATH.joinpath(f"{INPUT_PDF_FILE.stem}.txt")
    with open(output_text_file, "w", encoding="utf-8") as text_file:
        text_file.write(document_object.text)

    output_document_dict = OUTPUT_DATA_PATH.joinpath(f"{INPUT_PDF_FILE.stem}.json")
    with open(output_document_dict, "w", encoding="utf-8") as json_file:
        json_file.write(json_string)
        


def locate_fields(fields:dict, text_lines:list):
    """Search the position field labels throughout the document"""
    field_index = {}
    for field, field_variations in fields.items():
        field_indices = []
        for index, text_line in enumerate(text_lines):
            for variation in field_variations:
                if variation in text_line:
                    field_indices.append(index)
                    break
        field_index[field]=field_indices
    return field_index


def extract_info(text_file, OUTPUT_DATA_PATH):


    # Load the english NLP model
    nlp = spacy.load('en_core_web_trf')

    TEXT_PATH = OUTPUT_DATA_PATH.joinpath(f'{text_file}.txt')
    with open(TEXT_PATH, 'r') as f:
        text_lines = [line.strip() for line in f] 


    # Get field positions {field:[occurences]}
    field_index = locate_fields(fr.fields, text_lines)

    info = {}
    for fd,indexes in field_index.items():
        info[fd]=[]
        if indexes:
            # making an exception for full names, we use NLP to extract those.
            if fd =='full_name':
                for line_pos,line in enumerate(text_lines):
                    doc = nlp(line)
                    for ent in doc.ents:
                        if ent.label_ == 'PERSON' and re.match(fr.patterns[fd], ent.text) and not ent.text in info[fd] :
                            info[fd].append(ent)
        
            else:
                for i in indexes:
                    for line_pos,line in enumerate(text_lines):
                        if abs(line_pos - i) <= 3  and re.match(fr.patterns[fd], line) and not line in info[fd]:
                            info[fd].append(line)
                        elif abs(line_pos - i) <= 20  and re.findall(fr.patterns[fd], line) and not line in info[fd] and fd in fr.strong_fields :
                            info[fd] += re.findall(fr.patterns[fd], line)
                        else:
                            continue
    
    output_info = OUTPUT_DATA_PATH.joinpath(f"{text_file}_info.txt")
    with open(output_info, "w", encoding= 'utf-8-sig') as doc:
        doc.write(str(info))










from typing import Optional, Sequence
from dotenv import load_dotenv
from google.api_core.client_options import ClientOptions
from google.cloud import documentai
load_dotenv()
PROJECT_PATH = Path.cwd()
INPUT_DATA_PATH = PROJECT_PATH.joinpath(os.getenv("INPUT_FOLDER"))
OUTPUT_DATA_PATH = PROJECT_PATH.joinpath(os.getenv("OUTPUT_FOLDER"))

INPUT_PDF_FILE = INPUT_DATA_PATH.joinpath(INPUT_DATA_PATH, f'{sys.argv[2]}.pdf')
with open(PROJECT_PATH.joinpath('key.json'), 'r') as f:
            json_file = json.load(f)
            PROJECT_ID = json_file.get('project_id')

def process_document_form_sample(
    project_id=  PROJECT_ID,
    location=  os.getenv("LOCATION"),
    processor_id=  os.getenv("PROCESSOR_ID"),
    processor_version= 'rc',
    file_path=  INPUT_PDF_FILE,
    mime_type= os.getenv( "MIME_TYPE"),
    output_folder = OUTPUT_DATA_PATH,
) -> documentai.Document:
    # Online processing request to Document AI
    document = process_document(
        project_id, location, processor_id, processor_version, file_path, mime_type
    )


    text = document.text
    print(f"Full document text: {repr(text)}\n")
    print(f"There are {len(document.pages)} page(s) in this document.")

    # Read the form fields and tables output from the processor
    for page in document.pages:
        print(f"\n\n**** Page {page.page_number} ****")

        print(f"\nFound {len(page.tables)} table(s):")
        for idx, table in enumerate(page.tables):
            num_columns = len(table.header_rows[0].cells)
            num_rows = len(table.body_rows)
            print(f"Table with {num_columns} columns and {num_rows} rows:")

            # Print header rows
            print("Columns:")
            print_table_rows(table.header_rows, text)
            # Print body rows
            print("Table body data:")
            print_table_rows(table.body_rows, text)
            # Create a DataFrame for the table
            table_data = []
            table_data.append([layout_to_text(cell.layout, text) for cell in table.header_rows[0].cells])
            table_data.extend([layout_to_text(cell.layout, text) for cell in row.cells] for row in table.body_rows)
            table_df = pd.DataFrame(table_data)

            # Save the table as an Excel file
            table_excel_file = os.path.join(output_folder, f'table_{idx + 1}.xlsx')
            table_df.to_excel(table_excel_file, index=False)
        

    return document


def print_table_rows(
    table_rows: Sequence[documentai.Document.Page.Table.TableRow], text: str
) -> None:
    for table_row in table_rows:
        row_text = ""
        for cell in table_row.cells:
            cell_text = layout_to_text(cell.layout, text)
            row_text += f"{repr(cell_text.strip())} | "
        print(row_text)

def process_document(
    project_id=  os.getenv("PROJECT_ID"),
    location=  os.getenv("LOCATION"),
    processor_id=  os.getenv("PROCESSOR_ID"),
    processor_version= 'rc',
    file_path=  INPUT_PDF_FILE,
    mime_type= os.getenv( "MIME_TYPE"),
    process_options: Optional[documentai.ProcessOptions] = None,
) -> documentai.Document:
    
    client = documentai.DocumentProcessorServiceClient(
        client_options=ClientOptions(
            api_endpoint=f"{location}-documentai.googleapis.com"
        )
    )

    
    name = client.processor_version_path(
        project_id, location, processor_id, processor_version
    )

    # Read the file into memory
    with open(str(file_path), "rb") as image:
        image_content = image.read()

    # Configure the process request
    request = documentai.ProcessRequest(
        name=name,
        raw_document=documentai.RawDocument(content=image_content, mime_type=mime_type),
        # Only supported for Document OCR processor
        process_options=process_options,
    )

    result = client.process_document(request=request)

    return result.document


def layout_to_text(layout: documentai.Document.Page.Layout, text: str) -> str:
    """
    Document AI identifies text in different parts of the document by their
    offsets in the entirety of the document"s text. This function converts
    offsets to a string.
    """
    # If a text segment spans several lines, it will
    # be stored in different text segments.
    return "".join(
        text[int(segment.start_index) : int(segment.end_index)]
        for segment in layout.text_anchor.text_segments
    )


process_document_form_sample()