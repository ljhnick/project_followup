import cv2
import easyocr
from textInTheWorld.gpt3.wrapper import LLMWrapper
# import textInTheWorld.utils.handler as handler

class TextReaderOCR():
    def __init__(self):
        # self.root_path = rootpath
        self.reader = easyocr.Reader(['en'], quantize=False)
        self.gpt3 = LLMWrapper()
     
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

    def filter_text(self, text):
        pass


class PromptGenerator():
    
    def __init__(self):
        pass

    



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