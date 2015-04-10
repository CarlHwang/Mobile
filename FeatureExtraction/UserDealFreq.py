#! /usr/bin/env python
# -*- coding:utf-8 -*-

import csv

def user_deal_freq():
    outfile = open('../csv/user_deal_freq.csv', 'wb')
    spamwriter = csv.writer(outfile, dialect = 'excel')
    spamwriter.writerow(['user_id', 'deal_freq'])
    users = {}
    time_range = [-1,-1]
    with open('../csv/train_user_time_to_int_cleaned.csv', 'rb') as f:
        reader = csv.reader(f)
        for row in reader:
            user_id = row[0]
            time = row[5]
            if(time=='time'):
                continue
            
            time = int(time)
            behavior_type = int(row[2])

            if time_range[0] < 0:
                time_range = [time, time]
            else:
                time_range = [min(time_range[0], time), max(time_range[1], time)]         

            if not users.get(user_id):
                if behavior_type == 4:
                    users[user_id] = 1
                else:
                    users[user_id] = 0
            else:
                if behavior_type==4:
                    users[user_id] += 1
                

                    
    period = time_range[1]-time_range[0]+1
    for key in users.keys():
        deal = users[key]    
        spamwriter.writerow([key, deal/float(period)])
        
user_deal_freq()

    
'''
#
#
#    GET FEATURE
#
#
'''
def GetUserDealFreq(outputTable):
    inputTable = {}
    #minUserDealFreq = 0
    with open('../csv/user_deal_freq.csv', 'rb') as f:
        reader = csv.reader(f)
        for row in reader:
            user_id = row[0]
            UserDealFreq = row[1]
            
            if user_id == 'user_id':
                continue
            
            inputTable[user_id] = float(UserDealFreq)            
    
    for key in outputTable.keys():
        user_id = key.split()[0]
        if not inputTable.get(user_id):
            outputTable[key].append(0)
        else:
            outputTable[key].append(inputTable[user_id])
 
    
      
    
