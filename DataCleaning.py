#! /usr/bin/env python
# -*- coding:utf-8 -*-

import csv

# 把user列表里的时间字符串转换成整数表示
def timeToInt():
    # 输出的文件头
    outfile = open('./csv/train_user_time_to_int.csv', 'wb')
    spamwriter = csv.writer(outfile, dialect = 'excel')
    spamwriter.writerow(['user_id', 'item_id', 'behavior_type', 'user_geohash', 'item_category', 'time'])
    
    with open('./csv/train_user.csv', 'rb') as infile:
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
    table = {}
    tableDeal = {}
    with open('./csv/train_user_time_to_int.csv', 'rb') as infile:
        reader = csv.reader(infile)
        for row in reader:
            user_id = row[0]
            item_id = row[1]
            behavior_type = row[2]
            time = row[5]
            
            if user_id == 'user_id':
                continue
            
            time = int(time)
            
            
            if behavior_type == '4':
                '''put deal into deal table'''
                if tableDeal.get(user_id):
                    if not tableDeal[user_id].get(item_id):
                        tableDeal[user_id][item_id] = []
                    tableDeal[user_id][item_id].append(time)
                else:
                    tableDeal[user_id] = {item_id: [time]}
            else:
                '''put click, collect, cart into another table'''
                if table.get(user_id):
                    if not table[user_id].get(item_id):
                        table[user_id][item_id] = []
                    table[user_id][item_id].append(time)
                else:
                    table[user_id] = {item_id: [time]}
                    
    tableDealInvalid ={}
                    
    ''' it is ugly below'''
    '''to see a deal time has or has not a smaller access time, if so, the deal time is valid'''
    for user_id in tableDeal.keys():
        
        tableDealInvalid[user_id] = {}
        items = tableDeal[user_id]
        
        for item_id in items.keys():
                        
            for deal_time in items[item_id]: 
                
                if table.get(user_id) and table[user_id].get(item_id):
                    
                    valid = False
                    
                    for time in table[user_id][item_id]:
                        
                        if time <= deal_time:
                            valid = True
                            break
                        
                    if not valid:
                        if tableDealInvalid[user_id].get(item_id):
                            tableDealInvalid[user_id][item_id] = max(deal_time, tableDealInvalid[user_id][item_id])
                        else:
                            tableDealInvalid[user_id][item_id] = deal_time
                else:
                    tableDealInvalid[user_id][item_id] = deal_time
                    
    table = None
    tableDeal = None
    
    # 输出的文件头
    outfile = open('./csv/train_user_time_to_int_cleaned.csv', 'wb')
    spamwriter = csv.writer(outfile, dialect = 'excel')
    spamwriter.writerow(['user_id', 'item_id', 'behavior_type', 'user_geohash', 'item_category', 'time'])
    with open('./csv/train_user_time_to_int.csv', 'rb') as infile:
        reader = csv.reader(infile)
        num = 1
        for row in reader:
            user_id = row[0]
            item_id = row[1]
            time = row[5]
            
            if user_id == 'user_id':
                continue
            
            time = int(time)
            
            if tableDealInvalid.get(user_id) and tableDealInvalid[user_id].get(item_id) and time < tableDealInvalid[user_id][item_id]:
                print num
                num += 1
                continue
            
            spamwriter.writerow(row)
                
            
# def cleanInvalidRecord():
#     # 输出的文件头
#     outfile = open('./csv/train_user_time_to_int_cleaned.csv', 'wb')
#     spamwriter = csv.writer(outfile, dialect = 'excel')
#     spamwriter.writerow(['user_id', 'item_id', 'behavior_type', 'user_geohash', 'item_category', 'time'])
#     
#     table = {}
#     with open('./csv/last_access_time.csv', 'rb') as infile:
#         reader = csv.reader(infile)
#         for row in reader:
#             user_id = row[0]
#             item_id = row[1]
#             click_gap1 = row[2]
#             click_gap2 = row[3]
#             collect_gap = row[4]
#             cart_gap = row[5]
#             time = row[6]
#             
#             if time == 'time':
#                 continue
#             time = int(time)
#             
#             if click_gap1 == '-1' and click_gap2 == '-1' and collect_gap == '-1' and cart_gap == '-1':
#                 key = user_id + ' ' + item_id
#                 if not table.get(key):
#                     table[key] = time
#                 else:
#                     table[key] = max(table[key], time)
#     
#     with open('./csv/train_user_time_to_int.csv', 'rb') as infile:
#         reader = csv.reader(infile)
#         num = 1
#         for row in reader:
#             user_id = row[0]
#             item_id = row[1]
#             time = row[5]
#             
#             if time == 'time':
#                 continue
#             time = int(time)
#             
#             key = user_id + ' ' + item_id
#             
#             if (not table.get(key)) or table[key] < time:
#                 
#                 spamwriter.writerow(row)
#             else:
#                 print num
#                 num += 1
             
if __name__ == '__main__':
#     timeToInt()
    cleanInvalidRecord()
