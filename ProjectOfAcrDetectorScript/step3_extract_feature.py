def calculate_frequence(target_seq):
    '''
    This function is used to count the number of codon in protein coding genes
    '''
    code_l = re.findall(r'(\w\w\w)',str(target_seq))
    sum_num = len(code_l)
    CodonsDict = dict([('TTT', 0), ('TTC', 0), ('TTA', 0), ('TTG', 0), ('CTT', 0), ('CTC', 0), ('CTA', 0),
                     ('CTG', 0), ('ATT', 0), ('ATC', 0),
                     ('ATA', 0), ('ATG', 0), ('GTT', 0), ('GTC', 0), ('GTA', 0), ('GTG', 0), ('TAT', 0),
                     ('TAC', 0), ('TAA', 0), ('TAG', 0),
                     ('CAT', 0), ('CAC', 0), ('CAA', 0), ('CAG', 0), ('AAT', 0), ('AAC', 0), ('AAA', 0),
                     ('AAG', 0), ('GAT', 0), ('GAC', 0),
                     ('GAA', 0), ('GAG', 0), ('TCT', 0), ('TCC', 0), ('TCA', 0), ('TCG', 0), ('CCT', 0),
                     ('CCC', 0), ('CCA', 0), ('CCG', 0),
                     ('ACT', 0), ('ACC', 0), ('ACA', 0), ('ACG', 0), ('GCT', 0), ('GCC', 0), ('GCA', 0),
                     ('GCG', 0), ('TGT', 0), ('TGC', 0),
                     ('TGA', 0), ('TGG', 0), ('CGT', 0), ('CGC', 0), ('CGA', 0), ('CGG', 0), ('AGT', 0),
                     ('AGC', 0), ('AGA', 0), ('AGG', 0),
                     ('GGT', 0), ('GGC', 0), ('GGA', 0), ('GGG', 0)])
    for item in CodonsDict.keys():
        if item in code_l:
            CodonsDict[item] = code_l.count(item)
    tensor = []
    for i in sorted(CodonsDict.keys()):
        tensor.append(float('%.4f' % (CodonsDict[i]/float(sum_num))))
    return np.array(tensor)

def codon_distance(gene2seq):
    gene2distance={}
    proteins_in_genomes=gene2seq.keys()
    genome_cds1 = gene2seq.values()
    genome_cds="".join(genome_cds1)
    genome_codon=calculate_frequence(genome_cds)
    for i in proteins_in_genomes:
        i_codon=calculate_frequence(gene2seq[i])
        distance=np.linalg.norm(genome_codon-i_codon)
        gene2distance[i]=str(distance)
    return gene2distance

def function_len_codon():
    cdsPath="/storage/rd2/dc/AcrDetector/data/genome_cds/"
    files=os.listdir(cdsPath)
    #files=["GCA_003073895.1_ASM307389v1_cds_from_genomic.fna"]
    for i in files:
        records=SeqIO.parse(cdsPath+i, "fasta")
        gene2seq={}
        for j in records:
            header=str(j.description)
            tmp_header=header
            seq=str(j.seq)
            if len(seq)%3==0:
                if re.search("[^ATGC]",seq):
                    pass
                else:
                    if "complement" in header:
                        strand="-"
                    else:
                        strand="+"
                    header=header.split(" [")
                    seqID=header[0]
                    tmp_info=header[0].split("|")[1].split("_")
                    chromosome=tmp_info[0]
                    protein=seqID
                    if "[protein=" in tmp_header:
                        proteinFunc=re.search(r"\[protein=.*\]*?",tmp_header)
                        proteinFunc=proteinFunc.group(0).split(" [")[0]
                    else:
                        proteinFunc="unknown"
                    gene2chromosome[protein]=chromosome
                    gene2seq[protein]=seq
                    gene2function[protein]=proteinFunc
                    gene2genLen[protein]=str(len(seq))
                    gene2strand[protein]=strand
                    if chromosome not in chromosome2gene.keys():
                        chromosome2gene[chromosome]=[protein]
                    else:
                        chromosome2gene[chromosome].append(protein)
        gene2distance=codon_distance(gene2seq)
        gene2codon.update(gene2distance)

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
                j_strand=gene2strand[j]
                tmp.append(j_strand)
        if tmp:
            target2neighbour[key]="1"
            t2n[key]=tmp
        else:
            target2neighbour[key]="0"
            t2n[key]=[]
    return target2neighbour, query2accession, t2n

def deviation():
    cds_path="./data/genome_cds/"
    files=os.listdir(cds_path)
    #files=["GCA_003073895.1_ASM307389v1_cds_from_genomic.fna" ]
    gene2deviation={}
    for i in files:
        id2seq={}
        file_path=cds_path+i
        records=SeqIO.parse(file_path, "fasta")
        for j in records:
            seqID=str(j.id)
            seq=str(j.seq)
            if len(seq)%3==0:
                id2seq[seqID]=seq
        gene2distance=codon_distance(id2seq)
        genes=gene2distance.keys()
        geneLen=len(genes)-1
        for k in genes:
            large_num=0
            for L in genes:
                if gene2distance[k]>gene2distance[L]:
                    large_num=large_num+1
            deviation=large_num/geneLen
            gene2deviation[k]=str(deviation)
    return gene2deviation

def getFeature(sampleID):
    samples2f={}
    possible_hth=query2accession.keys()
    for i in sampleID:
        chromosome=gene2chromosome[i]
        chrGenes=chromosome2gene[chromosome]
        i_index=chrGenes.index(i)
        chrGenesNum=len(chrGenes)-1
        strand_i=gene2strand[i]
        if i_index==0:
            i5=chrGenes[i_index+1]
            i3=chrGenes[i_index+2]
        elif i_index==chrGenesNum:
            i5=chrGenes[i_index-1]
            i3=chrGenes[i_index-2]
        else:
            i5=chrGenes[i_index-1]
            i3=chrGenes[i_index+1]
        dev_i5=gene2deviation[i5]
        dev_i3=gene2deviation[i3]
        len_i5=gene2genLen[i5]
        len_i3=gene2genLen[i3]
        if strand_i == gene2strand[i5] or strand_i == gene2strand[i3]:
            codirection="1"
        else:
            codirection="0"
        if target2neighbour[i]=="1":
            if strand_i in t2n[i]:
                hth_direction="1"
            else:
                hth_direction="0"
        else:
            hth_direction="-1"

        feature=[gene2chromosome[i], codirection, len_i5, gene2genLen[i], len_i3, gene2function[i],\
                gene2codon[i],dev_i5,gene2deviation[i],dev_i3,target2neighbour[i],hth_direction]
        samples2f[i]=feature
    return samples2f

if __name__ == "__main__":
    from Bio import SeqIO
    import os
    import re
    import numpy as np

    gene2function={}
    gene2genLen={}
    gene2codon={}
    chromosome2gene={}
    gene2strand={}
    gene2chromosome={}
    function_len_codon()
    gene2deviation=deviation()
    target2neighbour, query2accession, t2n = hth_anno()
    selected_samples=list(target2neighbour.keys())

    positive_records=SeqIO.parse("./data/benchmark_positive","fasta")
    POSITIVE=[]
    for record in positive_records:
        p_id=str(record.id)
        POSITIVE.append(p_id)
    POSITIVE_union=list(set(POSITIVE).intersection(set(selected_samples)))
    #POSITIVE_union=["lcl|CP029097.1_cds_AWE96846.1_1393","lcl|CP029097.1_cds_AWF02691.1_5650"]
    p2f=getFeature(POSITIVE_union)

    negative_path="./data/negative/"
    neg_file=os.listdir(negative_path)
    NEGATIVE=[]
    for neg in neg_file:
        neg_path=negative_path+neg
        negative_records=SeqIO.parse(neg_path,"fasta")
        for record in negative_records:
            n_id=str(record.id)
            NEGATIVE.append(n_id)
    NEGATIVE_union=list(set(NEGATIVE).intersection(set(selected_samples)))
    #NEGATIVE_union=["lcl|CP029097.1_cds_AWE96846.1_1393","lcl|CP029097.1_cds_AWE98455.1_3370"]
    n2f=getFeature(NEGATIVE_union)

    OUT=open("./data/benchmark_feature.csv","w")
    for i in POSITIVE_union:
        OUT.write("acr\t"+i+"\t"+ "\t".join(p2f[i])+"\n")
    for i in NEGATIVE_union:
        OUT.write("nonacr\t"+i+"\t"+"\t".join(n2f[i])+"\n")
    OUT.close()







