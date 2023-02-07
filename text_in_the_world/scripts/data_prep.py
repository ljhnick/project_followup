from textInTheWorld.utils.file_reader import CSVReader, PDFReader
from textInTheWorld.data.process import RawDataProcess
from textInTheWorld.ocr.image_processer import TextReaderOCR
from textInTheWorld.preprocessing.context import ContextGenerator
from pathlib import Path
import textInTheWorld.utils.handler as handler
from tqdm import tqdm
import os
import openai
import numpy as np

openai.api_key = os.getenv("OPENAI_API_KEY")

def multiple_entry(): # this focuses on the 36 images
    root = Path(__file__).parent.parent
    data_folder = root / 'data'

    csvReader = CSVReader(data_folder)
    processed_data = RawDataProcess(csvReader.data_list)

def user_data():
    # read data first
    data_path = '/Users/ljhnick/Meta/project_followup/text_in_the_world/data/clean/data_participants.json'
    data = handler.read_json(data_path)

    ocrReader = TextReaderOCR()
    for entry in tqdm(data['data']):
        img_path = entry['img_path']
        try:
            result = ocrReader.read_raw(img_path)
        except:
            print('cannot read text')
            continue
        description = entry['description']
        path = entry['img_path']
        ocrReader.filter_text(result, description, path)

def user_data_labeled():
    csv_path = '/Users/ljhnick/Meta/project_followup/text_in_the_world/data/raw/csv_labeled_action/Actions.csv'
    pdf_folder = '/Users/ljhnick/Meta/project_followup/text_in_the_world/data/raw/pdf'
    context_template = '/Users/ljhnick/Meta/project_followup/text_in_the_world/data/text/text_extract_context.txt'
    clean_text_template = '/Users/ljhnick/Meta/project_followup/text_in_the_world/data/text/text_clean.txt'

    csvReader = CSVReader()
    pdfReader = PDFReader()
    ocrReader = TextReaderOCR()
    contextGen = ContextGenerator()
    # contextGen.read_template(context_template)

    csv_data = csvReader.read_csv(csv_path)

    pdf_folder_path = Path(pdf_folder)

    csv_shuffled = csv_data.values
    
    data_result = []
    np.random.shuffle(csv_shuffled)
    for data in tqdm(csv_shuffled):
        file_num = data[3]
        page = data[5]-1
        action = data[4].split('> ')[1]

        file_path = pdf_folder_path / f'{file_num}.pdf'
        img_bytes = pdfReader.read_img_as_bytes(file_path, page)
        description = pdfReader.read_text_from_page(file_path, page)
        
        try:
            context = contextGen.context_complete(description, context_template)
        # print(context)
        except Exception as e:
            print(e)
            print(data)
            continue
        
        ocr_result = ocrReader.read_bytes(img_bytes)
        
        data_json = {}
        data_json['text'] = ocr_result
        data_json['context'] = context
        data_json['action'] = action

        # print(f'***********ACTION: {action}**************')
        data_result.append(data_json)
        
    handler.save_json(data_result, '/Users/ljhnick/Meta/project_followup/text_in_the_world/data/clean/data_648_labeled.json')
    # print(csv_data)


if __name__ == '__main__':
    user_data_labeled()