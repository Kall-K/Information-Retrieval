import os, json
import boolean, vsm
from timeit import default_timer as timer
import matplotlib.pyplot as plt
import numpy as np


PATH = os.getcwd() + "\\collection\\docs"


def experiment(queries, num_r):
    boolean_res = []
    vsm_res = []

    for q, size in zip(queries, num_r):

        start = timer()
        docs = boolean.boolean_main(q)
        end = timer()
        boolean_res.append({
            'docs': docs, #
            'time': end-start #sec
        })
        
        start = timer()
        docs = vsm.vsm_main(q)
        end = timer()
        vsm_res.append({
            'docs': docs, 
            'time': end-start
        })

    return boolean_res, vsm_res

def precision(result, relevant):
#posa apo ta eggrafa pou anaktithikan einai sxetika me to erotima
    pr = []
    for res,rel in zip(result,relevant):
        pr.append(len([doc for doc in res['docs'] if int(doc) in rel])/len(res['docs']))

    return pr

def recall(result, relevant):
#posa apo ta sxetika eggrafa anaktithikan sinolika
    rc = []
    for res,rel in zip(result,relevant):
        rc.append(len([doc for doc in res['docs'] if int(doc) in rel])/len(rel))

    return rc

def metrics_main():
    queries = open(os.getcwd()+'\\collection\\Queries.txt', 'r')
    text = queries.read()
    queries = text.split("\n")
    # queries = queries[:5]
    relevant = open(os.getcwd()+'\\collection\\Relevant.txt', 'r')
    text = relevant.read()
    relevant = text.split("\n")
    # relevant = relevant[:5]

    existing_docs =  [int(d) for d in os.listdir(PATH)]

    num_r = []
    relevant_new = []
    for rel in relevant:
        temp = [int(r) for r in rel.split() if int(r) in existing_docs] 
        num_r.append(len(temp))
        relevant_new.append(temp)

    boolean_res, vsm_res = experiment(queries, num_r)


    pr_boolean = precision(boolean_res,relevant_new)
    pr_vsm = precision(vsm_res, relevant_new)

    rc_boolean = recall(boolean_res,relevant_new)
    rc_vsm = recall(vsm_res, relevant_new)
    
    for i in range(len(queries)):
        boolean_res[i].update({'precision': pr_boolean[i], 'recall': rc_boolean[i]})
        vsm_res[i].update({'precision': pr_vsm[i], 'recall': rc_vsm[i]})

    for b,s in zip(boolean_res, vsm_res):
        b['docs'] = len(b['docs'])
        s['docs'] = len(s['docs'])

    with open("Boolean_Results.json", "w") as outfile: 
        json.dump(boolean_res, outfile)
    with open("VSM_Results.json", "w") as outfile: 
        json.dump(boolean_res, outfile)
        
    f = open("Metrics.txt", "w")    
    f.write('Boolean Model vs VSM Model \n')
    for i in range(len(queries)):
        f.write(f'-> Question{i+1} \n \
              time: {boolean_res[i]['time']}  {vsm_res[i]['time']} \n \
              precision: {boolean_res[i]['precision']}  {vsm_res[i]['precision']} \n \
              recall: {boolean_res[i]['recall']}  {vsm_res[i]['recall']} \n \
              Num Docs: {boolean_res[i]['docs']}  {vsm_res[i]['docs']} \n ')
    f.close()
    # ir_model = ['boolean', 'vsm']
    # plt.figure("Precision Results")
    # x_axis = np.arange(len(ir_model))
    # plt.bar(x_axis-0.2,precision(boolean_res,relevant_new),0.4,label = 'boolean model')
    # plt.bar(x_axis+0.2,precision(vsm_res, relevant_new),0.4,label = 'vsm model')
    # plt.xticks(x_axis,ir_model)
    # plt.xlabel("Models")
    # plt.ylabel("Precision")
    # plt.legend()
    # plt.savefig('Precision.png')
    # plt.close()

if __name__ == '__main__':
    metrics_main()