f=open("./data/benchmark_feature.csv").read().split("\n")
f.remove("")
OUT=open("./data/feature.csv","w")
header="\t".join(["label","g_id","chromosome","codirection","len_i5","len","len_i3","function","codon","dev_i5","dev","dev_i3","hth"])
OUT.write(header+"\n")
acr_func=["[protein=hypothetical protein]","[protein=Uncharacterised protein]","[protein=putative uncharacterized protein]"]
for i in f:
    i_info=i.split("\t")
    function=i_info[7]
    if function in acr_func:
        j=i.replace(function,"1")
    else:
        j=i.replace(function,"0")
    OUT.write(j+"\n")
OUT.close()

