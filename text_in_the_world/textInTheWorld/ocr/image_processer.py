import cv2
import easyocr
from textInTheWorld.gpt3.wrapper import LLMWrapper
import json
import textInTheWorld.utils.handler as handler

class TextReaderOCR():
    savepath_ = '/Users/ljhnick/Meta/project_followup/text_in_the_world/data/clean/data_user_filtered.json'
    
    def __init__(self):
        # self.root_path = rootpath
        self.reader = easyocr.Reader(['en'], quantize=False)
        self.gpt3 = LLMWrapper()
        self.prompt_generator = PromptGenerator()
        self.data_processed = {'data': []}
     
    def _read_image(self, filepath, max_resolution=1500):
        img = cv2.imread(filepath)
        width = img.shape[1]
        height = img.shape[0]
        if max(width, height) > max_resolution:
            ratio = max(width, height)/max_resolution
            img = cv2.resize(img, (int(width/ratio),int(height/ratio)))
        self.img = img
        return img

    def read_text(self, img, detail=0, paragraph=False):
        result = self.reader.readtext(img, detail=detail, paragraph=paragraph)
        return result

    def read_raw(self, path):
        img = self._read_image(path)
        result = self.read_text(img)
        return result

    def filter_text(self, text, description):
        result = self.prompt_generator.generate(text, description)
        result_gpt = self.gpt3.text_completion(result)

        try:
            data_json = json.loads(result_gpt)
            data_json['raw_text'] = text
            data_json['description'] = description
            self.data_processed['data'].append(data_json)
        except:
            return

        # save the data
        handler.save_json(self.data_processed, self.savepath_)
        # print(data_json)


class PromptGenerator():
    coding_keys = ["text", "places", "activities", "actions"]

    def __init__(self):
        self.prompt = self.initilize_prompt(self.coding_keys)
        # self.text = text
        # self.description = description

    def initilize_prompt(self, coding_keys):
        prompt = 'Clean the following text recognized from an image, including fixing the typo, removing unmeaningful phrases and complete the sentence. Also predict possible places the text is on, what is the activity and what the user would like to do with it after taking the image based on the user description of the photo. The output should be in JSON format with the following keys: '
        for key in coding_keys:
            prompt = prompt + f'"{key}", ' 
        prompt = prompt[:-2]
        prompt += '.\n\n'
        return prompt

    def generate(self, text, description):
        self.text = text
        self.description = description
        
        prompt = self.prompt
        prompt = prompt + "Text: "
        for t in text:
            prompt = prompt + f"'{t}', "
        prompt = prompt[:-2]
        prompt += '\n\nUser Description: '
        prompt += description
        prompt = prompt + '\n\nResult:'

        self.generated_prompt = prompt
        return prompt
        





def main():
    filepath = '/Users/ljhnick/Meta/project_followup/text_in_the_world/data/raw/img/1/Chris J-15223498-2350587-281452.jpg'

    readerOCR = TextReaderOCR(filepath)
    img = cv2.imread(filepath)

    width = img.shape[1]
    height = img.shape[0]
    
    ratio = max(height, width)/1500
    img = cv2.resize(img, (int(width/ratio), int(height/ratio)))
    reader = easyocr.Reader(['en'], quantize=False)
    result = reader.readtext(img, detail=0, paragraph=False)
    print(result)

    
    print(img.shape)

if __name__ == "__main__":
    main()