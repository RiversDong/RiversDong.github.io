if __name__ == "__main__":
    from sklearn.model_selection import GridSearchCV,train_test_split, StratifiedKFold
    from sklearn.metrics import make_scorer, accuracy_score, recall_score, precision_score, f1_score
    from sklearn.ensemble import RandomForestClassifier
    import pandas as pd
    import numpy as np
    import sys

    test=pd.read_csv("./data/feature_new.csv",sep='\t')
    test['label']=(test['label']=="acr").astype(int)

    X=test[["codirection", "len_i5", "len", "len_i3", "function", "codon", "dev_i5", "dev", "dev_i3", "hth"]]
    Y=test['label']
    X_train,y_train = X ,Y
    random_seed=int(sys.argv[1])
    rf=RandomForestClassifier(random_state=random_seed)
    parameters = {'n_estimators':(50,),'max_depth':(19,),'min_samples_split':(50,)}
    kflod = StratifiedKFold(n_splits=5,random_state=random_seed,shuffle=True)
    scoring = {'Accuracy':make_scorer(accuracy_score), 'Recall':make_scorer(recall_score), 'Precision':make_scorer(precision_score), "F1":make_scorer(f1_score)}
    grid = GridSearchCV(rf,parameters, scoring=scoring, refit='F1', cv=kflod.split(X_train,y_train), n_jobs=10)
    grid.fit(X_train,y_train)
    # grid.best_index_
    # grid.best_estimator_
    # grid.best_score_
    # grid.best_params_
    # cv_results_ 会返回一个字典
    results=grid.cv_results_
    accs=results["mean_test_Accuracy"]
    acc_std=results["std_test_Accuracy"]

    recalls=results["mean_test_Recall"]
    recall_std=results["std_test_Recall"]

    precisions=results["mean_test_Precision"]
    precision_std=results["std_test_Precision"]

    f1_score=results["mean_test_F1"]
    f1_score_std=results["std_test_F1"]

    index_range=range(0, len(accs))
    for i in index_range:
        acc=str(round(accs[i],4))
        recall=str(round(recalls[i],4))
        precision=str(round(precisions[i],4))
        f1=str(round(f1_score[i],4))
        info=["random_"+str(random_seed),acc,recall,precision,f1]
        print("\t".join(info))









