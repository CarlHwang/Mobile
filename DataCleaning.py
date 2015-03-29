#! /usr/bin/env python
# -*- coding:utf-8 -*-
import csv
from _ast import Num

# 把user列表里的时间字符串转换成整数表示
def timeToInt():
    # 输出的文件头
    outfile = open('train_user_time_to_int.csv', 'wb')
    spamwriter = csv.writer(outfile, dialect = 'excel')
    spamwriter.writerow(['user_id', 'item_id', 'behavior_type', 'user_geohash', 'item_category', 'time'])
    
    with open('train_user.csv', 'rb') as infile:
        reader = csv.reader(infile)
        for row in reader:
            user_id = row[0]
            item_id = row[1]
            behavior_type = row[2]
            user_geohash = row[3]
            item_category = row[4]
            time = row[5]
            
            if(len(time) < 12):
                continue
            month = int(time[5:7])
            day = int(time[8:10])
            hour = int(time[11:])
            num = 1
            
            # 计算相对时间
            if(month == 11):
                num += (day-18)*24 + hour
            else:
                num += 312 + (day-1)*24 + hour
                
            spamwriter.writerow([user_id, item_id, behavior_type, user_geohash, item_category, num])
            
            print month, day, hour, num
            
def cleanInvalidRecord():
    # 输出的文件头
    outfile = open('train_user_time_to_int_cleaned.csv', 'wb')
    spamwriter = csv.writer(outfile, dialect = 'excel')
    spamwriter.writerow(['user_id', 'item_id', 'behavior_type', 'user_geohash', 'item_category', 'time'])
    
    table = {}
    with open('./FeatureExtraction/last_access_time.csv', 'rb') as infile:
        reader = csv.reader(infile)
        for row in reader:
            user_id = row[0]
            item_id = row[1]
            click_gap1 = row[2]
            click_gap2 = row[3]
            collect_gap = row[4]
            cart_gap = row[5]
            time = row[6]
            
            if time == 'time':
                continue
            time = int(time)
            
            if click_gap1 == '-1' and click_gap2 == '-1' and collect_gap == '-1' and cart_gap == '-1':
                key = user_id + ' ' + item_id
                if not table.get(key):
                    table[key] = time
                else:
                    table[key] = max(table[key], time)
    
    with open('train_user_time_to_int.csv', 'rb') as infile:
        reader = csv.reader(infile)
        num = 1
        for row in reader:
            user_id = row[0]
            item_id = row[1]
            time = row[5]
            
            if time == 'time':
                continue
            time = int(time)
            
            key = user_id + ' ' + item_id
            if (not table.get(user_id + ' ' + item_id)) or table[key] < time:
                
                spamwriter.writerow(row)
            else:
                print num
                num += 1
                    
            
            
             
if __name__ == '__main__':
#     timeToInt()
    cleanInvalidRecord()
