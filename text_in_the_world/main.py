import openai

input_text = "TAXI TRANSPORTATION INFORMATION YELLOW CAB (831) 333-1234"
result = openai.Completion.create(
    model="davinci:ft-personal:textintheworld-v1-2023-01-27-18-08-16",
    prompt=f"Please give 4 most possible actions from the list provided when people take a picture which contains the text.\nList of actions: remember for later, share it on social media, send it to someone, capture the moment, look for more information, set a reminder, translate, others\n\nText: '{input_text}'\n\n###\n\n",
    temperature=0,
    max_tokens=128,
    top_p=1,
    frequency_penalty=0,
    presence_penalty=0)

res = result["choices"][0]['text']
res = res.split("END")[0]
print(res)

