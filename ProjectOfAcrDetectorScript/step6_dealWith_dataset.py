from imblearn.under_sampling import ClusterCentroids
import pandas as pd
import numpy as np

benchmark=pd.read_csv("./data/feature_new.csv",sep='\t')
benchmark['label']=(benchmark['label']=="acr").astype(int)
X=benchmark[["len", "function", "codon", "dev", "hth"]]
y=benchmark['label']

cc = ClusterCentroids(sampling_strategy={0:25158},n_jobs=1,random_state=0)

X_smt, y_smt = cc.fit_sample(X, y)

new_benchmark=pd.concat([y_smt,X_smt],axis=1)
new_benchmark.to_csv("./data/feature_CC.csv",sep="\t",index=False)
