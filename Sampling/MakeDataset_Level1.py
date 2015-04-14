#! /usr/bin/env python
# -*- coding:utf-8 -*-

import csv
import random
from Sampling import GetFeature

negative_sample_num = 4574733



def MakeDateset(negative_sample_needed, target_model, date):
    
    featureTable = {}
    
    sampling_rate = negative_sample_needed / float(negative_sample_num) * 1000000
    
    with open('../csv/label.csv', 'rb') as f:
        reader = csv.reader(f)
        for row in reader:
            user_id = row[0]
            item_id = row[1]
            label = row[2]
            
            if user_id == 'user_id':
                continue
            
            key = user_id  + ' ' + item_id
            
            if not label == '1':
                seed = random.randint(1,1000000)
                if seed > sampling_rate:
                    continue
            
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
    
    GetFeature.GetDealAfterAccess(featureTable, '1')
    GetFeature.GetDealAfterAccess(featureTable, '2')
    GetFeature.GetDealAfterAccess(featureTable, '3')
    
    print "---------------------------------------------------------------"
    
    path = '../csv/trainningset/level1/' + date + '_' + target_model + '_' + str(negative_sample_needed) + '.csv'
    outfile = open(path, 'wb')
    spamwriter = csv.writer(outfile, dialect = 'excel')
                
    for key in featureTable.keys():
        
        user_id, item_id = key.split()[0], key.split()[1]
        features = featureTable[key]
        row = [user_id, item_id]
        row.extend(features)
        
        # double the positive sample
        write_time = 1
        if features[0] == '1':
            write_time = 2
        for i in range(write_time):
            spamwriter.writerow(row)
        

MakeDateset(10000, 'lr', '0413')
MakeDateset(10001, 'lr', '0413')
MakeDateset(12000, 'lr', '0413')
MakeDateset(12001, 'lr', '0413')
MakeDateset(14000, 'lr', '0413')
MakeDateset(16000, 'lr', '0413')
MakeDateset(18000, 'lr', '0413')
MakeDateset(20000, 'lr', '0413')

MakeDateset(10000, 'rf', '0413')
MakeDateset(10001, 'rf', '0413')
MakeDateset(12000, 'rf', '0413')
MakeDateset(12001, 'rf', '0413')
MakeDateset(14000, 'rf', '0413')
MakeDateset(16000, 'rf', '0413')
MakeDateset(18000, 'rf', '0413')
MakeDateset(20000, 'rf', '0413')

