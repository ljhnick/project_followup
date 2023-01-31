import pandas as pd
from pathlib import Path
import glob

class CSVReader():
    def __init__(self, folder):
        self.file_list = glob.glob(str(folder) + '/*.csv')
        self.data_list = []
        # self.read_all_data(self.file_list)

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

class IMGReader():
    def __init__(self, folder):
        self.folder_path = folder

    def read_all_subfolders(self):
        self.img_list = glob.glob(str(self.folder_path) + '/**/*.jpg')



# test below

def test():
    filepath = "/Users/ljhnick/Meta/project_followup/text_in_the_world/data/raw/csv/1.csv"
    data = pd.read_csv(filepath)
    columns = data.columns.values
    print(f'first: {columns[27]}, \n second: {columns[35]}')
    print(data.values[:, 34])
    # print(data)

if __name__ == '__main__':
    test()