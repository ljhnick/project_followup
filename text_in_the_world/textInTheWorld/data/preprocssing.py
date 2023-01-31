from textInTheWorld.utils.file_reader import CSVReader, IMGReader
import textInTheWorld.utils.handler as sv

class DataPreProcessing():
    
    def __init__(self, csv_path, img_path):
        self.csv_path = csv_path
        self.img_path = img_path

    def read_all_data(self):
        # read csv
        csv_reader = CSVReader(self.csv_path)
        csv_reader.read_all_data_subfolders(self.csv_path)
        # read img
        img_reader = IMGReader(self.img_path)
        img_reader.read_all_subfolders()

        self.csv_data = csv_reader.csv_data
        self.img_file_data = img_reader.img_list

    def map_data(self):
        self.extract_csv()
        self.extract_img()
        result = self.merge_csv_img()
        return result

    def extract_csv(self):
        result = []
        for data in self.csv_data:
            for index in range(len(data.values[:, 0])):
                entry = {}
                scout_id = data.values[index, 0]
                description = data.values[index, 44]
                entry['scout_id'] = scout_id
                entry['description'] = description
                result.append(entry)
        result = sorted(result, key=lambda x:x['scout_id'])
        self.csv_processed_user_uploaded = result
        # print(len(result))

    def extract_img(self):
        result = []
        for img_path in self.img_file_data:
            scout_id = img_path.split('-')[-1].split('.')[0]
            entry = {
                'scout_id': scout_id,
                'img_path': img_path
            }
            result.append(entry)
        result = sorted(result, key=lambda x:int(x['scout_id']))
        self.img_path_proecess_user_uploaded = result
        # print(len(result))

    def merge_csv_img(self):
        result = []
        for i in range(len(self.img_path_proecess_user_uploaded)):
            entry = {
                'scout_id': self.img_path_proecess_user_uploaded[i]['scout_id'],
                'img_path': self.img_path_proecess_user_uploaded[i]['img_path'],
                'description': self.csv_processed_user_uploaded[i]['description']
            }
            result.append(entry)
        return result




def test():
    csv = '/Users/ljhnick/Meta/project_followup/text_in_the_world/data/raw/csv'
    img = '/Users/ljhnick/Meta/project_followup/text_in_the_world/data/raw/img'
    prep = DataPreProcessing(csv, img)
    prep.read_all_data()
    result = prep.map_data()
    dict_save = {"data": result}

    save_path = '/Users/ljhnick/Meta/project_followup/text_in_the_world/data/clean/data_participants.json'
    sv.save_json(dict_save, save_path)

if __name__ == '__main__':
    test()