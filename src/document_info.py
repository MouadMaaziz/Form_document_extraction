import pdfx
import pandas as pd
import os












def get_info(pdf_file,OUTPUT_DATA_PATH):
    pdf = pdfx.PDFx(pdf_file)
    metadata = pdf.get_metadata()
    print(metadata)
    df = pd.DataFrame(metadata)
    excel_file = os.path.join(OUTPUT_DATA_PATH, f'{pdf_file.stem}_metadata.xlsx')
    df.to_excel(excel_file, sheet_name='metadata_by_pdfx', index=False)