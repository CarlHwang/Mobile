#! /usr/bin/env python
# -*- coding:utf-8 -*-

import csv

def LR_RF_Blending(lr_weight, rf_weight, top_k = 650):
    
    RF_prob = {}
    LR_prob = {}
    
    with open('../csv/testingset/rf_predict_avg_result.csv', 'rb') as f:
        reader = csv.reader(f)
        for row in reader:
            user_id = row[0]
            item_id = row[1]
            prob = float(row[2])
            key = user_id + ' ' + item_id
            RF_prob[key] = prob
            
    with open('../csv/testingset/lr_predict_avg_result.csv', 'rb') as f:
        reader = csv.reader(f)
        for row in reader:
            user_id = row[0]
            item_id = row[1]
            prob = float(row[2])
            key = user_id + ' ' + item_id
            LR_prob[key] = prob
            
    # make predict
    prob_table = {}
    for key in LR_prob.keys():
        prob_table[key] = lr_weight * LR_prob[key] + rf_weight * RF_prob[key]
    
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
            