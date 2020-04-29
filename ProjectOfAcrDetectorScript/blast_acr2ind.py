import os
ind=["./data/table2Protein/"+i for i in os.listdir("./data/table2Protein") if ".faa." not in i]

def makedb(ind):
    for i in ind:
        cmd="makeblastdb -in {0} -dbtype prot".format(i)
        os.system(cmd)

#makedb(ind)

def performBlast():
    for i in ind:
        out=os.path.basename(i).split(".")[0]
        cmd="blastp -query ./data/from_AcrFinder.fa -db {0} -outfmt 7 -out ./data/table2Protein/{1} -evalue 10e-3".format(i,out)
        #print(cmd)
        os.system(cmd)
#performBlast()

#ind=["./data/table2Protein/"+i for i in os.listdir("./data/table2Protein") if "." not in i]
#for i in ind:
#    f=open(i).read().split("\n")

#    for i in f:
#        if "#" not in i:




