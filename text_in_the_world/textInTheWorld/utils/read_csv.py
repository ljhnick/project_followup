import pandas as pd
from pathlib import Path
import glob

class CSVReader():
    def __init__(self, folder):
        self.file_list = glob.glob(str(folder) + '/*.csv')
        self.data_list = []
        self.read_all_data(self.file_list)

    def read_all_data(self, list):
        for filepath in list:
            data = pd.read_csv(filepath)
            self.data_list.append(data)


# test below
def test():
    filepath = "/Users/ljhnick/Meta/project_followup/text_in_the_world/data/raw/csv/entry_1.csv"
    data = pd.read_csv(filepath)
    columns = data.columns.values
    print(f'first: {columns[27]}, \n second: {columns[35]}')
    print(data.values[:, 34])
    # print(data)

if __name__ == '__main__':
    test()