import re, os, json
from collections import defaultdict

'''
convention:
use the following operators 
-and 
-or
-not
'''
'''
na koitaxo mhpos anti gia set na xrisimopoiiso dianisma. to dianisma tha einai osa kai ta keimena. 
kathe lexi tha exei to diko ths dianisa me 1 se opoio doc yparxei kai oi praxeis tha ginontai bitwise.
'''


PATH1 = os.getcwd() + "\\inverted_dict_boolean.json"
with open(PATH1, 'r') as f:
       inv_dict =  json.load(f)
f.close()

PATH2 = os.getcwd() + "\\collection\\docs"
whole =  set(os.listdir(PATH2))
DOCS =  tuple(os.listdir(PATH2))

def calc_expression(exp):
    
    set_exp = set()
    
    while len(exp) != 0:
        t1 = exp.pop()
        if t1 == 'and':
            t2 = exp.pop()
            if type(t2) == str: t2 = set(inv_dict[t2])            
            set_exp = set_exp & t2
        elif t1 == 'or':
            t2 = exp.pop()
            if type(t2) == str: t2 = set(inv_dict[t2])            
            set_exp = set_exp | t2
        elif t1 == 'not':
            t2 = exp.pop()
            if type(t2) == str: t2 = set(inv_dict[t2])            
            set_exp = whole - t2
        else:
            if type(t1) == str: set_exp.update(set(inv_dict[t1]))
            else: set_exp = t1

    return set_exp

def unwrapper(exp):

    exp_f = []

    while len(exp)!=0:
        t = exp.pop()

        if ')' == t:
            exp, value = unwrapper(exp)
            exp_f.append(value)
        elif '(' == t: 
            return exp, calc_expression(exp_f)
        else:
            exp_f.append(t)

    return calc_expression(exp_f)

def build_matrix(terms):

    boolean_matrix = defaultdict(list)
    
    for t in terms:
        if t in inv_dict.keys():
            for d in DOCS:
                if d in inv_dict[t]: boolean_matrix[d].append(1)
                else: boolean_matrix[d].append(0)

    return boolean_matrix
                

def boolean_matrix(exp):
    doc_matrix = defaultdict(list)
    for d in DOCS:
        for e in exp:
            if d in inv_dict[e]: doc_matrix[d].append(1)
            else: doc_matrix[d].append(0)
    
    return doc_matrix

def result(doc_matrix):
    ranking = {}
    for d, vec in doc_matrix.items():
        s = sum(vec)
        ranking[d] = s

    ranking = dict(sorted(ranking.items(), key=lambda item: item[1], reverse=True))
    ranking = dict(filter(lambda kv: kv[1] != 0, ranking.items()))

    return ranking

    

def boolean_main(query):
    query.lower()
    query = [q for q in query.split() if q in inv_dict.keys()]
    exp = ' or '.join(query)
    exp = exp.split()
    # res = unwrapper(exp)    
    res = result(boolean_matrix(query))
    print(len(res))
    return list(res)

def boolean_expression(expression):
    exp = re.split(r'(\s+|\(|\))', expression)
    exp = [token for token in exp if token.strip()]

    # chars = ['(', ')', 'and', 'or', 'not']
    # terms = [t for t in exp if t not in chars]
    # print(terms)
    # build_matrix(terms)

    res = unwrapper(exp)
    print(len(res), res)

if __name__ == '__main__':
    # expression = '((infection and patients) or effective)'    #input('give a logical query:')
    # boolean_expression(expression)
    query = 'How effective are inhalations of mucolytic agents in the treatment of CF patients'#input
    boolean_main(query)