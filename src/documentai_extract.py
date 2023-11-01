
import os
from pathlib import Path
import re
import json
from typing import List, Dict, Tuple
import pandas as pd
import spacy
from google.cloud import documentai_v1 as documentai
from google.api_core.client_options import ClientOptions

from . import form_regex as fr


def read_json(json_filename: str, OUTPUT_DATA_PATH) -> dict:
    """
    Read and load a JSON file from the specified path.
    """
    JSON_PATH = OUTPUT_DATA_PATH.joinpath(f'{json_filename}.json')
    with open(JSON_PATH, 'r', encoding='utf-8') as t:
        doc = json.load(t)
    return doc


def parse_from_pdf(pdf_file_path, PROJECT_ID, PROCESSOR_ID, OUTPUT_DATA_PATH, LOCATION, MIME_TYPE) -> json:
    """
    Parse a PDF document using Google Document AI and save the results as a JSON file.
    general parser  cdf0d0066d96355 or 
    form parser  330d9636fe52f1db
    """

    client = documentai.DocumentProcessorServiceClient(
        client_options=ClientOptions(api_endpoint=f'{LOCATION}-documentai.googleapis.com')
    )

    RESOURCE_NAME = client.processor_path(PROJECT_ID, LOCATION, PROCESSOR_ID)

    with open(pdf_file_path, "rb") as image:
        image_content = image.read()

    raw_document = documentai.RawDocument(content=image_content, mime_type=MIME_TYPE)
    request = documentai.ProcessRequest(name=RESOURCE_NAME, raw_document=raw_document)
    result = client.process_document(request=request)
    
    document_object = result.document
    print("Document processing complete.")

    json_string = type(result).to_json(result)

    output_document_dict = OUTPUT_DATA_PATH.joinpath(f"{pdf_file_path.stem}.json")
    with open(output_document_dict, "w", encoding="utf-8") as json_file:
        json_file.write(json_string)

    return json_file
        

def get_field_value(json_file, confidence_threshold = 0) -> List[Tuple]:
    "Extracting a list of (Fields and Values, Confidence) from the JSON file"

    extracted_form_fields = []
    pages = json_file['document']['pages']
    for page in pages:
        form_fields = page.get('formFields', [])
        
        for form_field in form_fields:
            field = form_field.get('fieldName', {}).get('textAnchor', {}).get('content', '').strip()
            value = form_field.get('fieldValue', {}).get('textAnchor', {}).get('content', '').strip()
            confidence = form_field.get('fieldName', {}).get('confidence', {})
            if confidence > float(confidence_threshold):
                extracted_form_fields.append( (field, value, confidence))
    return extracted_form_fields

def extract_entity_types(json_file: json) -> List[Dict]:
    """
    Extract and return a list of identified entity types 
    with their respective confidence from the JSON data.
    """
    entity_types = []
    for entity in json_file['document']['entities']:
        for property in entity['properties']:
            entity_type = property['type']
            mention_text = property['mentionText']
            confidence = property['confidence']
            entity_types.append({
                'entityType': entity_type,
                'mentionText': mention_text,
                'confidence': confidence
            })
    return entity_types



def process_form_data(json_name, OUTPUT_DATA_PATH, confidence_threshold ) -> pd.DataFrame:
    """
    Reading a JSON file and saving a spreadsheet of the field and values extracted as well as all
    the identified entities with their respective confidence according to the OCR parsing.
    """
    # Reading JSON file
    json_file = read_json(json_name, OUTPUT_DATA_PATH)

    entity_types = extract_entity_types(json_file) 
    extracted_data = get_field_value(json_file, confidence_threshold)
    field_value_df = pd.DataFrame(extracted_data, columns=['Field', 'value', 'confidence'])

    field_value_df['data_type'] = None
    field_value_df['data_type_confidence'] = None

    for index, row in field_value_df.iterrows():
        field_text = str(row['Field']).lower()
        value_text = str(row['value'])
        max_confidence =[]

        for ent in entity_types:
            entity_type = ent['entityType']
            entity_text = ent['mentionText']
        
            # Check if the entity type is in 'Field' or 'value' (case-insensitive)
            if (entity_text in field_text or entity_text in value_text) and entity_type != 'page_number' :
                max_confidence.append(ent)
        try:
            if max_confidence:
                max_entity = max(max_confidence, key=lambda x: x['confidence'])
                field_value_df.at[index, 'data_type'] = max_entity['entityType']
                field_value_df.at[index, 'data_type_confidence'] = max_entity['confidence']
        except ValueError:
            pass
    
    excel_file = os.path.join(OUTPUT_DATA_PATH, f'{json_name}_results.xlsx')
    field_value_df.to_excel(excel_file, sheet_name='results', index=False, na_rep='None')
    return field_value_df



def get_tables(json_name, OUTPUT_DATA_PATH ):
    """Extracting tables from the all the pages in the document"""
    
    # Reading JSON file
    json_file = read_json(json_name, OUTPUT_DATA_PATH)

    document = json_file['document']
    text = document['text']
    print(f"There are {len(document['pages'])} page(s) in this document.")
    excel_file_path = os.path.join(OUTPUT_DATA_PATH, f'{json_name}_tables.xlsx')
    excel_file = pd.ExcelWriter(excel_file_path, engine='openpyxl')

    # Read the form fields and tables output from the processor
    for page in document['pages']:
        print(f"\n**** Page {page['pageNumber']} ****")

        print(f"\nFound {len(page['tables'])} table(s):")

        for idx, table in enumerate(page['tables']):
            num_columns = len(table['headerRows'][0]['cells'])
            num_rows = len(table['bodyRows'])
            print(f"Table with {num_columns} columns and {num_rows} rows:")

            # Create a DataFrame for the table
            table_data = []
            table_data.append([layout_to_text(cell['layout'], text) 
                               for cell in table['headerRows'][0]['cells']]
            )
            table_data.extend([layout_to_text(cell['layout'], text) 
                               for cell in row['cells']] for row in table['bodyRows']
            )
            table_df = pd.DataFrame(table_data)

            # Save the table as an Excel file
            sheet_name = str(idx+1)
            table_df.to_excel(excel_file, sheet_name=sheet_name, startrow=0 , header=False, index=False)
        
        # Save the Excel file
    excel_file.save()

    return None

def layout_to_text(layout: documentai.Document.Page.Layout, text: str) -> str:
    """
    Document AI identifies text in different parts of the document by their
    offsets in the entirety of the document"s text. This function converts
    offsets to a string.
    """
    # If a text segment spans several lines, it will
    # be stored in different text segments.
    return "".join(
        text[int(segment['startIndex']) : int(segment['endIndex'])]
        for segment in layout['textAnchor']['textSegments']
    )



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

def extract_patterns(text_file, OUTPUT_DATA_PATH):
    """
    Extract patterns and data based on specified field labels and variations.
    """
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
    
    output_info = OUTPUT_DATA_PATH.joinpath(f"{text_file}_patterns.txt")
    with open(output_info, "w", encoding= 'utf-8-sig') as doc:
        doc.write(str(info))

