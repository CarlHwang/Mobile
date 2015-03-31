#! /usr/bin/env python
# -*- coding:utf-8 -*-

import csv

# ���ÿ����Ʒ�Ķ��� ��ͬ��Ϊ ������
def user_deal_freq():
    # 输出的文件头
    outfile = open('../csv/user_deal_freq.csv', 'wb')
    spamwriter = csv.writer(outfile, dialect = 'excel')
    spamwriter.writerow(['user_id', 'deal_freq'])
    users = {}
    time_range = [-1,-1]
    #mouth=[30];
    with open('../csv/train_user_time_to_int_cleaned.csv', 'rb') as f:
        reader = csv.reader(f)
        for row in reader:
            user_id = row[0]
            behavior_type = row[2]
            time = row[5]
            if(time=='time'):
                continue
            
            time = int(time)
            
            if time_range[0] < 0:
                time_range = [time, time]
            else:
                time_range = [min(time_range[0], time), max(time_range[1], time)]
                        
            if(len(behavior_type) > 2):
                continue            
            if(behavior_type=='4'):                
                #time=int(row[5])
                if not users.get(user_id):
                    deal = 1
                    users[user_id] = deal
                else:
                    users[user_id] += 1
                    
    period = time_range[1]-time_range[0]+1
    for key in users.keys():
        deal = users[key]    
        spamwriter.writerow([key, deal/float(period)])
    
if __name__ == '__main__':
    user_deal_freq()