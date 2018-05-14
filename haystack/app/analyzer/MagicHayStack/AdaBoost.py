from numpy import *
#import numpy as np
import pandas as pds
from sklearn.ensemble import *
from sklearn.tree import DecisionTreeClassifier
from sklearn.externals import joblib
from matplotlib import pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

def loadDataSet(filename):      #general function to parse tab -delimited floats
    df = pds.read_csv(filename,encoding='utf-8')
    x_cols = list(df.columns)
    cluster_m = df[x_cols[0]]
    text_m = df[x_cols[-1]]
    x_cols.remove('url')
    x_cols.remove('text')
    y_m = df[x_cols[-1]]
    x_cols.remove('class')
    X_m = df[x_cols]
    return cluster_m,text_m,X_m,y_m

def param_det():
    training_fn = 'C:\\Users\i344862\Desktop\HayStack\data\\training_dist.csv'
    train_cluster, train_text, train_x, train_y = loadDataSet(training_fn)
    testing_fn = 'C:\\Users\i344862\Desktop\HayStack\data\\testing.csv'
    test_cluster, test_text, test_x, test_y = loadDataSet(testing_fn)
    test_cluster = array(test_cluster)
    test_y = array(test_y)
    c = set(test_cluster)
    # f_beta = []; pre = []; rec = [];
    n_est = [];    l_rate = [];    s = [];  cluster_precision = []
    for n_estimators in range(4, 13):
        for learning_rate in [0.01, 0.03, 0.09, 0.3, 0.9, 3, 9]:
            print("--------------%f,%f--------------" % (n_estimators, learning_rate))
            clf = AdaBoostClassifier(base_estimator=DecisionTreeClassifier(max_depth = 1), n_estimators=n_estimators, learning_rate=learning_rate)
            clf.fit(train_x, train_y)
            prob = clf.predict_proba(test_x)
            #print(shape(prob))
            cluster_p = 0
            prob_1 = prob[:, 1]
            #print(shape(prob_1))
            for cluster in c:
                p = prob_1[nonzero(test_cluster == cluster)]
                y = test_y[nonzero(test_cluster == cluster)]
                max_index_list = where(p == max(p))[0]
                # print(p[max_index_list])
                for i in range(max_index_list.size):
                    max_index = max_index_list[i]
                    if y[max_index] == 1:
                        cluster_p += 1
                        #print(max_index, p[max_index])
                        break
            cluster_precision.append(float(cluster_p) / len(c))
            score = clf.score(test_x, test_y)
            s.append(score)
            print(score, float(cluster_p) / len(c))
            # print(shape(predict)[0])
            # for i in range(shape(predict)[0]):
            #     if test_y[i] == 1 and predict[i] == 1: tp += 1
            #     elif test_y[i] == 1 and predict[i] == 0: tn += 1
            #     elif test_y[i] == 0 and predict[i] == 1: fp += 1
            #     else: fn += 1
            # if tp+fp == 0: precision = 0
            # else: precision = float(tp)/(tp+fp)
            # if tp+fn == 0: recall = 0
            # else: recall = float(tp)/(tp+fn)
            # beta = 1
            # if (beta**2*precision+recall) == 0: f = 0
            # else: f = float(beta**2+1)*precision*recall/(beta**2*precision+recall)
            # f_beta.append(f)
            n_est.append(n_estimators)
            l_rate.append(learning_rate)
            # pre.append(precision)
            # rec.append(recall)

    print("drawing")
    #print(f_beta)
    fig = plt.figure()
    ax = Axes3D(fig)
    # n_est, l_rate = np.meshgrid(n_est, l_rate)
    # ax.plot_surface(n_est, l_rate, s, rstride=1, cstride=1, cmap='rainbow')
    ax.scatter(n_est, l_rate, s)
    ax.scatter(n_est, l_rate, cluster_precision, c='orange')
    # ax.scatter(n_est, l_rate, rec)
    ax.set_zlabel('score')  # 坐标轴
    ax.set_ylabel('l_rate')
    ax.set_xlabel('n_est')
    plt.show()
    print("end")

param_det()

# '''
# (6,5)  (7,4)  (9.5)  (11.5)
# '''
'''train'''
training_fn = 'C:\\Users\i344862\Desktop\HayStack\data\\training_dist.csv'
train_cluster,train_text,train_x,train_y = loadDataSet(training_fn)
clf = AdaBoostClassifier(base_estimator=DecisionTreeClassifier(max_depth = 1), n_estimators=9, learning_rate=0.09)
clf.fit(train_x, train_y)
import os
magic_haystack = os.path.dirname(os.path.abspath("AdaBoost.py"))
joblib.dump(clf, os.path.join(magic_haystack, 'tmp/model.pkl'))
#
# '''test'''
# testing_fn = 'C:\\Users\i344862\Desktop\HayStack\data\\testing_dist.csv'
# test_cluster,test_text,test_x,test_y = loadDataSet(testing_fn)
# clf1 = joblib.load('rf.pkl')
#
# total_1 = 0.0
# test_1 = 0.0
# predict = clf1.predict(test_x)
# score = clf1.score(test_x,test_y)
# prob = clf1.predict_proba(test_x)
# #print(shape(predict)[0])
# for i in range(shape(predict)[0]):
#     if test_y[i] == 1: total_1 += 1
#     if test_y[i] == 1 and test_y[i] == predict[i]: test_1 += 1
# print('precision: %f' % float(float(test_1)/float(total_1)))
# print('score: %f'%score)
# print('----------------predict-------------------')
# print(predict)
# print(mat(test_y))
# print('----------------confidence-------------------')
# print(prob)
# print('----------------feature_importances-------------------')
# print(clf1.feature_importances_)

