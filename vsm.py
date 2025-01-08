'''
Sim(q,dj) = [Σ(wij * wiq)] / |dj| * |q|
N ο συνολικός αριθμός κειμένων στη συλλογή
ni ο αριθμός κειμένων που περιέχουν τον όρο ki
freq(i,j) συχνότητα του ki στο dj
idf(i) = log (N/ni)
f(i,j) = freq(i,j) / max(freq(l,j))  το l πρεπει να είναι καποιος ορος του κειμενου j 
wij= f(i,j) * log(N/ni) -> καλείταιtf-idf ζυγισμένο σχήμα
wiq= (0.5 + [0.5 * freq(i,q) / max(freq(l,q)]) * log(N/ni)
'''
import os
from statistics import mode
from collections import Counter
import math as m
import json

DOCS =  tuple(os.listdir("collection\\docs"))
NUM_DOCS = len(DOCS)


def doc_max_freq(inverted_dict, doc):

    max_f = {'term':None, 'f':0}

    for term, val in inverted_dict.items():

        if doc in val['doc']:
            idx = val['doc'].index(doc)
            f = val['f'][idx]

            if f > max_f['f']:
                max_f['f'] = f
                max_f['term'] = term

    return max_f


def query_weights(query, inverted_dict):

    terms = query.split()
    terms = [t for t in terms if t in inverted_dict.keys()]
    w = []

    terms_f = Counter(terms)
    max_term = mode(terms)

    for t_f, val in terms_f.items():
        ni = len(inverted_dict[t_f]['doc'])
        w_t = 0.5 + ((0.5 * (val / terms_f[max_term])) * m.log10(NUM_DOCS/ni))
        w.append(w_t)
   
    # v2
    # for term, val in inverted_dict.items():
    #     if term in terms_f.keys():
    #         ni = len(val['doc'])
    #         w_t = 0.5 + ((0.5 * (terms_f[term] / terms_f[max_term])) * m.log10(NUM_DOCS/ni))
    #         w.append(w_t)
    #     else: 
    #         w.append(0)
    return w, terms_f


def doc_weights(inverted_dict, doc, q_terms):
    w = []
    max_f = doc_max_freq(inverted_dict, doc)

    for t_f in q_terms.keys():
        
        if doc in inverted_dict[t_f]['doc']:

            idx = inverted_dict[t_f]['doc'].index(doc)

            f = inverted_dict[t_f]['f'][idx]
            
            ni = len(inverted_dict[t_f]['doc'])

            w_t = (f / max_f['f']) * m.log10(NUM_DOCS/ni)
            w.append(w_t)
        else: w.append(0)
    
    # v2
    # for _, val in inverted_dict.items():

    #     if doc in val['doc']:
    #         idx = val['doc'].index(doc)
    #         f = val['f'][idx]
    #         ni = len(val['doc'])
    #         w_t = (f / max_f['f']) * m.log10(NUM_DOCS/ni)
    #         w.append(w_t)
    #     else: w.append(0)

    return w

def norm(vector):
    return m.sqrt(sum(x**2 for x in vector))

def similarity(doc_w, query_w):

    s = [d*q for d, q in zip(doc_w, query_w)]

    
    return sum(s) / (norm(doc_w) * norm(query_w))



def vsm_main(query,save=False):
    f = open('inverted_dict_vsm.json')
    inverted_dict = json.load(f)
    f.close()

    query = query.lower()
    query_w, query_terms = query_weights(query, inverted_dict)
    sims = {}

    for doc in DOCS:
        doc_w = doc_weights(inverted_dict, doc, query_terms)
        if all(x == 0 for x in doc_w): 
            continue # sim = 0
        else: 
            sim = similarity(doc_w, query_w)
            sims[doc] = sim

    sorted_data = dict(sorted(sims.items(), key=lambda item: item[1], reverse=True))
    sorted_data = filter(lambda kv: kv[1] != 0, sorted_data.items())
    
    if save:
        with open('similarities.json', "w") as outfile:
            json.dump(dict(sorted_data), outfile)
        outfile.close()
    
    return [sd[0] for sd in sorted_data]

if __name__ == '__main__':
    query = 'How effective are inhalations of mucolytic agents in the treatment of CF patients'#input
    vsm_main(query, save=True)