#! /usr/bin/env python
# -*- coding:utf-8 -*-

import csv

# ���ÿ����Ʒ�Ķ��� ��ͬ��Ϊ ������
def user_behavior_hour():
    # 输出的文件头
    outfile = open('../csv/user_behavior_hour.csv', 'wb')
    spamwriter = csv.writer(outfile, dialect = 'excel')
    spamwriter.writerow(['user_id', 'behavior_hour'])
    users = {}
    with open('../csv/train_user_time_to_int_cleaned.csv', 'rb') as f:
        reader = csv.reader(f)
        for row in reader:
            user_id = row[0]
                        
            if(row[5]=='time'):
                continue
            time=int(row[5])
            if not users.get(user_id):
                hour=[0]
                hour[0]= time
                users[user_id] = hour
            else:
                hour = users.get(user_id)
                if(time in hour):
                    continue
                hour.append(time)
                users[user_id] = hour
    
    for key in users.keys():
        hour = users.get(key)
        spamwriter.writerow([key, len(hour)])
    
if __name__ == '__main__':
    user_behavior_hour()
    