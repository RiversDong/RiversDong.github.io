import os

# hmmscan search sequence against profile database
# hmmscan takes as input a query file containing one or more sequences
# hmmpress prepare profile database for hmmscan

def build_db():
    hmmpress_cmd="hmmpress ./data/hthpfam"
    os.system(hmmpress_cmd)

def search_hth():
    # the last one is query
    hmmscan_cmd="hmmscan -o ./data/domian_in_neighbour --tblout ./data/domian_in_neighbour.tbl --noali -E 1e-5 ./data/hthpfam ./data/neighbours.fa"
    os.system(hmmscan_cmd)

if __name__ == "__main__":
    build_db()
    search_hth()
