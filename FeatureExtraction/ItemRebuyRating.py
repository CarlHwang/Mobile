#! /usr/bin/env python
# -*- coding:utf-8 -*-

import csv

def item_rebuy_rate():
    outfile = open('../csv/item_rebuy_rate.csv', 'wb')
    spamwriter = csv.writer(outfile, dialect = 'excel')
    spamwriter.writerow(['item_id', 'rebuy_rate'])
    #rate = []
    items = {}
    with open('../csv/class_by_item.csv', 'rb') as f1:
        reader_usernum = csv.reader(f1)
        for row_usernum in reader_usernum:
            item_id = row_usernum[0]
            if(item_id=='item_id'):
                    continue
            item_buyer = row_usernum[1]
            items[item_id] = item_buyer
      
    with open('../csv/item_behavior_count.csv','rb') as f2:
        reader_deal = csv.reader(f2)
        for row_deal in reader_deal:
            item_id_deal = row_deal[0]
            if(item_id_deal=='item_id'):
                continue
            deal = int(row_deal[4])
            if items.get(item_id_deal):
                user_num = items[item_id_deal]
#             user_num=items.get(item_id_deal)
                user_num = int(user_num)
                rate=(deal-user_num)/float(deal)
                spamwriter.writerow([item_id_deal,rate])
     
                
                print item_id_deal,rate,deal,user_num

             

if __name__ == '__main__':
    item_rebuy_rate()