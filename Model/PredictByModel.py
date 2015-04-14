#! /usr/bin/env python
# -*- coding:utf-8 -*-

# Auther: Carl Hwang
# Date: 2015-4-13

import csv
from Sampling.ReadDataset import ReadPredictDataset
from sklearn.externals import joblib


'''Logistic Regression'''

def LRSinglePredict(num_negative_sample, date, top_k = 650, hours=24):
    test_data, id_set = ReadPredictDataset(hours, isWithID=True)
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
    

def LRAvgPredict(date,top_k=650, hours=24):
    num_negative_samples = [10000,12000,14000,16000,18000,20000]
    avg_row = []
    
    #
    test_data, id_set = ReadPredictDataset(hours, isWithID=True)
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
        # make predict
    prob_table = {}
    for i in range(len(id_set)):
        usid, itid = id_set[i][0], id_set[i][1]
        key = usid + ' ' + itid
        prob_table[key] = avg[i]
        
    import operator
    sorted_predict = sorted(prob_table.iteritems(), key=operator.itemgetter(1), reverse=True)  
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
    
    outfile = open('../csv/testingset/lr_predict_avg_result.csv', 'wb')
    spamwriter = csv.writer(outfile, dialect = 'excel')
    
    for i in range(len(id_set)):
        user_id = id_set[i][0]
        item_id = id_set[i][1]
        spamwriter.writerow([user_id, item_id, avg[i]])


'''Random Forest'''
def RFSinglePredict(num_negative_sample, date, top_k = 650, hours=24):
    test_data, id_set = ReadPredictDataset(hours, isWithID=True, level='2')
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
        

def RFAvgPredict(date, top_k=650, hours=24):
    num_negative_samples = [12000,14000,16000,18000,20000]
    avg_row = []
    
    #
    test_data, id_set = ReadPredictDataset(hours, isWithID=True, level='2')
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
        
    # make predict
    prob_table = {}
    for i in range(len(id_set)):
        usid, itid = id_set[i][0], id_set[i][1]
        key = usid + ' ' + itid
        prob_table[key] = avg[i]
        
    import operator
    sorted_predict = sorted(prob_table.iteritems(), key=operator.itemgetter(1), reverse=True)  
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
    
    # write prob, for ensemble
    outfile = open('../csv/testingset/rf_predict_avg_result.csv', 'wb')
    spamwriter = csv.writer(outfile, dialect = 'excel')
    
    for i in range(len(id_set)):
        user_id = id_set[i][0]
        item_id = id_set[i][1]
        spamwriter.writerow([user_id, item_id, avg[i]])
    
