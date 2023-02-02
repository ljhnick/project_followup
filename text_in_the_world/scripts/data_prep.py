from textInTheWorld.utils.file_reader import CSVReader
from textInTheWorld.data.process import RawDataProcess
from textInTheWorld.ocr.image_processer import TextReaderOCR
from pathlib import Path
import textInTheWorld.utils.handler as handler
from tqdm import tqdm
import os
import openai

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


if __name__ == '__main__':
    user_data()