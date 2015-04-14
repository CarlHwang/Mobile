#! /usr/bin/env python
# -*- coding:utf-8 -*-

# Auther: Carl Hwang
# Date: 2015-4-11

from sklearn.ensemble import RandomForestClassifier
from sklearn.externals import joblib
from Sampling.ReadDataset import ReadDataset

def FitRandomForest(num_negative_sample, date):
    train_data = ReadDataset(num_negative_sample, 'rf', date, level='2')
    forest = RandomForestClassifier(n_estimators = 500, oob_score=True, n_jobs=-1, max_features='auto')
    forest = forest.fit(train_data[0:, 1:], train_data[0:, 0])
    joblib.dump(forest, './PersistModel/rf_' + str(num_negative_sample) + '_' + date + '.model')
    