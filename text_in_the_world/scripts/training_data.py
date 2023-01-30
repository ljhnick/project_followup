import json
from textInTheWorld.data.prep import TrainingDataPrep

def main():
    filepath =  "/Users/ljhnick/Meta/project_followup/text_in_the_world/data/clean/result.json"
    trainData = TrainingDataPrep(filepath)

if __name__ == '__main__':
    main()