import cv2
import easyocr
from textInTheWorld.gpt3.wrapper import LLMWrapper, LLMClassifier
import json
import textInTheWorld.utils.handler as handler

def detect_text(path):
    """Detects text in the file."""
    from google.cloud import vision
    import io
    client = vision.ImageAnnotatorClient()

    with io.open(path, 'rb') as image_file:
        content = image_file.read()

    image = vision.Image(content=content)

    response = client.text_detection(image=image)
    texts = response.text_annotations
    # print('Texts:')

    # for text in texts:
    #     # print('\n"{}"'.format(text.description))

    #     vertices = (['({},{})'.format(vertex.x, vertex.y)
    #                 for vertex in text.bounding_poly.vertices])

        # print('bounds: {}'.format(','.join(vertices)))

    if response.error.message:
        raise Exception(
            '{}\nFor more info on error messages, check: '
            'https://cloud.google.com/apis/design/errors'.format(
                response.error.message))

    text = texts[0].description
    text = text.replace('\n', '  ')

    return text

class TextReaderOCR():
    savepath_ = '/Users/ljhnick/Meta/project_followup/text_in_the_world/data/clean/data_user_filtered.json'
    
    def __init__(self):
        # self.root_path = rootpath
        # self.reader = easyocr.Reader(['en'], quantize=False)
        self.gpt3 = LLMWrapper()
        self.gpt3_classifier = LLMClassifier()
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

        # print(detect_text(filepath))
        return img

    def read_text(self, img, detail=0, paragraph=False):
        result = self.reader.readtext(img, detail=detail, paragraph=paragraph)
        return result

    def read_raw(self, path):
        # img = self._read_image(path)
        # result = self.read_text(img)
        result = detect_text(path)

        # print(result)
        return result

    def filter_text(self, text, description, img_path):
        result = self.prompt_generator.generate(text, description)
        try:
            result_gpt = self.gpt3.text_completion(result)
            # print(result_gpt)
        except:
            print("gpt 3 failed, pause here")

        try:
            data_json = json.loads(result_gpt)
            categories = self.gpt3_classifier.categorize(data_json['actions'])
            categories = categories.split(',')
            data_json['categories'] = categories
            data_json['raw_text'] = text
            data_json['description'] = description
            data_json['img_path'] = img_path
            self.data_processed['data'].append(data_json)
        except:
            return

        # save the data
        handler.save_json(self.data_processed, self.savepath_)
        # print(data_json)


class PromptGenerator():
    coding_keys = ["text", "places", "activities", "actions"]
    cat_path = '/Users/ljhnick/Meta/project_followup/text_in_the_world/textInTheWorld/data/categories.json'
    _categories = json.load(open(cat_path))
    categories = _categories['categories']

    def __init__(self):
        self.prompt = self.initilize_prompt(self.coding_keys)
        # self.text = text
        # self.description = description

    def initilize_prompt(self, coding_keys):
        prompt = 'Clean the following text recognized from an image, including fixing the typo, removing unmeaningful phrases and complete the sentence.\nBased on the user description, predict possible places the text is on, what is the activity. Also summarize what the user will do with the image.'
        # for cat in self.categories:
        #     prompt = prompt + f'"{cat}"' + ", "
        # prompt = prompt[:-2]
        # prompt += '.'
        prompt = prompt + '\nThe output should be in JSON format with the following keys: '
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
        if text.__class__ == list:
            for t in text:
                prompt = prompt + f"'{t}', "
            prompt = prompt[:-2]
        else:
            prompt += f'"{text}"'
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