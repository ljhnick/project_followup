from textInTheWorld.utils.read_csv import CSVReader
from textInTheWorld.data.process import RawDataProcess
from pathlib import Path

def main():
    root = Path(__file__).parent.parent
    data_folder = root / 'data'

    csvReader = CSVReader(data_folder)
    processed_data = RawDataProcess(csvReader.data_list)

if __name__ == '__main__':
    main()