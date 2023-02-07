from textInTheWorld.gpt3.wrapper import LLMWrapper
import json

class ContextGenerator():
    def __init__(self):
        self.gpt3 = LLMWrapper()
        return None

    def read_template(self, path):
        with open(path) as f:
            contents = f.read()
            self.template = contents
    
    def generate_prompt(self, text):
        prompt = self.template.replace('[INPUT_TEXT]', text)
        return prompt

    def generate(self, prompt):
        result = self.gpt3.text_completion(prompt)
        # res = json.loads(result)
        return result

    def context_complete(self, text, template):
        self.read_template(template)
        prompt = self.generate_prompt(text)
        context = self.generate(prompt)
        context = json.loads(context)
        return context

    def text_clean(self, text, template):
        self.read_template(template)
        t = text.replace('\n', ' ')
        prompt = self.generate_prompt(t)
        clean_text = self.generate(prompt)
        return clean_text
