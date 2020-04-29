if __name__ == "__main__":

	# GridSearchCV 进行网格搜索确定最优参数
	# train_test_split 划分数据集为进行网格搜索的样本和用来进行测试的样本
	# KFold 用来划分样本，包含划分样本的分数和每一份里面具体的样本是谁
	# KFold和StratifiedKFold的区别StratifiedKFold是分层采样  在交叉验证过程中每一份正负样本与benchmark比例相同
	from sklearn.model_selection import GridSearchCV,train_test_split, StratifiedKFold

	# 指定交叉验证时的评价指标
	# 我额外导入其它几个评价指标，最后一起输出
	from sklearn.metrics import make_scorer, accuracy_score, recall_score, precision_score, f1_score

	# 导入随机森林分类器
	from sklearn.ensemble import RandomForestClassifier

	#处理警告信息
	import pandas as pd
	import numpy as np

	test=pd.read_csv("./data/feature_new.csv",sep='\t')
	test['label']=(test['label']=="acr").astype(int)

	X=test[["codirection", "len_i5", "len", "len_i3", "function", "codon", "dev_i5", "dev", "dev_i3", "hth"]]
	Y=test['label']

	# X: data and y: lable. data type is array
	X_train,y_train = X ,Y


	# 随机深林引入
	# oob_score 即是否采用袋外样本来评估模型的好坏 默认是false默认识False。 （重要）
	# n_estimators 随机森林中决策树的数目
	# max_features RF 划分时考虑的最大特征数，默认是auto （重要）
	# max_depth 决策树最大深度 （重要）
	# min_samples_split 内部节点再划分所需最小样本数，这个值限制了子树继续划分的条件 （重要）
	# min_samples_leaf  叶子节点最少样本数 （重要）
	# max_leaf_nodes通过限制最大叶子节点数，可以防止过拟合，默认是"None”，即不限制最大的叶子节点数
	# min_impurity_split 节点划分最小不纯度
	# random_state 设置固定的随机种子
	rf=RandomForestClassifier(random_state=0)

	# 指定随机森林的参数字典，基于此参数进行网格搜索确定最优的参数 
	# 确认随机森林哪些参数需要优化
	parameters = {'n_estimators':range(50,101,10),'max_depth':range(3,20,2),'min_samples_split':range(50,301,20)}


	# 分割数据集为5份。每一份测试，剩下的10份进行训练
	# sfolder = StratifiedKFold(n_splits=4,random_state=0,shuffle=False)
	# rain, test in sfolder.split(X,y)
	# random_state 和 shuffle=True一起使用才有意义，shuffle=True random_state去不同的值才能随机起来 不一样
	kflod = StratifiedKFold(n_splits=5, random_state=0, shuffle=True)

	# f1 Scoring Classification
	scoring = {'Accuracy':make_scorer(accuracy_score), 'Recall':make_scorer(recall_score), 'Precision':make_scorer(precision_score), "F1":make_scorer(f1_score)}

	# scoring中指定的参数进行了优化，只选择
	# 对比GridSearchCV和cross_validate的区别
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

	params=results["params"]

	OUT=open("cv.res", "w")
	index_range=range(0, len(accs))
	for i in index_range:
		tree_number=str(params[i]["n_estimators"])
		depth=str(params[i]["max_depth"])
		min_samples_split=str(params[i]["min_samples_split"])
		acc=str(round(accs[i],4))
		recall=str(round(recalls[i],4))
		precision=str(round(precisions[i],4))
		f1=str(round(f1_score[i],4))
		info=["{0}:{1}:{2}".format(tree_number,depth,min_samples_split),acc,recall,precision,f1]
		#info=["{0}:{1}".format(depth,min_samples_split),acc,recall,precision,f1]
		OUT.write("\t".join(info)+"\n")
	OUT.close()


