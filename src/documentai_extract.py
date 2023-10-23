
import os
from pathlib import Path
import json
import re

import pandas as pd

from google.cloud import documentai_v1 as documentai
from google.api_core.client_options import ClientOptions

import spacy
import en_core_web_trf

from . import form_regex as fr

  


# Load the english NLP model
#nlp = spacy.load("en_core_web_sm")
nlp = spacy.load('en_core_web_trf')







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

    # Store the extracted text into a .txt file
    output_text_file = OUTPUT_DATA_PATH.joinpath(f"{INPUT_PDF_FILE.stem}.txt")
    with open(output_text_file, "w", encoding="utf-8") as text_file:
        text_file.write(document_object.text)


def extract_info(text_file, OUTPUT_DATA_PATH):

    TEXT_PATH = OUTPUT_DATA_PATH.joinpath(f'{text_file}.txt')
    
    text_lines = []
    with open(TEXT_PATH, 'r') as f: 
        for line in f:
            text_lines.append(line.strip())

    
    # for l in raw_text.split('\n'):
    #     doc = nlp(l)
    #     print([token.text for token in doc])
    

    # Define fields and their variations to look for in the text
    fields = {
        'full_name': ['Name', 'name', 'First', 'Last'],
        'sex': ['sex', 'Sex', 'gender', 'Gender'],
        'date_of_birth': ['Birth','birth', 'DOB'],
        'dates': ['Date','date', 'day'],
        'phone': ['Phone', 'Telephone', 'Contact', 'Cell'],
        'email': ['Email','Electronic mail', 'e-mail','email', 'E-mail'],
        'address': ['Address', 'address','residence', 'street address', ' mail'],
        'street_address': ['Address', 'address','residence', 'street address', ' mail'],
        'ssn': ['Social','security', 'number', 'SSN', 'ssn'],
        'driver_license': [ 'Driver','License', 'DL', 'driver' ],
        'marital_status': ['Marital status','Status'],
        'price': ['price','Price', 'total','Total', '$', 'USD', 'US Dollar', 'Amount','amount', 'AMOUNT']
     }
    
    # These are fields that have a strong matching pattern (they don't have to be close to the field name)
    strong_fields = ['phone','ssn','email','address','date_of_birth', 'dates','street_address', 'price']

    # Looking for entrypoints for each field by keywords
    field_index = {}
    for field, fieldname in fields.items():
        field_index[field] = []
        for variation in fieldname:
            field_index[field].extend(text_lines.index(line) for line in text_lines if variation in line)

    info = {}
    for fd,indexes in field_index.items():
        if indexes:
            # look for the pattern from text_lines[index-2] to text_lines[index + 2]
            info[fd]=[]
            for i in indexes:
                for line in text_lines:
                    if abs(text_lines.index(line) - i) <= 3  and re.match(fr.patterns[fd], line) and not line in info[fd]:
                        info[fd].append(line)
                    elif abs(text_lines.index(line) - i) <= 20  and re.findall(fr.patterns[fd], line) and not line in info[fd] and fd in strong_fields :
                        info[fd] += re.findall(fr.patterns[fd], line)
                    else:
                        continue
    
    output_info = OUTPUT_DATA_PATH.joinpath(f"{text_file}_info.txt")
    with open(output_info, "w", encoding= 'utf-8-sig') as doc:
        doc.write(str(info))