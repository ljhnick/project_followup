import os
import openai
import json

class LLMWrapper():
    def __init__(self):
        self.api_key = os.getenv("OPENAI_API_KEY")
    
    def text_completion(self, prompt, model='text-davinci-003', max_token=1024):
        is_success = False
        while not is_success:
            try:
                response = openai.Completion.create(
                    engine=model,
                    prompt=prompt,
                    temperature=0,
                    max_tokens=max_token,
                    top_p=1,
                    frequency_penalty=0,
                    presence_penalty=0
                )
                is_success = True
            except Exception as e:
                print(e)

        

        response_text = response.choices[0].text
        return response_text

    def text_classification(self, prompt, model='text-davinci-003', max_token=1, num_of_class=2):
        response = openai.Completion.create(
            engine=model,
            prompt=prompt,
            temperature=0,
            max_tokens=max_token,
            logprobs=num_of_class,
            top_p=1,
            frequency_penalty=0,
            presence_penalty=0
        )
        
        logprobs = response['choices'][0]['logprobs']['top_logprobs'][0]
        return response, logprobs



class LLMClassifier(LLMWrapper):
    def __init__(self):
        super().__init__()
        path = '/Users/ljhnick/Meta/project_followup/text_in_the_world/textInTheWorld/data/categories.json'
        self.load_categories(path)
        
    def load_categories(self, path):
        cats = json.load(open(path))
        self.categories = cats['categories']

    def init_prompt(self, text):
        p = 'Classify the texts into the following categories: '
        for cat in self.categories:
            p += f'"{cat}",'
        p = p[:-1]
        p += f"\n\nText: {text}\nResult:"
        return p

    def categorize(self, text):
        p = self.init_prompt(text)
        result = self.text_completion(p)
        return result

class LLMTest(LLMClassifier):
    def __init__(self):
        super().__init__()

    def init_prompt(self, text):
        p = 'Classify the following texts based on the context into the following categories: '
        for cat in self.categories:
            p += f'"{cat}",'
        p = p[:-1]
        p += '. The output should be in JSON format with the key "catogories" with no more than two categories.'
        p += f"\n\n{text}\nOutput:"
        return p

    def categorize(self, text):
        p = self.init_prompt(text)
        result = self.text_completion(p)
        return result

def test():
    print(os.getenv("OPENAI_API_KEY"))
    openai.api_key = os.getenv("OPENAI_API_KEY")

    response = "i want to search for the meaning of the word."
    prompt = 'Clean the following text recognized from an image, including fixing the typo, removing unmeaningful phrases and complete the sentence.\nBased on the user description, predict possible places the text is on, what is the activity.\nAnd classify what the user would like to do with the informatio in the image in the following categories: remember for later, share it on social media, send it to someone, capture the moment, look for more information, set a reminder, translate, others.\nThe output should be in JSON format with the following keys: "text", "places", "activities", "actions".\n\nText: "← Restriction Overview  Nov 8, 2022  Your group activity is restricted  Why was your group activity  restricted?  Your previous group activity didn\'t  follow our Community Standards so  you can\'t do things like create, invite,  post and comment in groups.  Laurie Penman  You shared this on your profile >  OPEN Nov 8, 2022  The post repeats false information about  COVID-19 that goes against our Community  Standards.  Rock Singer\'s Fatal Brain Injury  Caused by AstraZeneca Vaccine,  Inquest Concludes  sti  Laurie Penn  NO  for  MB  Patrioted this in Illinois  fi  OPEN Nov 8, 2022  DE 1973 NAS  Rock Singer\'s Fatal Brain  Injury Caused by AstraZeneca  Vaccine, Inquest Concludes  AstraZeneca\'s COVID-19 vaccine caused the  "catastrophic brain injury" that resolved in the  death of a 48-year-old U.X. rock singer two weeks  after he got the worcine, on inquest concluded.  By Suzanne Burdick, Ph.D.  Eign  S"\n\nUser Description: Did I take that photo? Because I am constantly getting restricted by QuickBooks And I have been saving all of my documentation for when the class action starts. Because I\'m gonna be right there getting my piece of fake books but That\'s why I that\'s why I took it. That\'s why I wrote stuff on it. That\'s why I saved it in cataloged it. Yeah. I love saving screenshots. Let me tell you. And in other things that I write on, I also take pictures of, but there\'s none of my phone because I recently download everything to my laptop. I take pictures of the graphs. To send a friends and things like that. So I like my little pen to write on my pictures.\n\nResult:'

    response = openai.Completion.create(
    model="text-davinci-003",
    prompt=prompt,
    temperature=0,
    max_tokens=256,
    top_p=1,
    frequency_penalty=0,
    presence_penalty=0
    )

    print(response.choices[0].text)

if __name__ == '__main__':
    test()