import os
f=open("./data/calculate_distance.distance").read().split("\n")
assembly178=[]
assembly2Acrs={}
for i in f:
    i_info=i.split("\t")
    assembly=i_info[0].split("_")[0:3]
    assembly="_".join(assembly)
    assembly178.append(assembly)
    assembly2Acrs[assembly]=i_info[1].split(",")

from Bio import SeqIO

def readCds(Infile):
    records=SeqIO.parse(Infile,"fasta")
    accession2id={}
    id_list=[]
    for i in records:
        i_id=str(i.id)
        i_accession=i_id.split("_")[-2]
        accession2id[i_accession]=i_id
        id_list.append(i_id)
    return accession2id, set(id_list)

def read_feature_new():
    f=open("./data/feature_new.csv").read().split("\n")
    f.remove("")
    label=f[0]
    data=f[1:]
    id2record={}
    for i in data:
        id2record[i.split()[1]]=i
        #print(i,i.split()[1])
    return label,id2record
label,id2record=read_feature_new()
idInfeature=set(id2record.keys())

def getRank(acr_id):
    f=open("re").read().split("\n")
    f.remove("")
    acr2rank={}
    rank_list=[]
    probability=[]
    for i in f:
        rank_list.append(i.split()[0])
        probability.append(i.split()[1])
    for j in acr_id:
        try:
            j_index=rank_list.index(j)
            rank=j_index+1
            acr2rank[j]=str(rank)+"\t"+probability[j_index]
        except Exception as ret:
            print(j)
    return acr2rank

p="/storage/rd2/dc/AcrDetector/data/genome_cds/"
allCdsFiles=os.listdir(p)
for i in assembly178:
    cds=i+"_cds_from_genomic.fna"
    if cds in allCdsFiles:
        OUT=open("tmp.feature","w")
        OUT.write(label+"\n")
        cdsFile=p+cds
        accession2id, id_list=readCds(cdsFile)
        acrs=assembly2Acrs[i]
        acrs_id=[accession2id[j] for j in acrs]
        afterRemove=idInfeature.difference(id_list)
        afterRemove=list(afterRemove)
        afterRemove.sort()
        for remain in afterRemove:
            OUT.write(id2record[remain]+"\n")
        OUT.close()
        cmd="python step8_saveModel.py 50 19 50"
        os.system(cmd)
        cmd="python ./AcrDetector/AcrDetector.py -i {0} -o re".format(cdsFile)
        os.system(cmd)
        acr2rank=getRank(acrs_id)
        acrKeys=acr2rank.keys()
        for k in acrKeys:
            print(cds+"\t"+k+"\t"+acr2rank[k])


