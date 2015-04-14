#! /usr/bin/env python
# -*- coding:utf-8 -*-

import csv
from Sampling import GetFeature


def MakePredictDateset(hours):
    featureTable = {}

    path = '../csv/testingset/level2/predict_set_' + str(hours) + 'h.csv'
    with open(path, 'rb') as f:
        reader = csv.reader(f)
        for row in reader:
            user_id = row[0]
            item_id = row[1]
            
            if user_id == 'user_id':
                continue
            
            key = user_id  +' ' + item_id
     
            featureTable[key] = []
            
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
    
    GetFeature.GetDealAfterAccess(featureTable, '1')
    GetFeature.GetDealAfterAccess(featureTable, '2')
    GetFeature.GetDealAfterAccess(featureTable, '3')

    GetFeature.GetLROutput(featureTable)
    
    out_path = '../csv/testingset/level2/predict_set_feature_' + str(hours) + 'h.csv'
    outfile = open(out_path, 'wb')
    spamwriter = csv.writer(outfile, dialect = 'excel')
                
    for key in featureTable.keys():
        
        user_id, item_id = key.split()[0], key.split()[1]
        features = featureTable[key]
        row = [user_id, item_id]
        row.extend(features)
        
        spamwriter.writerow(row)

MakePredictDateset(720)

