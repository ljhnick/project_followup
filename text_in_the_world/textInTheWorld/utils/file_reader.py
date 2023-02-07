import pandas as pd
import glob
import fitz
import io
from PIL import Image

class CSVReader():
    def __init__(self, folder=""):
        if folder != "":
            self.file_list = glob.glob(str(folder) + '/*.csv')
        self.data_list = []

    def read_all_data_subfolders(self, main_folder):
        self.csv_list = glob.glob(str(main_folder) + '/*.csv')
        # print(self.csv_list)
        self.csv_data = []
        for filepath in self.csv_list:
            data = pd.read_csv(filepath)
            self.csv_data.append(data)

    def read_all_data(self, list):
        for filepath in list:
            data = pd.read_csv(filepath)
            self.data_list.append(data)

    def read_csv(self, path):
        data = pd.read_csv(path)
        return data

class IMGReader():
    def __init__(self, folder):
        self.folder_path = folder

    def read_all_subfolders(self):
        self.img_list = glob.glob(str(self.folder_path) + '/**/*.jpg')

class PDFReader:
    def __init__(self):
        return None

    def read_pdf(self, filepath):
        pdf = fitz.open(filepath)
        return pdf

    def read_img_as_bytes(self, filepath, page):
        
        pdf = self.read_pdf(filepath)
        xref = pdf.get_page_images(page)[0][0]
        pixmap = fitz.Pixmap(pdf, xref)
        img_byte = pixmap.tobytes()
        return img_byte

    def read_text_from_page(self, filepath, page):
        pdf = self.read_pdf(filepath)
        text = pdf[page].get_text()
        text = text.replace('\n', ' ')
        return text

# test below

def test():
    filepath = "/Users/ljhnick/Meta/project_followup/text_in_the_world/data/raw/csv/1.csv"
    data = pd.read_csv(filepath)
    columns = data.columns.values
    print(f'first: {columns[27]}, \n second: {columns[35]}')
    print(data.values[:, 34])
    # print(data)

def pdf_test():
    filepath = '/Users/ljhnick/Meta/project_followup/text_in_the_world/data/raw/pdf/Mission 1.pdf'
    reader = PDFReader()

    reader.read_img_as_bytes(filepath, 0)
    reader.read_text_from_page(filepath, 0)

if __name__ == '__main__':
    pdf_test()