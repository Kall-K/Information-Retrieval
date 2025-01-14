from langchain_core.prompts import ChatPromptTemplate
from langchain_ollama.llms import OllamaLLM
import boolean, vsm
import sys

def model_call(model, query):
    text = ''
    if model == 'boolean':
        docs = boolean.boolean_main(query)
    elif model == 'vsm':
         docs = vsm.vsm_main(query)

    for doc in docs[:3]:
        path = 'collection\\docs\\' + doc
        with open(path, "r") as f:
                    txt = f.read()
                    txt = txt.replace('\n', ' ')
                    text = text + 'Document ' + doc + ': ' + txt + '\n'
        f.close()

    with open("text.txt", "w") as f:
        f.writelines(text)
    f.close()

    return text


if __name__ == '__main__':
    query = 'How effective are inhalations of \
    mucolytic agents in the treatment of CF patients?'
    # query = input('Enter your question: ')
    model = 'boolean'

    if len(sys.argv) > 1 : 
        arg = sys.argv[1]       
        if arg == 'vsm':
            model = 'vsm'

    text = model_call(model, query)

    template = "Question: Based on this text {text} answer the question {question}"

    prompt = ChatPromptTemplate.from_template(template)

    model = OllamaLLM(model='llama3.2')

    chain = prompt | model

    print(chain.invoke({'text': text, 
                        'question': query}))