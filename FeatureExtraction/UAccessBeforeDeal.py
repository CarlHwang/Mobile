#! /usr/bin/env python
# -*- coding:utf-8 -*-

import csv

def AccessBeforeDeal():
    table = {}
    with open('../csv/last_access_time.csv', 'rb') as infile:
        reader = csv.reader(infile)
        for row in reader:
            user_id = row[0]
            
            click_before1 = row[6]
            click_before2 = row[7]
            collect_before = row[8]
            cart_before = row[9]
            
            if user_id == 'user_id':
                continue
            click_before1 = int(click_before1)
            click_before2 = int(click_before2)
            collect_before = int(collect_before)
            cart_before = int(cart_before)
            
            if table.get(user_id):
                table[user_id][0] += (click_before1+click_before2+collect_before+cart_before)
                table[user_id][1] += 1
            else:
                table[user_id] = [click_before1+click_before2+collect_before+cart_before, 1]
    
    # 输出的文件头
    outfile = open('../csv/user_access_before_deal.csv', 'wb')
    spamwriter = csv.writer(outfile, dialect = 'excel')
    spamwriter.writerow(['user_id', 'average_access_before'])
    
    for key in table.keys():
        spamwriter.writerow([key, table[key][0]/float(table[key][1])])
        
    print "UAccessBeforeDeal Done!"

if __name__ == '__main__':
    AccessBeforeDeal()
    pass


'''
#
#
#    GET FEATURE
#
#
'''
        
        
def GetUserAccessBeforeDeal(outputTable):
    inputTable = {}
    maxAccessBeforeDeal = 0
    with open('../csv/user_access_before_deal.csv', 'rb') as f:
        reader = csv.reader(f)
        for row in reader:
            user_id = row[0]
            access_before_deal = row[1]
            
            if user_id == 'user_id':
                continue
            
            inputTable[user_id] = access_before_deal
            maxAccessBeforeDeal = max(maxAccessBeforeDeal, access_before_deal)
    
    for key in outputTable.keys():
        user_id = key.split()[0]
        if not inputTable.get(user_id):
            outputTable[key]['access_before_deal'] = maxAccessBeforeDeal
        else:
            outputTable[key]['access_before_deal'] = inputTable[user_id]
        