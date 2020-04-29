import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from joblib import dump
from xgboost import XGBClassifier
import sys

n_estimators=int(sys.argv[1])
max_depth=int(sys.argv[2])
min_samples_split=int(sys.argv[3])

benchmark=pd.read_csv("/storage/rd2/dc/AcrDetector/data/feature_new.csv",sep='\t')
#benchmark=pd.read_csv("tmp.feature","\t")

benchmark['label']=(benchmark['label']=="acr").astype(int)

X=benchmark[["codirection", "len_i5", "len", "len_i3", "function", "codon", "dev_i5", "dev", "dev_i3", "hth"]]

Y=benchmark['label']

X_train,y_train = X ,Y

# 最优参数传入随机森林
rf=RandomForestClassifier(random_state=0, n_estimators=n_estimators, max_depth=max_depth, min_samples_split=min_samples_split)
rf.fit(X_train, y_train)
dump(rf, '/storage/rd2/dc/AcrDetector/AcrDetector/modelHthDb/rf.joblib')

