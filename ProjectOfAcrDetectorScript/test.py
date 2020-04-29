def hth_anno():
    f=open("./data/domian_in_neighbour.tbl").read().split("\n")
    f=f[3:-11]
    query2accession={}
    for i in f:
        i_info=i.split()
        query=i_info[2]
        accession=i_info[1]
        if query not in query2accession.keys():
            query2accession[query]=[accession]
        else:
            query2accession[query].append(accession)
    geneWithHth=list(query2accession.keys())
    
    #f=open("./data/del").read().split("\n")
    f=open("./data/neighbour.log_1").read().split("\n")
    f.remove("")
    target2neighbour={}
    t2n={}
    for i in f:
        i_info=i.split(":")
        key=i_info[0]
        value=eval(i_info[1])
        tmp=[]
        for j in value:
            if j in geneWithHth:
                j_strand="dsadasdsa"
                tmp.append(j_strand)
        if tmp:
            target2neighbour[key]="1"
            t2n[key]=tmp
        else:
            target2neighbour[key]="0"
            t2n[key]=[]
    return target2neighbour, query2accession, t2n

hth_anno()
