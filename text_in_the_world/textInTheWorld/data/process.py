from textInTheWorld.gpt3.wrapper import LLMWrapper
import json
from pathlib import Path
from tqdm import tqdm
import time


class RawDataProcesserSingle():
    _categories = json.load(open(str(Path(__file__).parent / 'categories.json')))
    _categories = _categories['categories']

    _savepath = "/Users/ljhnick/Meta/project_followup/text_in_the_world/data/clean/result.json"

    def __init__(self, data):
        self.data = data
        self.gpt3 = LLMWrapper()
        self.data_processed = [{}, {}]
        self._prompt_init()
        self.result = []
        
        self.process()

    def _prompt_init(self):
        t = "Classify the category of the following responses in the following categories:"
        for cat in self._categories:
            t = t + " " + cat + ","
        t = t[:-1]
        t += ":\n\n"

        t += "Input: "
        self.init_prompt = t

    def _read_results(self):
        results = json.load(open(self._savepath))
        return results
    
    def _save_results(self, results):
        with open(self._savepath, 'w', encoding='utf-8') as f:
            json.dump(results, f, ensure_ascii=False)

    def process(self):
        self.get_input_text(self.data)
        self.get_response_text(self.data)
        
        num = 2
        for index in range(num):
            self.result.append(self.categorize(index))

    def get_input_text(self, data):
        columns = data.columns.values
        text_1 = columns[27]
        text_2 = columns[35]
        
        input_1 = text_1.split('*"')[1].split('"*')[0]
        input_2 = text_2.split('*"')[1].split('"*')[0]        
        input_text = (input_1, input_2)

        self.input_text = input_text

    def get_response_text(self, data):
        r1 = data.values[:, 34]
        r2 = data.values[:, 42]
        self.responses = (r1, r2)
    
    def _result_init(self):
        result = {}
        result['input_text'] = ""
        result['actions'] = []
        for cat in self._categories:
            each = {}
            each['cat'] = cat
            each['num'] = 0
            result['actions'].append(each)
        return result

    def _update_result(self, result, response):
        for each in result['actions']:
            if each['cat'] == response:
                each['num'] += 1
                # print(each['cat'])
                break

    def categorize(self, i):
        result = self._result_init()
        input = self.input_text[i]
        result['input_text'] = input
        responses = self.responses[i]
        
        # complete the prompt here
        for r in tqdm(responses):
            prompt = self.init_prompt + r
            prompt += "\nOutput:"
            cat = self.gpt3.text_completion(prompt)
            cat_split = cat.split(',')
            for category in cat_split:
                cat_str = category.split(".")[0]
                if cat_str[0] == " ":
                    cat_str = cat_str[1:]
                self._update_result(result, cat_str.lower())

            time.sleep(0.5)
        
        saved_results = self._read_results()
        saved_results['results'].append(result)

        self._save_results(saved_results)

        return result
                
            

class RawDataProcess():
    _savepath = "/Users/ljhnick/Meta/project_followup/text_in_the_world/data/clean/result.json"

    def __init__(self, data_list):
        self.did_process = []
        self._init_save()
        self.process_each(data_list)

    def _init_save(self):
        saveresult = {"results": []}
        with open(self._savepath, 'w', encoding='utf-8') as f:
            json.dump(saveresult, f, ensure_ascii=False)

    def process_each(self, data_list):
        for data in tqdm(data_list):
            self.did_process.append(RawDataProcesserSingle(data))

        print(1)