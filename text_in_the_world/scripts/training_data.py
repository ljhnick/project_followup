import json
from textInTheWorld.data.prep import TrainingDataPrep, TrainingDataPrepUserData, TrainingDataLabeled

def main():
    filepath =  "/Users/ljhnick/Meta/project_followup/text_in_the_world/data/clean/result.json"
    trainData = TrainingDataPrep(filepath)

def user_data():
    path = '/Users/ljhnick/Meta/project_followup/text_in_the_world/data/clean/data_user_filtered.json'
    data_prep = TrainingDataPrepUserData(path)
    data_prep.parse_data()

def user_data_labeled():
    path = '/Users/ljhnick/Meta/project_followup/text_in_the_world/data/clean/data_648_labeled.json'
    data_prep = TrainingDataLabeled()
    data_prep.load_raw(path)
    data_prep.prepare_data()

if __name__ == '__main__':
    user_data_labeled()