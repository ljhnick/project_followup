import hydra
import json
from textInTheWorld.gpt3.wrapper import LLMWrapper
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

    
    
@hydra.main(version_base=None, config_path=config_path, config_name="config")
def main(cfg):
    model_ada = cfg.trained_models.ada
    model_davinci = cfg.trained_models.davinci

    gpt3 = LLMWrapper()
    num_of_pred = 3

    with open(test_file, 'r') as f:
        json_list = list(f)

    num_all = 0
    num_true = 0
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

def test_pretrained():
    text_template = '/Users/ljhnick/Meta/project_followup/text_in_the_world/data/text/text_categories.txt'

    




if __name__ == '__main__':
    main()