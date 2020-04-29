import os
files=["./AcrDetector/examples/"+i for i in os.listdir("./AcrDetector/examples/")]
def acrhomo(i):
    f="/storage/rd2/dc/AcrDetector/data/table2Protein/"+i
    f=open(f).read().split("\n")
    f.remove("")
    acrs=[]
    for i in f:
        if "#" not in i:
            acrs.append(i.split("\t")[1])
    return list(set(acrs))

def getRank(acr_id):
    f=open("re").read().split("\n")
    f.remove("")
    acr2rank={}
    rank_list=[]
    probability=[]
    for i in f:
        p_id="_".join(i.split()[0].split("_")[-3:-1])
        rank_list.append(p_id)
        probability.append(i.split()[1])
    for j in acr_id:
        try:
            j_index=rank_list.index(j)
            rank=j_index+1
            acr2rank[j]=str(rank)+"\t"+probability[j_index]
        except Exception as ret:
            print(j+"\t"+"None")
    return acr2rank

for i in files:
    cmd="python ./AcrDetector/AcrDetector.py -i {0} -o re".format(i)
    os.system(cmd)
    file_name=os.path.basename(i).split(".")[0]
    acrs=acrhomo(file_name)
    acr2rank=getRank(acrs)
    acrKeys=acr2rank.keys()
    for k in acrKeys:
        print(file_name+"\t"+k+"\t"+acr2rank[k])

