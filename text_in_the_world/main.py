import openai

# input_text = "TAXI TRANSPORTATION INFORMATION YELLOW CAB (831) 333-1234"
result = openai.Completion.create(
    model="text-davinci-003",
    prompt="Please write an email to my father explaining why I am late today:",
    temperature=0,
    max_tokens=128,
    top_p=1,
    frequency_penalty=0,
    presence_penalty=0)

res = result["choices"][0]['text']
res = res.split("END")[0]
print(res)

