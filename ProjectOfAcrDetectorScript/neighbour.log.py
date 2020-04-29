f=open("./data/neighbour.log").read().split("\n")
f.remove("")

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

OUT=open("./data/neighbour.log_1", "w")
for i in f:
    if "[]" not in i:
        nL=eval(i.split(":")[1])
        tmp=[]
        for j in nL:
            tmp.append(int(j.split("_")[-1]))
        if check_list(tmp):
            OUT.write(i+"\n")
OUT.close()



         


        
