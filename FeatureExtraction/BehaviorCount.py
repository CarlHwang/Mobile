#! /usr/bin/env python
# -*- coding:utf-8 -*-
from Sampling import Tool

import csv

# 获得每个商品的对于 不同行为 的人数
def item_behavior_count():
    # 输出的文件头
    outfile = open('../csv/item_behavior_count.csv', 'wb')
    spamwriter = csv.writer(outfile, dialect = 'excel')
    spamwriter.writerow(['item_id', 'click', 'collect', 'cart', 'deal'])
    
    items = {}
    with open('../csv/train_user_time_to_int_cleaned.csv', 'rb') as f:
        reader = csv.reader(f)
        for row in reader:
            item_id = row[1]
            behavior_type = row[2]

            if item_id == 'item_id':
                continue
            
            behavior_type = int(behavior_type)
            
            # 如果统计集合中没有这个商品，加入，如果有，对应的行为计数+1
            if not items.get(item_id):
                items[item_id] = [0,0,0,0]
                
            items[item_id][behavior_type-1] += 1
            
            print item_id, behavior_type
    
    for key in items.keys():
        behaviors = items.get(key)
        spamwriter.writerow([key, behaviors[0], behaviors[1], behaviors[2], behaviors[3]])

def user_behavior_count():
    # 输出的文件头
    outfile = open('../csv/user_behavior_count.csv', 'wb')
    spamwriter = csv.writer(outfile, dialect = 'excel')
    spamwriter.writerow(['user_id', 'click', 'collect', 'cart', 'deal'])
    
    users = {}
    with open('../csv/train_user_time_to_int_cleaned.csv', 'rb') as f:
        reader = csv.reader(f)
        for row in reader:
            user_id = row[0]
            behavior_type = row[2]

            if user_id == 'user_id':
                continue
            
            behavior_type = int(behavior_type)
            
            # 如果统计集合中没有这个人，加入，如果有，对应的行为计数+1
            if not users.get(user_id):
                users[user_id] = [0,0,0,0]

            users[user_id][behavior_type-1] += 1
            
            print user_id, behavior_type
    
    for key in users.keys():
        behaviors = users.get(key)
        spamwriter.writerow([key, behaviors[0], behaviors[1], behaviors[2], behaviors[3]])
        
def category_behavior_count():
    # 输出的文件头
    outfile = open('../csv/category_behavior_count.csv', 'wb')
    spamwriter = csv.writer(outfile, dialect = 'excel')
    spamwriter.writerow(['item_category', 'click', 'collect', 'cart', 'deal'])
    
    categorys = {}
    with open('../csv/train_user_time_to_int_cleaned.csv', 'rb') as f:
        reader = csv.reader(f)
        for row in reader:
            item_category = row[4]
            behavior_type = row[2]

            if item_category == 'item_category':
                continue
            
            behavior_type = int(behavior_type)
            
            # 如果统计集合中没有这个类，加入，如果有，对应的行为计数+1
            if not categorys.get(item_category):
                categorys[item_category] = [0,0,0,0]

            categorys[item_category][behavior_type-1] += 1
            
            print item_category, behavior_type
    
    for key in categorys.keys():
        behaviors = categorys.get(key)
        spamwriter.writerow([key, behaviors[0], behaviors[1], behaviors[2], behaviors[3]])

        
if __name__ == '__main__':
    item_behavior_count()
    user_behavior_count()
    category_behavior_count()
    pass
    
    
'''
#
#
#    GET FEATURE
#
#
'''
    
    
def GetItemBehaviorCount(outputTable):
    inputTable = {}
    with open('../csv/item_behavior_count.csv', 'rb') as f:
        reader = csv.reader(f)
        for row in reader:
            item_id = row[0]
            click = row[1]
            collect = row[2]
            cart = row[3]
            deal = row[4]
            
            if item_id == 'item_id':
                continue
            
            inputTable[item_id] = [click,collect,cart,deal]
   
    for key in outputTable.keys():
        item_id = key.split()[1]
        outputTable[key].extend(inputTable[item_id])


def GetUserBehaviorCount(outputTable):
    inputTable = {}
    with open('../csv/user_behavior_count.csv', 'rb') as f:
        reader = csv.reader(f)
        for row in reader:
            user_id = row[0]
            click = row[1]
            collect = row[2]
            cart = row[3]
            deal = row[4]
            
            if user_id == 'user_id':
                continue
            
            inputTable[user_id] = [click,collect,cart,deal]
   
    for key in outputTable.keys():
        user_id = key.split()[0]
        outputTable[key].extend(inputTable[user_id])


def GetCategoryBehaviorCount(outputTable):
    inputTable = {}
    with open('../csv/category_behavior_count.csv', 'rb') as f:
        reader = csv.reader(f)
        for row in reader:
            item_category = row[0]
            click = row[1]
            collect = row[2]
            cart = row[3]
            deal = row[4]
            
            if item_category == 'item_category':
                continue
            
            inputTable[item_category] = [click,collect,cart,deal]
            
    item_to_cate = {}
    with open('../csv/train_user_time_to_int_cleaned.csv', 'rb') as f:
        reader = csv.reader(f)
        for row in reader:
            item_id = row[1]
            item_category = row[4]
            if item_id == 'item_id':
                continue
            item_to_cate[item_id] = item_category
               
    for key in outputTable.keys():
        item_id = key.split()[1]
        item_category = item_to_cate[item_id]
        outputTable[key].extend(inputTable[item_category])
        
        
#         outputTable[key]['item_click_count'] = inputTable[item_id]['item_click_count']
#         outputTable[key]['item_collect_count'] = inputTable[item_id]['item_collect_count']
#         outputTable[key]['item_cart_count'] = inputTable[item_id]['item_cart_count']
#         outputTable[key]['item_deal_count'] = inputTable[item_id]['item_deal_count']
        
