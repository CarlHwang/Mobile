#! /usr/bin/env python
# -*- coding:utf-8 -*-

# Auther: Carl Hwang
# Date: 2015-4-13

import csv
from Sampling.ReadDataset import ReadPredictDataset
from sklearn.externals import joblib


'''Logistic Regression'''

def LRSinglePredict(num_negative_sample, date, top_k = 600):
    test_data, id_set = ReadPredictDataset(isWithID=True)
    lr = joblib.load('./PersistModel/lr_' + str(num_negative_sample) + '_' + date + '.model')
    result = lr.predict_proba(test_data)
    
    predict = {}
    for i in range(len(id_set)):
        user_id = id_set[i][0]
        item_id = id_set[i][1]
                
        prob = result[i][1]
        
        key = user_id + ' ' + item_id
        predict[key] = prob

    import operator
    sorted_predict = sorted(predict.iteritems(), key=operator.itemgetter(1), reverse=True)  
    sorted_predict = sorted_predict[:top_k]
    
    # 输出的文件头
    outfile = open('../predict/tianchi_mobile_recommendation_predict.csv', 'wb')
    spamwriter = csv.writer(outfile, dialect = 'excel')
    spamwriter.writerow(['user_id', 'item_id'])
    
    for row in sorted_predict:
        key = row[0]
        user_id = key.split()[0]
        item_id = key.split()[1]
        spamwriter.writerow([user_id, item_id])
    

def LRAvgPredict(date):
    num_negative_samples = [10000,10001,12000,12001,14000,16000,18000,20000]
    avg_row = []
    
    #
    test_data, id_set = ReadPredictDataset(isWithID=True)
    for i in range(len(num_negative_samples)):
        lr = joblib.load('./PersistModel/lr_' + str(num_negative_samples[i]) + '_' + date + '.model')
        result = lr.predict_proba(test_data)
        avg_row.append(result[:,1])
        
            
    avg = []
    for i in range(len(avg_row[0])):
        feature = []
        for j in range(len(avg_row)):
            feature.append(avg_row[j][i]) 
        avg.append(sum(feature)/len(feature))
    
    
    outfile = open('../csv/testingset/lr_predict_avg_result.csv', 'wb')
    spamwriter = csv.writer(outfile, dialect = 'excel')
    
    for i in range(len(id_set)):
        user_id = id_set[i][0]
        item_id = id_set[i][1]
        spamwriter.writerow([user_id, item_id, avg[i]])


'''Random Forest'''
def RFSinglePredict(num_negative_sample, date, top_k = 600):
    test_data, id_set = ReadPredictDataset(isWithID=True)
    rf = joblib.load('./PersistModel/rf_' + str(num_negative_sample) + '_' + date + '.model')
    result = rf.predict_proba(test_data)
    
    predict = {}
    for i in range(len(id_set)):
        user_id = id_set[i][0]
        item_id = id_set[i][1]
        prob = result[i][1]
        
        key = user_id + ' ' + item_id
        predict[key] = prob

    import operator
    sorted_predict = sorted(predict.iteritems(), key=operator.itemgetter(1), reverse=True)  
    sorted_predict = sorted_predict[:top_k]
    
    # 输出的文件头
    outfile = open('../predict/tianchi_mobile_recommendation_predict.csv', 'wb')
    spamwriter = csv.writer(outfile, dialect = 'excel')
    spamwriter.writerow(['user_id', 'item_id'])
    
    for row in sorted_predict:
        key = row[0]
        user_id = key.split()[0]
        item_id = key.split()[1]
        spamwriter.writerow([user_id, item_id])
        

def RFAvgPredict(date):
    num_negative_samples = [10000,10001,12000,12001,14000,16000,18000,20000]
    avg_row = []
    
    #
    test_data, id_set = ReadPredictDataset(isWithID=True)
    for i in range(len(num_negative_samples)):
        rf = joblib.load('./PersistModel/rf_' + str(num_negative_samples[i]) + '_' + date + '.model')
        result = rf.predict_proba(test_data)
        avg_row.append(result[:,1])
        
            
    avg = []
    for i in range(len(avg_row[0])):
        feature = []
        for j in range(len(avg_row)):
            feature.append(avg_row[j][i]) 
        avg.append(sum(feature)/len(feature))
    
    
    outfile = open('../csv/testingset/rf_predict_avg_result.csv', 'wb')
    spamwriter = csv.writer(outfile, dialect = 'excel')
    
    for i in range(len(id_set)):
        user_id = id_set[i][0]
        item_id = id_set[i][1]
        spamwriter.writerow([user_id, item_id, avg[i]])
    
