#! /usr/bin/env python
# -*- coding:utf-8 -*-

import csv
from numpy.f2py.auxfuncs import throw_error

clickTable = {}
collectTable = {}
cartTable = {}
dealTable = {}

lastAccessTimeTable = []

def lastAccessTime():
    pass

def lastAccessTimeOverItem():
    # 输出的文件头
    outfile = open('last_access_time.csv', 'wb')
    spamwriter = csv.writer(outfile, dialect = 'excel')
    spamwriter.writerow(['user_id', 'item_id', 'last_access_gap'])
    

    with open('../train_user_time_to_int.csv', 'rb') as infile:
        reader = csv.reader(infile)
        for row in reader:
            user_id = row[0]
            item_id = row[1]
            behavior_type = row[2]
            time = row[5]
            
            if(len(time) > 3):
                continue
            
            time = int(time)
            if behavior_type == '1':
                addToTable(clickTable, user_id +' '+ item_id, time)
            elif behavior_type == '2':
                addToTable(collectTable, user_id +' '+ item_id, time)
            elif behavior_type == '3':
                addToTable(cartTable, user_id +' '+ item_id, time)
            else:
                addToTable(dealTable, user_id +' '+ item_id, time)
        
        
    print "建表完成"
        
    for key in dealTable.keys():
        times = dealTable[key]
        for time in times:
            lastClick = getLastAccessTime(clickTable, key, time)
            lastCollect = getLastAccessTime(collectTable, key, time)
            lastCart = getLastAccessTime(cartTable, key, time)
            last = max(lastClick, lastCollect, lastCart)
            
            gap = time - last
            print "gap", gap, "购买时间：", time, "点击", lastClick, "收藏", lastCollect, "购物车", lastCart
            if gap < 0:
                raise Exception("gap小于0")
            heads = key.split()
            lastAccessTimeTable.append([heads[0], heads[1], gap])
    
    for record in lastAccessTimeTable:
        spamwriter.writerow(record)
                
def getLastAccessTime(table, key, value):
    ret = -1
    if table.get(key):
        for i in range(len(table[key])):
            if value >= table[key][i]:
                ret = table[key][i]
            else:
                break
    return ret
            
def addToTable(table, key, value):
    if not table.get(key):
        table[key] = [value]
    else:
        # 选择排序 O(n)
        for i in range(len(table[key])):
            if value < table[key][i]:
                table[key].insert(i, value)
                
if __name__ == '__main__':
    lastAccessTimeOverItem()
    
                