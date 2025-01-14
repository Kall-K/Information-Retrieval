import os, json
import boolean, vsm
from timeit import default_timer as timer

PATH = os.getcwd() + "\\collection\\docs"


def experiment(queries, num_r):
    boolean_res = []
    vsm_res = []

    for q, size in zip(queries, num_r):

        start = timer()
        docs = boolean.boolean_main(q)
        end = timer()
        boolean_res.append({
            'docs': docs,
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
    pr = []
    for res,rel in zip(result,relevant):
        pr.append(len([doc for doc in res['docs'] if int(doc) in rel])/len(res['docs']))

    return pr

def recall(result, relevant):
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
        boolean_res[i].update({'precision': pr_boolean[i], 'recall': rc_boolean[i], '#docs': len(boolean_res[i]['docs'])})
        vsm_res[i].update({'precision': pr_vsm[i], 'recall': rc_vsm[i], '#docs': len(vsm_res[i]['docs'])})

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
              Num Docs: {boolean_res[i]['#docs']}  {vsm_res[i]['#docs']} \n \
              5-top Docs: {boolean_res[i]['docs'][:5]}  {vsm_res[i]['docs'][:5]} \n')
    f.close()

if __name__ == '__main__':
    metrics_main()
    print("Results have been generated. You can find them in the following files:")
    print("- Metrics: Metrics.txt")
    print("- Boolean Retrieved docs: Boolean_Results.json")
    print("- VSM Retrieved docs: VSM_Results.json")