#! /usr/bin/env python
# -*- coding:utf-8 -*-
import csv

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
             
if __name__ == '__main__':
    timeToInt()
    #test
