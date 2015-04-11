#! /usr/bin/env python
# -*- coding:utf-8 -*-

import csv


def evaluate():
    test = {}
    
    true_num = 0
    predict_num = 0
    hit_num = 0
    
    with open('../predict/test_set.csv', 'rb') as f:
        reader = csv.reader(f)
        for row in reader:
            user_id = row[0]
            item_id = row[1]
                
            if user_id == 'user_id':
                continue
                
            if not test.get(user_id):
                test[user_id] = [item_id]
            test[user_id].append(item_id)
            true_num += 1
                
    with open('../predict/tianchi_mobile_recommendation_predict.csv', 'rb') as f:
        reader = csv.reader(f)
        for row in reader:
            user_id = row[0]
            item_id = row[1]
            
            if user_id == 'user_id':
                continue
            
            if test.get(user_id) and item_id in test[user_id]:
                hit_num += 1
            predict_num += 1
            
    precision = hit_num / float(predict_num)
    recall = hit_num / float(true_num)
    F1 = 2*precision*recall / (precision+recall)
    
    print 'F1:', F1, '  Precision:', precision, '  Recall:', recall
    
# evaluate()
