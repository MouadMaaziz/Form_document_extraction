# Import necessary functions and modules
from src.documentai_extract import (
    parse_from_pdf, extract_patterns, get_tables, process_form_data
)
from src.document_info import get_info
import sys
import os
from pathlib import Path
import json
from dotenv import load_dotenv
from flask import Flask, request, jsonify, send_file, render_template
from werkzeug.utils import secure_filename


app = Flask(__name__, template_folder='./templates')

# Load documentai credentials and Cloud project info from environment variables and a JSON file
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
PROCESSOR_VERSION = os.getenv("PROCESSOR_VERSION")


UPLOAD_FOLDER = PDF_FILE_PATH
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/')
def home():
    return render_template('upload.html')  # Render the HTML template

@app.route('/process_pdf', methods=['POST'])
def process_pdf():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'})

    file = request.files['file']
    selected_function = request.form.get('function')

    if file.filename == '':
        return jsonify({'error': 'No selected file'})

    if not file.filename.endswith('.pdf'):
        return jsonify({'error': 'Invalid file format'})

    # Secure the file name
    filename = secure_filename(file.filename)

    # Save the uploaded file
    input_pdf_path = PDF_FILE_PATH.joinpath(filename)
    file.save(input_pdf_path)

    # Determine the action based on the selected function
    if selected_function == 'process':
        json_name = parse_from_pdf(
            input_pdf_path,
            PROJECT_ID,
            PROCESSOR_ID,
            OUTPUT_DATA_PATH,
            LOCATION,
            MIME_TYPE
        )
        
        confidence = float(request.form.get('confidence', 0))        
        processed_pdf = process_form_data(json_name, OUTPUT_DATA_PATH, confidence)
        return send_file(processed_pdf, as_attachment=True)

    elif selected_function == 'document_info':
        processed_pdf = get_info(input_pdf_path , OUTPUT_DATA_PATH)
        
        return send_file(processed_pdf, as_attachment=True)

    elif selected_function == 'tables':
        json_name = parse_from_pdf(
            input_pdf_path,
            PROJECT_ID,
            PROCESSOR_ID,
            OUTPUT_DATA_PATH,
            LOCATION,
            MIME_TYPE
        )
        processed_pdf = get_tables(json_name, OUTPUT_DATA_PATH)
        return send_file(processed_pdf, as_attachment=True)

    else:
        return jsonify({'error': 'Invalid function selection'})

if __name__ == "__main__":
    app.run(debug=True)
