import os
import openai


class LLMWrapper():
    def __init__(self):
        self.api_key = os.getenv("OPENAI_API_KEY")
    
    def text_completion(self, prompt, model='text-davinci-003'):
        response = openai.Completion.create(
            engine=model,
            prompt=prompt,
            temperature=0,
            max_tokens=256,
            top_p=1,
            frequency_penalty=0,
            presence_penalty=0
        )

        response_text = response.choices[0].text
        return response_text


def test():
    print(os.getenv("OPENAI_API_KEY"))
    openai.api_key = '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'

    response = "i want to search for the meaning of the word."
    prompt = f"Classify the category of the following responses in the following categories: remember for later, share it on social media, capture the moment, send it to someone, set a reminder, look for more information, other: \n\n Input: {response} \n Output:"

    response = openai.Completion.create(
    engine="text-davinci-003",
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