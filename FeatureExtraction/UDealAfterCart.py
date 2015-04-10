#! /usr/bin/env python
# -*- coding:utf-8 -*-

import csv

def DealAferCart():


    cart_time_table = {}
    
    deal_time_table = {}
    
    cart_num=0
    deal_cart_num = 0
    
    with open('../csv/train_user_time_to_int_cleaned.csv', 'rb') as f:
        reader = csv.reader(f)
        for row in reader:
            if(row[0]=='user_id'):
                continue
            ui_id = row[0]+' '+row[1]
            behavior_type = row[2]

            
            behavior_type = int(behavior_type)
            time_point = 0
            if(behavior_type==3):
                time_point = int(row[5])
                if not cart_time_table.get(ui_id):
                    
                    cart_time_table[ui_id] = [time_point]
                else:
                    #time.sort();
                    if not time_point in cart_time_table[ui_id]:
                        cart_time_table[ui_id].append(time_point)
                    #print ui_id,cart_time[ui_id]
            if(behavior_type ==4):
                time_point = int(row[5])
                if not deal_time_table.get(ui_id):
                    deal_time_table[ui_id] = [time_point]
                else:
                    if not time_point in deal_time_table[ui_id]:
                        deal_time_table[ui_id].append(time_point)
                    #print ui_id,cart_time[ui_id]
                    
    for key in cart_time_table.keys():
        time_cart = cart_time_table[key]
        if deal_time_table.get(key):
            time_deal = deal_time_table[key]
            for cart in time_cart:
                for deal in time_deal:
                    if deal-cart>=0:
                        deal_cart_num += 1
                        break
                cart_num += 1
        else:
            cart_num += len(time_cart)

    rate = deal_cart_num/float(cart_num)
    print deal_cart_num,cart_num,rate
             
if __name__ == '__main__':
    DealAferCart()
    
    
    