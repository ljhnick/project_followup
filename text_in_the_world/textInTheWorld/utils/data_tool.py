
def fine_tune_data_tool(prompt, completion):
    sep = '\n\n###\n\n'
    p = prompt.replace(sep, '')
    p += sep

    c = " " + completion

    return p, c