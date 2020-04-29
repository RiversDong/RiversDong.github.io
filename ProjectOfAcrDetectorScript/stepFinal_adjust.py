import os
p="/storage/rd2/dc/AcrDetector/AcrDetector/examples/"

acr={"GCF_000438685.2.fna":"lcl|NC_021826.1_cds_WP_003731276.1_1445",\
        "GCF_001188875.1.fna":"lcl|NZ_CP009676.1_cds_WP_128382896.1_1347",\
        "GCF_001235745.1.fna":"lcl|NZ_CUEW01000002.1_cds_WP_053038109.1_172",\
        "GCF_002369615.1.fna":"lcl|NZ_MWUW01000002.1_cds_WP_142302263.1_855",\
        "GCF_001583095.1.fna":"lcl|NZ_LUEQ01000011.1_cds_WP_061665674.1_2984",\
        "GCF_002163735.1.fna":"lcl|NZ_CP015885.1_cds_WP_002401839.1_2907",\
        "GCF_002735835.1.fna":"lcl|NZ_PEBM01000063.1_cds_WP_099390844.1_1977",\
        "GCF_003042995.1.fna":"lcl|NZ_PZGO01000018.1_cds_WP_107591702.1_2028",\
        "GCA_001855735.1.fna":"lcl|MNAC01000021.1_cds_OHX26873.1_930",\
        "GCF_000196055.1.fna":"lcl|NC_004368.1_cds_WP_000384271.1_216"}
cdsfiles=acr.keys()
params=["50_19_50","70_19_50","80_19_50","90_19_50","60_19_50","100_19_50","90_17_50","100_17_50",\
        "50_17_50","60_17_50","70_17_50","80_17_50","90_15_50","100_15_50"]
#params=["50_19_50"]

def getRank(acr_id):
    f=open("re").read().split("\n")
    f.remove("")
    rank_list=[]
    for i in f:
        rank_list.append(i.split()[0])
    rank=rank_list.index(acr_id)+1
    return rank

print("\t".join(cdsfiles))
for param in params:
    param_info=param.split("_")
    n_estimators=param_info[0]
    max_depth=param_info[1]
    min_samples_split=param_info[2]
    os.system("python step8_saveModel.py {0} {1} {2}".format(n_estimators, max_depth, min_samples_split))
    rank_list=[]
    for i in cdsfiles:
        infile=p+i
        cmd="python ./AcrDetector/AcrDetector.py -i {0} -o re".format(infile)
        os.system(cmd)
        acr_id=acr[i]
        try:
            rank=getRank(acr_id)
            rank_list.append(rank)
        except Exception:
            rank_list.append("NA")
    rank_list=map(str, rank_list)
    rank_list="\t".join(rank_list)
    print(param+"\t"+rank_list)


