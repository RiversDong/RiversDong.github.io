from joblib import load
import pandas as pd
from sklearn.metrics import accuracy_score, recall_score, precision_score, f1_score

rf = load('/storage/rd2/dc/AcrDetector/AcrDetector/modelHthDb/rf.joblib')

benchmark=pd.read_csv("./data/feature.csv",sep='\t')

benchmark['label']=(benchmark['label']=="acr").astype(int)

X=benchmark[["codirection", "len_i5", "len", "len_i3", "function", "codon", "dev_i5", "dev", "dev_i3", "hth"]]

Y=benchmark['label']

X_train,y_train = X ,Y

y_prediction = rf.predict(X_train)

acc=accuracy_score(y_train, y_prediction)
recall=recall_score(y_train, y_prediction)
precision=precision_score(y_train, y_prediction)
f=f1_score(y_train, y_prediction)

print(acc,recall,precision,f)

print("===========")

x=pd.crosstab(y_train, y_prediction,  rownames=['actual'], colnames=['preds'])
print(x)


