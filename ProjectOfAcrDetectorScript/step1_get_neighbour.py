def neighbours():
    cdsPath="./data/genome_cds/"
    files=os.listdir(cdsPath)
    gene2chromosome={}
    gene2seq={}
    gene2strand={}
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
                    if "complement" in header:
                        strand="-"
                    else:
                        strand="+"
                    header=header.split(" [")
                    seqID=header[0]
                    tmp_info=header[0].split("|")[1].split("_")
                    chromosome=tmp_info[0]
                    gene2chromosome[seqID]=chromosome
                    gene2seq[seqID]=seq
                    gene2strand[seqID]=strand
                    if chromosome not in chromosome2gene.keys():
                        chromosome2gene[chromosome]=[seqID]
                    else:
                        chromosome2gene[chromosome].append(seqID)
    return gene2chromosome, chromosome2gene, gene2strand, gene2seq

if __name__=="__main__":
    import os
    from Bio import SeqIO
    import re
    from Bio.Seq import Seq
    from Bio.Alphabet import IUPAC
    benchmark=[]
    gene2chromosome, chromosome2gene, gene2strand, gene2seq = neighbours()
    neighbour_id2neighbour_seq={}
    p_records=SeqIO.parse("./data/benchmark_positive","fasta")
    for record in p_records:
        p_id=str(record.id)
        benchmark.append(p_id)
    
    negative_path="./data/negative/"
    neg_file=os.listdir(negative_path)
    for neg in neg_file:
        neg_path=negative_path+neg
        n_records=SeqIO.parse(neg_path, "fasta")
        for record in n_records:
            n_id=str(record.id)
            benchmark.append(n_id)

    LOG=open("./data/neighbour.log","w")
    for i in benchmark:
        if gene2strand[i]=="+":
            chromosome=gene2chromosome[i]
            genes=chromosome2gene[chromosome]
            i_index=genes.index(i)
            neighbour_index=i_index+1
            downstream_neighbours=genes[neighbour_index:neighbour_index+3]
            LOG.write(i+":{0}\n".format(str(downstream_neighbours)))
            for j in downstream_neighbours:
                neighbour_id2neighbour_seq[j]=gene2seq[j]
        else:
            chromosome=gene2chromosome[i]
            genes=chromosome2gene[chromosome]
            i_index=genes.index(i)
            neighbour_index=i_index-3
            if neighbour_index>=0:
                downstream_neighbours=genes[neighbour_index:i_index]
            else:
                downstream_neighbours=genes[0:i_index]
            LOG.write(i+":{0}\n".format(str(downstream_neighbours)))
            for j in downstream_neighbours:
                neighbour_id2neighbour_seq[j]=gene2seq[j]
    LOG.close()

    neighbour_ids=neighbour_id2neighbour_seq.keys()
    OUT=open("./data/neighbours.fa","w")
    for i in neighbour_ids:
        coding_dna=Seq(neighbour_id2neighbour_seq[i], IUPAC.unambiguous_dna)
        protein=str(coding_dna.translate()).replace("*","")
        OUT.write(">"+i+"\n"+protein+"\n")
    OUT.close()






