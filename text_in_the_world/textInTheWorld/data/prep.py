import json
from pathlib import Path

class TrainingDataPrep():

    num_of_pos = 4
    _categories = json.load(open(str(Path(__file__).parent / 'categories.json')))
    _categories = _categories['categories']

    _save = '/Users/ljhnick/Meta/project_followup/text_in_the_world/data/train/train_data.json'

    def __init__(self, filepath):
        self.rawdata = json.load(open(filepath))
        self.traindata = []
        self.analyze(self.rawdata)
        
    def _data_entry(self):
        return {"prompt": "", "completion": ""}

    def analyze(self, data):
        for i in range(len(data["results"])-2):
            entry = data["results"][i]
            self.analyze_entry(entry)

        with open(self._save, 'w', encoding='utf-8') as f:
            json.dump(self.traindata, f, ensure_ascii=False)
            
        # for entry in data["results"]:
        #     self.analyze_entry(entry)
        

    def analyze_entry(self, entry):
        actions = entry["actions"]
        sorted_act = sorted(actions, key=lambda k:k['num'], reverse=True)
        completion = self.generate_completion(sorted_act)
        prompt = self.generate_prompt(entry["input_text"])

        train_entry = self._data_entry()
        train_entry["prompt"] = prompt
        train_entry["completion"] = completion

        self.traindata.append(train_entry)

    def generate_prompt(self, input):
        t = f"Please give {self.num_of_pos} most possible actions from the list provided when people take a picture which contains the text.\nList of actions: "

        for cat in self._categories:
            t = t + cat + ", "
        t = t[:-2]
        
        t += f"\n\nText: '{input}'\n\n###\n\n"

        return t

        
    def generate_completion(self, sorted_act):  
        num = self.num_of_pos
        t = f"The top {num} possible actions in order are:\n"
        for i in range(num):
            t += f"{i+1}. "
            t += sorted_act[i]['cat']
            t += "\n"
        t = t[:-1]
        # t += "."

        return t
    
    