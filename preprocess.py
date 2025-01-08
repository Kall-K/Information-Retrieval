import os, sys
import json, string
from collections import defaultdict
from timeit import default_timer as timer

BAD_WORDS = ['and', 'or', 'not', 'the']
NUM_DOCS = 1239
PATH = "collection\\docs"

def missing_files():
    # get all files from docs folder
    docs =  [int(d) for d in os.listdir(PATH)]
    
    # find missing documents
    missf = []
    for i in range(NUM_DOCS):
        if i+1 not in docs:
            missf.append(i+1)

    return missf


def inverted_file(model, type):
    docs = os.listdir(PATH)
    my_dict = defaultdict(type) # needs list on boolean model/ dict in vsm

    for d in docs:
        doc = PATH + '\\' + d 
        with open(doc, "r") as f:
            text = f.read()
        f.close()

        text = text.translate(str.maketrans('', '', string.punctuation))
        words = text.lower().split()

        if model == 'vsm':
            # 1 vsm model
            start = timer()
            for w in words:
                if w not in BAD_WORDS and len(w) > 2:
                    if w not in my_dict.keys():
                        my_dict[w] = {
                            'doc': [d],
                            'f': [1]
                        }
                    else: # here the word has already been found in previous document or in the same document
                        if d not in my_dict[w]['doc']:
                            my_dict[w]['doc'].append(d)
                            my_dict[w]['f'].append(1)
                        else:
                            my_dict[w]['f'][-1] = my_dict[w]['f'][-1] + 1
        elif model == 'boolean':
            # 2 boolean model
            start = timer()
            for w in words:
                if w not in BAD_WORDS and len(w) > 2:
                    if d in my_dict[w]:
                        continue
                    my_dict[w].append(d)
        end = timer()

    print(f'Num of found words: {len(my_dict.keys())}')
    print(f'{model.upper()}, Elapsed Time: {(end-start)*1000} ')
    with open(f"inverted_dict_{model}.json", "w") as outfile: 
        json.dump(my_dict, outfile)
    outfile.close()

if __name__ == '__main__':
    missf = missing_files()
    print(f'Num of missing files: {len(missf)} \nNum of documents: {NUM_DOCS-len(missf)}')

    model = 'boolean' #default
    type = list

    if len(sys.argv) > 1 : 
        arg = sys.argv[1]       
        if arg == 'vsm':
            model = 'vsm'
            type = dict
            # print(type)
    inverted_file(model, type)