import json 

def save_json(data, savepath):
    with open(savepath, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False)

def read_json(filepath):
    f = open(filepath)
    result = json.load(f)
    return result