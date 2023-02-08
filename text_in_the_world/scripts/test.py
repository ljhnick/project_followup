import hydra
import json
from textInTheWorld.gpt3.wrapper import LLMWrapper
from textInTheWorld.data.category_handler import CategoryHandler
from tqdm import tqdm


config_path = "/Users/ljhnick/Meta/project_followup/text_in_the_world/config"

test_file = '/Users/ljhnick/Meta/project_followup/text_in_the_world/data/train/labeled/val_prepared.jsonl'

def validate_predicted(gt, logprobs, num=1):
    pred = []
    pred_sorted = sorted(logprobs, key=logprobs.get, reverse=True)
    for i in range(num):
        pred.append(pred_sorted[i])

    for predition in pred:
        if predition == gt:
            return True
        
    return False

def validate_pretrained(gt, pred_pt):
    path = '/Users/ljhnick/Meta/project_followup/text_in_the_world/textInTheWorld/data/categories.json'
    cat_handler = CategoryHandler(path)
    cat_name = cat_handler.get_cat_name(int(gt))

    pred = pred_pt.replace("'", '"')
    pred = json.loads(pred)['category']
    
    for cat in pred:
        if cat.lower() == cat_name.lower():
            return True

    return False

def classify_pretrained(prompt, num_of_pred):
    text_template = '/Users/ljhnick/Meta/project_followup/text_in_the_world/data/text/text_categories.txt'
    with open(text_template, 'r') as f:
        text = f.read()

    text = text.replace('[NUM_OF_CATEGORIES', f'{num_of_pred}')
    text = text.replace('[INPUT_TEXT]', prompt)
    
    return text 
    
@hydra.main(version_base=None, config_path=config_path, config_name="config")
def main(cfg):
    model_ada = cfg.trained_models.ada
    model_davinci = cfg.trained_models.davinci

    gpt3 = LLMWrapper()
    num_of_pred = 3

    test_pretrained = True

    with open(test_file, 'r') as f:
        json_list = list(f)

    num_all = 0
    num_true = 0

    if not test_pretrained:
        for entry in tqdm(json_list):
            dict = json.loads(entry)
            prompt = dict['prompt']
            ground_truth = dict['completion']

            _, logprobs = gpt3.text_classification(prompt, model=model_davinci, num_of_class=7)
            
            result = validate_predicted(ground_truth, logprobs, num=num_of_pred)
            if result:
                num_true += 1

            num_all += 1
        acc = num_true / num_all

        print(f'the accuracy of the prediction when predicting {num_of_pred} result is {acc}')
    
    else:
        for entry in tqdm(json_list):
            dict = json.loads(entry)
            prompt = dict['prompt']
            ground_truth = dict['completion']

            final_prompt = classify_pretrained(prompt, num_of_pred)
            result = gpt3.text_completion(final_prompt)
            isacc = validate_pretrained(ground_truth, result)
            if isacc:
                num_true += 1

            num_all += 1
        acc = num_true / num_all
        print(f'the accuracy of the pretrain model (gpt 3 davinci) when predicting {num_of_pred} result is {acc}')






if __name__ == '__main__':
    main()