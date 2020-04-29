import os
f=open("./data/table2_link.txt").read().split("\n")
for i in f:
    link=i+"/"+i.split("/")[-1]+"_protein.faa.gz"
    #print(link)
    cmd="wget {0} -P ./data/table2Protein".format(link)
    os.system(cmd)
