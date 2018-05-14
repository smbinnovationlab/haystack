import datetime
import logging
import pickle

import numpy as np
import pandas as pds
import xgboost as xgb
from sklearn.ensemble import AdaBoostClassifier, RandomForestClassifier
from sklearn.metrics import precision_score, make_scorer, accuracy_score
from sklearn.model_selection import GridSearchCV
from sklearn.naive_bayes import GaussianNB
from sklearn.svm import SVC
from sklearn.tree import DecisionTreeClassifier

from app import analyzer as config


def run(train, test, max_depth, n_estimators, learning_rate, estimator='XGBoost', cluster_label=None):
    estimator = estimator.upper()
    if estimator.startswith('X'):
        clf = xgb.XGBClassifier(max_depth=max_depth, n_estimators=n_estimators, learning_rate=learning_rate, eval_metric='auc')
    elif estimator.startswith('A') or estimator.startswith('B'):
        clf = AdaBoostClassifier(base_estimator=DecisionTreeClassifier(max_depth=max_depth), n_estimators=n_estimators, learning_rate=learning_rate)
    elif estimator.startswith('R'):
        clf = RandomForestClassifier(max_depth=max_depth, n_estimators=n_estimators)
    elif estimator.startswith('G'):
        clf = GaussianNB()
    elif estimator.startswith('S'):
        clf = SVC(probability=True)
    else:
        raise ValueError('Unrecognized Estimator')


    X = train[:, :-1] + 1
    y = train[:, -1].astype(int)
    clf.fit(X, y)

    X = test[:, :-1]
    y = test[:, -1].astype(int)

    # accuracy
    score = clf.score(X, y)
    # print(score)

    # cluster evaluation
    pred = clf.predict_proba(X)
    c_score = cluster_score(cluster_label, pred[:, 1], np.array(y), verbose=False)

    return score, c_score


def cv(train):
    params = {
        # "algorithm": ['SAMME', 'SAMME.R'],
        # "learning_rate": [1e-2, 1e-1, 1e1, 1e2, 1e2],
        # "n_estimators": [10, 30, 50, 80, 100, 200],
        # "criterion": ['gini', 'entropy'],
        # "max_depth": [4, 8, None],
        # "bootstrap": [True, False],

        # SVC test
        # "kernel": ['linear', 'rbf', 'sigmoid'],
        "kernel": ['poly'],
        "degree": [2, 3, 4],
        "tol": [1e-3, 1e-2, 1e-1],
        "C": [0.2, 0.05, 0.01],
    }
    scoring = {
        'prec': make_scorer(precision_score),
        'accuracy': make_scorer(accuracy_score)
    }
    s = SVC(probability=False)
    clf = GridSearchCV(s, params, verbose=10, n_jobs=8, scoring='f1')

    X = train[:, :-1]
    y = train[:, -1]

    # X = (X - X.mean(0)) / X.std(0)

    clf.fit(X, y)
    print(clf.cv_results_)
    str(clf.cv_results_)

    fname = 'tmp/model_cv_svc_f1.pkl'
    pickle.dump(clf.best_estimator_, open(fname, 'wb'))
    print('CV Results')
    print(clf.cv_results_)
    print('CV Best params')
    print(clf.best_params_)
    print('CV Best score')
    print(clf.best_score_)

    with open('cv.log', 'a') as f:
        f.write(str(datetime.datetime.now()))
        f.write('\n')
        f.write(str(type(s)))
        f.write('\n')
        f.write(fname)
        f.write('\n')
        f.write(str(clf.best_params_))
        f.write('\n')
        f.write(str(clf.best_score_))
        f.write('\n')
        f.write('\n')


def grid_search():
    PREFIX = '/Users/i342777/OneDrive - SAP SE/dataset/'
    train_df = pds.concat([pds.read_csv(PREFIX + 'anello.csv', usecols=config.FEATURE_COL_NAMES),
                           pds.read_csv(PREFIX + 'tent.csv', usecols=config.FEATURE_COL_NAMES),
                           pds.read_csv(PREFIX + 'training.csv', usecols=config.FEATURE_COL_NAMES),
                           pds.read_csv(PREFIX + 'globe.csv', usecols=config.FEATURE_COL_NAMES),
                           pds.read_csv(PREFIX + 'mint.csv', usecols=config.FEATURE_COL_NAMES),
                           pds.read_csv(PREFIX + 'contigo.csv', usecols=config.FEATURE_COL_NAMES),
                           ]).dropna()
    test_df = pds.read_csv(PREFIX + 'squeeze.csv', usecols=config.FEATURE_COL_NAMES).dropna()

    print('%d train %d positive' % (train_df.shape[0], np.count_nonzero(train_df['class'] == 1)))
    print('%d test %d positive' % (test_df.shape[0], np.count_nonzero(test_df['class'] == 1)))

    train = np.array(train_df[config.FEATURE_COL_NAMES]).astype(float)
    test = np.array(test_df[config.FEATURE_COL_NAMES]).astype(float)

    train[train == -1] = 1e4
    test[test == -1] = 1e4

    # mean, std = train.mean(0), train.std(0)
    # train[:, :-1] = ((train - mean) / std)[:, :-1]
    # test[:, :-1] = ((test - mean) / std)[:, :-1]

    # train_x, train_y = balanced_subset(train[:, :-1], train[:, -1])
    # print(train_x.shape)
    # train = np.concatenate((train_x, train_y.reshape((-1, 1))), 1)

    whole = np.concatenate((train, test))

    cv(whole)

    # for estimator in ['SVM']:
    #     records = []
    #     for md in [1]:
    #     # for md in range(1, 11, 2):
    #         for ne in [75]:
    #         # for ne in range(5, 100, 10):
    #             if estimator == 'RandomForest' or estimator == 'SVM':
    #                 r = [0]
    #             else:
    #                 # r = [0.01]
    #                 r = np.concatenate([np.arange(0.01, 0.09, 0.02), np.arange(0.1, 1.2, 1)])
    #             for lr in r:
    #                 score, c_score = run(train=train, test=test, max_depth=md, n_estimators=ne, learning_rate=lr, estimator=estimator, cluster_label=test_df['url'])
    #                 records.append((score, c_score, md, ne, lr))
    #
    #     from matplotlib import pyplot as plt
    #     records = np.array(records)
    #     plt.figure()
    #     plt.scatter(x=records[:, 0], y=records[:, 1], marker='o')
    #     for s, cs, md, ne, lr in records:
    #         r = np.random.rand(2) / 100                  # avoid string overlapping
    #         plt.annotate("%d,%d,%.2g" % (md, ne, lr), (s, cs) + r, size=3)
    #     plt.xlim((0, 1.1))
    #     plt.xlabel('Accuracy')
    #     plt.ylim((0, 1.1))
    #     plt.ylabel('Cluster score')
    #     plt.title(estimator)
    #     path = 'tmp/' + estimator + '.png'
    #     plt.savefig(path, dpi=1000)
    #     logging.info(path)
    #     plt.close()
    #     # plt.show()
    #



if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
    grid_search()
