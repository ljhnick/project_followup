import json
from textInTheWorld.data.prep import TrainingDataPrep, TrainingDataPrepUserData

def main():
    filepath =  "/Users/ljhnick/Meta/project_followup/text_in_the_world/data/clean/result.json"
    trainData = TrainingDataPrep(filepath)

def user_data():
    path = '/Users/ljhnick/Meta/project_followup/text_in_the_world/data/clean/data_user_filtered.json'
    data_prep = TrainingDataPrepUserData(path)
    data_prep.parse_data()

if __name__ == '__main__':
    user_data()