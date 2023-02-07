import json
import random
from pathlib import Path
import textInTheWorld.utils.handler as handler
import textInTheWorld.utils.data_tool as dt
from textInTheWorld.data.category_handler import CategoryHandler
from random import shuffle
import pandas as pd

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


class TrainingDataPrepUserData():

    savepath_ = '/Users/ljhnick/Meta/project_followup/text_in_the_world/data/train/train_data_user.json'
    
    def __init__(self, path):
        self.raw_data_json = handler.read_json(path)
        self.prompt = ""

    def split_data(self, data, val_ratio=0.1):
        num = len(data)
        num_train = int(num*(1-val_ratio))
        data_copy = data
        shuffle(data_copy)
        train_data = data_copy[:num_train]
        val_data = data_copy[num_train:]

        path = Path(self.savepath_).parent
        train_path = path / 'user_data_train.json'
        val_path = path / 'user_data_val.json'
        handler.save_json(train_data, str(train_path))
        handler.save_json(val_data, str(val_path))


    def parse_data(self):
        self.raw_data = self.raw_data_json['data']
        self.data = []
        for data in self.raw_data:
            entry = self.generate_data_single(data)
            self.data.append(entry)
        # handler.save_json(self.data, self.savepath_)
        self.split_data(self.data)


    def generate_data_single(self, data_entry):
        text = data_entry['text']
        place = data_entry['places']
        activity = data_entry['activities']
        description = data_entry['description']
        actions = data_entry['actions']
        categories = data_entry['categories']
        
        # prompt = "The following text is recognized from an image captured by the user. Please predict the user's answer to the following question based on the context:\n1. Why did you take that photo?\n2. What information do you get from the picture, including the text?\n3. What are the potential next steps you would like to do with that photo with text? (you don't have to actually do it)\nThe response should be in one paragraph and oral (transcribed from the video).\n\n"
        prompt = ""

        prompt += f'Text: {text}\n\n'
        prompt += 'Context:\n- Place of the text: '
        if place.__class__ == list:
            for pl in place:
                prompt = prompt + pl + ','
            prompt = prompt[:-1]
        else:
            prompt += place

        prompt = prompt + '\n- Activity: '
        if activity.__class__ == list:
            for act in activity:
                prompt = prompt + act + ','
            prompt = prompt[:-1]
        else:
            prompt += activity
        prompt += '\n\nOutput:\n\n###\n\n'

        completion = ""
        if categories.__class__ == list:
            for cat in categories:
                completion += cat
                completion += ";"
            completion = completion[:-1]
            # completion += '.'
        else:
            completion += categories
        # completion += "END"

        entry = {'prompt': prompt, 'completion': completion}
        return entry

class TrainingDataLabeled():
    _catpath = '/Users/ljhnick/Meta/project_followup/text_in_the_world/textInTheWorld/data/categories.json'
    def __init__(self):
        self.cat_handler = CategoryHandler(self._catpath)

    def load_raw(self, path):
        self.data_path = path
        self.data_raw = handler.read_json(path)

    def generate_data_single(self, text, cat_id, context, with_context=True):
        prompt = {}
        prompt['text'] = text
        if with_context:
            prompt['context'] = context

        # prompt = json.dumps(prompt)

        completion = f"{cat_id}"

        # prompt, completion = dt.fine_tune_data_tool(prompt, completion)

        result = {
            'prompt': prompt,
            'completion': completion
        }
        return result

    def split_data(self, data, ratio, train_path, val_path, whole_path):
        random.shuffle(data)
        train_num = int(len(data)*(1-ratio))
        train_data = data[:train_num]
        val_data = data[train_num:]

        df_train = pd.DataFrame(train_data)
        df_val = pd.DataFrame(val_data)
        print(df_train['completion'].value_counts())
        print(df_val['completion'].value_counts())

        handler.save_json(train_data, train_path)
        handler.save_json(val_data, val_path)
        handler.save_json(val_data, whole_path)

    def prepare_data(self, test_ratio=0.15, with_context=True):
        dataset = []
        for data in self.data_raw:
            text = data['text']
            text = text.replace('\n', ' ')
            context = data['context']
            action = data['action']
            cat_id = self.cat_handler.get_cat_id(action)
            
            dataset.append(self.generate_data_single(text, cat_id, context, with_context))
        
        df = pd.DataFrame(dataset)
        df_column = df['completion']
        print(df_column.value_counts())
        train_path = '/Users/ljhnick/Meta/project_followup/text_in_the_world/data/train/labeled/train.json'
        val_path = '/Users/ljhnick/Meta/project_followup/text_in_the_world/data/train/labeled/val.json'
        whole_path = '/Users/ljhnick/Meta/project_followup/text_in_the_world/data/train/labeled/whole.json'
        self.split_data(dataset, test_ratio, train_path, val_path, whole_path)
        
    

        