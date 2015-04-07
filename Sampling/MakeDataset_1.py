#! /usr/bin/env python
# -*- coding:utf-8 -*-

import csv
import random
from FeatureExtraction import BehaviorCount, UAverageAccessGap, UAccessBeforeDeal

featureTable = {}

def MakeDateset(sampling_rate):
    
    with open('../csv/label.csv', 'rb') as f:
        reader = csv.reader(f)
        for row in reader:
            user_id = row[0]
            item_id = row[1]
            label = row[2]
            
            if user_id == 'user_id':
                continue
            
            key = user_id + ' ' + item_id
            
            featureTable[key] = {'label':label}
            
    BehaviorCount.GetItemBehaviorCount(featureTable)
    UAccessBeforeDeal.GetUserAccessBeforeDeal(featureTable)
    UAverageAccessGap.GetUserAvgAccessGap(featureTable)
            
    
    # 输出的文件头
    outfile = open('../csv/trainningset/dataset.csv', 'wb')
    spamwriter = csv.writer(outfile, dialect = 'excel')
    spamwriter.writerow(['user_id', 'item_id', 'user_average_access_gap', 'item_click_count', 'item_collect_count', 'item_cart_count', 'item_deal_count', 'access_before_deal', 'label'])
                
    sampling_rate *= 100
    
    total = 0
    select = 0
    
    for key in featureTable.keys():
        label = featureTable[key]['label']
        
        if not label == '1':
            total += 1
            seed = random.randint(1,100)
            print seed, sampling_rate
            if seed > sampling_rate:
                continue
            select += 1
        
        user_id, item_id = key.split()[0], key.split()[1]
        user_average_access_gap = featureTable[key]['user_average_access_gap']
        item_click_count = featureTable[key]['item_click_count']
        item_collect_count = featureTable[key]['item_collect_count']
        item_cart_count = featureTable[key]['item_cart_count']
        item_deal_count = featureTable[key]['item_deal_count']
        access_before_deal = featureTable[key]['access_before_deal']
        
        spamwriter.writerow([user_id, item_id, user_average_access_gap, item_click_count, item_collect_count, item_cart_count, item_deal_count, access_before_deal, label])
            
    print total, select
    
MakeDateset(0.2)
    