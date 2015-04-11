#! /usr/bin/env python
# -*- coding:utf-8 -*-

import csv
import random
from Sampling import GetFeature



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
            
            key = user_id  +' ' + item_id
            
            featureTable[key] = [label]
            
    GetFeature.GetAverageAccessGap(featureTable, '1') 
    GetFeature.GetAverageAccessGap(featureTable, '2') 
    GetFeature.GetAverageAccessGap(featureTable, '3') 
    GetFeature.GetAverageAccessGap(featureTable, '4') 
    
    GetFeature.GetBehaviorCoutingInCountingHour(featureTable, '1')       
    GetFeature.GetBehaviorCoutingInCountingHour(featureTable, '2')       
    GetFeature.GetBehaviorCoutingInCountingHour(featureTable, '3')       
    GetFeature.GetBehaviorCoutingInCountingHour(featureTable, '4')       
     
    GetFeature.GetBehaviorHourCountBeforePeriod(featureTable, '1')
    GetFeature.GetBehaviorHourCountBeforePeriod(featureTable, '2')
    GetFeature.GetBehaviorHourCountBeforePeriod(featureTable, '3')
    GetFeature.GetBehaviorHourCountBeforePeriod(featureTable, '4')
     
    GetFeature.GetBehaviorHourCountInPeriod(featureTable, '1')
    GetFeature.GetBehaviorHourCountInPeriod(featureTable, '2')
    GetFeature.GetBehaviorHourCountInPeriod(featureTable, '3')
    GetFeature.GetBehaviorHourCountInPeriod(featureTable, '4')
    
    GetFeature.GetCategoryBehaviorCount(featureTable, '1')
    GetFeature.GetCategoryBehaviorCount(featureTable, '2')
    GetFeature.GetCategoryBehaviorCount(featureTable, '3')
    GetFeature.GetCategoryBehaviorCount(featureTable, '4')
    
    GetFeature.GetEarliestBehavior(featureTable, '1')
    GetFeature.GetEarliestBehavior(featureTable, '2')
    GetFeature.GetEarliestBehavior(featureTable, '3')
    GetFeature.GetEarliestBehavior(featureTable, '4')
     
    GetFeature.GetFirstAccessAgainstLast(featureTable, '1')
    GetFeature.GetFirstAccessAgainstLast(featureTable, '3')
    GetFeature.GetFirstAccessAgainstLast(featureTable, '4')
     
    GetFeature.GetItemCategoryBehaviorRatio(featureTable, '1')
    GetFeature.GetItemCategoryBehaviorRatio(featureTable, '2')
    GetFeature.GetItemCategoryBehaviorRatio(featureTable, '3')   
    GetFeature.GetItemCategoryBehaviorRatio(featureTable, '4')
     
    GetFeature.GetItemOfSameCategoryInRange(featureTable, '1')
    GetFeature.GetItemOfSameCategoryInRange(featureTable, '2')
    GetFeature.GetItemOfSameCategoryInRange(featureTable, '3')
    GetFeature.GetItemOfSameCategoryInRange(featureTable, '4')

    
    outfile = open('../csv/trainningset/dataset.csv', 'wb')
    spamwriter = csv.writer(outfile, dialect = 'excel')
                
    sampling_rate *= 10000
    
    total = 0
    select = 0
    
    for key in featureTable.keys():
        label = featureTable[key][0]
        
        if not label == '1':
            total += 1
            seed = random.randint(1,10000)
            print seed, sampling_rate
            if seed > sampling_rate:
                continue
            select += 1
        
        user_id, item_id = key.split()[0], key.split()[1]
        

        features = featureTable[key]
        row = [user_id, item_id]
        row.extend(features)
        
        spamwriter.writerow(row)
        
    print total, select


MakeDateset(0.0011)


