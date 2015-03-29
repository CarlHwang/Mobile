#! /usr/bin/env python
# -*- coding:utf-8 -*-

import csv


dealTable = {}

def lastAccessTime():
    pass

def initTableOverItem():   
    # 输出的文件头
    outfile = open('last_access_time.csv', 'wb')
    spamwriter = csv.writer(outfile, dialect = 'excel')
    spamwriter.writerow(['user_id', 'item_id', 'click_gap1', 'click_gap2','collect_gap','cart_gap','time'])
    
    outfile_click1 = open('train_user_time_to_int_click1.csv', 'wb')
    spamwriter_click1 = csv.writer(outfile_click1, dialect = 'excel')
    spamwriter_click1.writerow(['user_id', 'item_id','time'])
    
    outfile_click2 = open('train_user_time_to_int_click2.csv', 'wb')
    spamwriter_click2 = csv.writer(outfile_click2, dialect = 'excel')
    spamwriter_click2.writerow(['user_id', 'item_id','time'])
    
    outfile_collect = open('train_user_time_to_int_collect.csv', 'wb')
    spamwriter_collect = csv.writer(outfile_collect, dialect = 'excel')
    spamwriter_collect.writerow(['user_id', 'item_id','time'])
    
    outfile_cart = open('train_user_time_to_int_cart.csv', 'wb')
    spamwriter_cart = csv.writer(outfile_cart, dialect = 'excel')
    spamwriter_cart.writerow(['user_id', 'item_id','time'])
    
    with open('../train_user_time_to_int.csv', 'rb') as infile:
        reader = csv.reader(infile)
        num = 1
        for row in reader:
            user_id = row[0]
            item_id = row[1]
            behavior_type = row[2]
            time = row[5]
            
            if time == 'time':
                continue
            if behavior_type == '4':
                spamwriter.writerow([user_id, item_id, -1, -1, -1, -1, time])
                print num, time
                
            elif behavior_type == '1':
                if num <= 5000000:
                    spamwriter_click1.writerow([user_id, item_id, time])
                else:
                    spamwriter_click2.writerow([user_id, item_id, time])
                num += 1
            elif behavior_type == '2':
                spamwriter_collect.writerow([user_id, item_id, time])
            else:
                spamwriter_cart.writerow([user_id, item_id, time])

            
def lastAccessTimeOverItemForBeh(btype):
    table = {}
    
    bfile = ''
    if btype == '1.1':
        bfile = 'train_user_time_to_int_click1.csv'
    elif btype == '1.2':
        bfile = 'train_user_time_to_int_click2.csv'
    elif btype == '2':
        bfile = 'train_user_time_to_int_collect.csv'
    else:
        bfile = 'train_user_time_to_int_cart.csv'
        
    with open(bfile, 'rb') as infile:
        reader = csv.reader(infile)
        num = 1
        for row in reader:
            user_id = row[0]
            item_id = row[1]
            time = row[2]
             
            if(time == 'time'):
                continue
             
            time = int(time)
            addToTable(table, user_id +' '+ item_id, time)
            print num, btype, time
            num+=1
            
    writeBehGap(btype, table)


def writeBehGap(btype, table):
    lastAccessTimeTable = []
    with open('last_access_time.csv', 'rb') as infile:
        reader = csv.reader(infile)
        num = 1
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
            lastBeh = -1
            if user_id == '112148363' and item_id == '390292615':
                lastBeh = getLastAccessTime(table, user_id +' '+ item_id, time)
            else:
                lastBeh = getLastAccessTime(table, user_id +' '+ item_id, time)
            gap = -1
            if not lastBeh == -1:
                gap = time - lastBeh
            print num, "   gap:", gap, "购买时间：", time, "行为", lastBeh
            num += 1
            if btype == '1.1':
                lastAccessTimeTable.append([user_id, item_id, gap, click_gap2, collect_gap, cart_gap, time])
            elif btype == '1.2':
                lastAccessTimeTable.append([user_id, item_id, click_gap1, gap, collect_gap, cart_gap, time])
            elif btype == '2':
                lastAccessTimeTable.append([user_id, item_id, click_gap1, click_gap2, gap, cart_gap, time])
            elif btype == '3':
                lastAccessTimeTable.append([user_id, item_id, click_gap1, click_gap2, collect_gap, gap, time])
              
    # 输出的文件头
    outfile = open('last_access_time.csv', 'wb')
    spamwriter = csv.writer(outfile, dialect = 'excel')
    spamwriter.writerow(['user_id', 'item_id', 'click_gap1', 'click_gap2','collect_gap','cart_gap','time'])
    
    for record in lastAccessTimeTable:
        spamwriter.writerow(record)

def getLastAccessTime(table, key, value):
    ret = -1
    if table.get(key):
        for i in range(len(table[key])):
#             print table[key]
            if value >= table[key][i]:
                ret = table[key][i]
            else:
                break
    return ret
            

def addToTable(table, key, value):
    if not table.get(key):
        table[key] = [value,]
    else:
        if value in table[key]:
            return
        # 冒泡排序 O(n)
        for i in range(len(table[key])):
            if value < table[key][i]:
                table[key].insert(i, value)


if __name__ == '__main__':
    initTableOverItem()
    lastAccessTimeOverItemForBeh('1.2')   # for click2
    lastAccessTimeOverItemForBeh('1.1')   # for click1
    
    lastAccessTimeOverItemForBeh('2')   # for collect
    lastAccessTimeOverItemForBeh('3')   # for cart
    