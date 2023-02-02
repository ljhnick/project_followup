import textInTheWorld.utils.handler as handler
from textInTheWorld.gpt3.wrapper import LLMWrapper, LLMTest
from tqdm import tqdm
import json

def compare(pred, pretrained, gt):
    predict = pred.lower().replace(' ', '')
    predict = predict.split(';')

    # if pretrained.__class__ != list:
    is_true_tuned = False
    is_true_pretrain = False

    ground = gt.lower().replace(' ', '')
    ground = ground.split(';') 

    for p in predict:
        if p[-1] == '.':
            p = p[:-1]
        for g in ground:
            if g[-1] == '.':
                g = g[:-1]
            if p == g:
                is_true_tuned = True

    if pretrained.__class__ == list:
        for data in pretrained:
            data = data.lower().replace(' ', '')
            data = data.replace('.', '')
            for g in ground:
                if g[-1] == '.':
                    g = g[:-1]
                if data == g:
                    is_true_pretrain = True
    else:
        data = pretrained.lower().replace(' ', '')
        data = data.replace('.', '')
        for g in ground:
            if g[-1] == '.':
                g = g[:-1]
            if data == g:
                is_true_pretrain = True

    return (is_true_tuned, is_true_pretrain)

def main():
    filepath = '/Users/ljhnick/Meta/project_followup/text_in_the_world/data/train/user_data_val.json'
    model_name = "ada:ft-personal:text-in-the-world-user-data-2023-02-01-17-34-23"
    model_davinci = 'text-davinci-003'
    data = handler.read_json(filepath)
    gpt3 = LLMWrapper()

    gpt3_test = LLMTest()
    # print(gpt3_test.categories)

    num_all = 0
    num_true = 0
    num_true_untuned = 0

    for entry in tqdm(data):
        result = gpt3.text_completion(entry['prompt'], model_name)
        result_untuned = gpt3_test.categorize(entry['prompt'])
        result_untuned = json.loads(result_untuned)['categories']

        result = result.split('END')[0]
        gt = entry['completion']
        ismatch = compare(result, result_untuned, gt)
        ismatch_tuned = ismatch[0]
        ismatch_untuned = ismatch[1]

        # print(f'predict: {result}, gt: {gt}, untuned: {result_untuned}')
        print(ismatch)
        if ismatch_tuned:
            num_true += 1
        if ismatch_untuned:
            num_true_untuned += 1
        num_all += 1
    
    accuracy_tuned = num_true / num_all
    accuracy_untuned = num_true_untuned / num_all
    print(f'the accuracy of the train model tested on the validation set is {accuracy_tuned}, the accuracy of the pretrained model is {accuracy_untuned}')

    


if __name__ == '__main__':
    main()