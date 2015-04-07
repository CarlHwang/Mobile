#! /usr/bin/env python
# -*- coding:utf-8 -*-


import csv

# 把user列表里的时间字符串转换成整数表示
def makeTrainingSet():
    
    dataset = []
    
    with open('./csv/train_user_time_to_int_cleaned.csv', 'rb') as infile:
        reader = csv.reader(infile)

        for row in reader:
            time = row[5]
            
            if time == 'time':
                continue
            time = int(time)
            
            if time > 720:
                continue
            
            dataset.append(row)
            
            
            
    # 输出的文件头
    outfile = open('./csv/train_user_time_to_int_cleaned.csv', 'wb')
    spamwriter = csv.writer(outfile, dialect = 'excel')
    spamwriter.writerow(['user_id', 'item_id', 'behavior_type', 'user_geohash', 'item_category', 'time'])
    
    for row in dataset:
        spamwriter.writerow(row)
    
    print 'Done !'
            
             
if __name__ == '__main__':
    makeTrainingSet()
