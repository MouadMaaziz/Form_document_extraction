
import os
from pathlib import Path
import re

import pandas as pd

from google.cloud import documentai_v1 as documentai
from google.api_core.client_options import ClientOptions

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

    # Store the extracted text into a .txt file
    output_text_file = OUTPUT_DATA_PATH.joinpath(f"{INPUT_PDF_FILE.stem}.txt")
    with open(output_text_file, "w", encoding="utf-8") as text_file:
        text_file.write(document_object.text)



def locate_fields(fields:dict, text_lines:list):
    """Search the position field labels throughout the document"""
    field_index = {}
    for field, field_variations in fields.items():
        field_index[field] = []
        for variation in field_variations:
            field_index[field].extend(text_lines.index(line) for line in text_lines if variation in line)
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