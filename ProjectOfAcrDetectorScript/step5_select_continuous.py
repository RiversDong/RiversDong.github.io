import os
from Bio import SeqIO
import re
def getSkipID():
    cdsPath="./data/genome_cds/"
    files=os.listdir(cdsPath)
    chromosome2gene={}
    for i in files:
        records=SeqIO.parse(cdsPath+i, "fasta")
        for j in records:
            header=str(j.description)
            seq=str(j.seq)
            if len(seq)%3==0:
                if re.search("[^ATGC]",seq):
                    pass
                else:
                    header=header.split(" [")
                    seqID=header[0]
                    tmp_info=header[0].split("|")[1].split("_")
                    chromosome=tmp_info[0]
                    if chromosome not in chromosome2gene.keys():
                        chromosome2gene[chromosome]=[seqID]
                    else:
                        chromosome2gene[chromosome].append(seqID)
    skipIDs=[]
    chromosomes=chromosome2gene.keys()
    for i in chromosomes:
        i_range=range(0,len(chromosome2gene[i]),30)
        for j in i_range:
            skipIDs.append(chromosome2gene[i][j])
    return set(skipIDs)

skipIDs=getSkipID()

f=open("./data/feature.csv").read().split("\n")
acr=f[0:4132]
f=f[4132:]
f.remove("")
id2f={}
for i in f:
    i_info=i.split()
    i_id=i_info[1]
    id2f[i_id]=i
ids=set(id2f.keys())

def check_list(neighbour_index):
    neighbour_index.sort()
    n_range=range(1,len(neighbour_index))
    for i in n_range:
        latter=neighbour_index[i]
        former=neighbour_index[i-1]
        interval=latter-former
        if interval!=1:
            return False
    return True

f=open("./data/neighbour.log_1").read().split("\n")
f.remove("")
selected=[]
for i in f:
    i_info=i.split(":")
    i_key=i_info[0]
    i_index=i_key.split("_")[-1]
    neighbour_index=[int(i_index)]
    i_neighbour=eval(i_info[1])
    if i_neighbour:
        for j in i_neighbour:
            j_index=int(j.split("_")[-1])
            neighbour_index.append(j_index)
    if len(neighbour_index)!=1:
        if check_list(neighbour_index):
            selected.append(i_key)
            #print(i_key,neighbour_index)

for i in acr:
    print(i)
unions=set(selected) & ids
unions=list(unions & skipIDs)
for i in unions:
    print(id2f[i])




