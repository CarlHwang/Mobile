#! /usr/bin/env python
# -*- coding:utf-8 -*-

import csv
from math import log, fabs
from pylab import scatter, linspace, plot, show


def generateDecayCurvePotin():
    # 输出的文件头
    outfile = open('../csv/last_access_gap.csv', 'wb')
    spamwriter = csv.writer(outfile, dialect = 'excel')
    spamwriter.writerow(['user_id', 'item_id', 'last_access_gap'])

    with open('../csv/last_access_time.csv', 'rb') as infile:
        reader = csv.reader(infile)
        num = 1
        for row in reader:
            user_id = row[0]
            item_id = row[1]
            click_gap1 = row[2]
            click_gap2 = row[3]
            collect_gap = row[4]
            cart_gap = row[5]
            
            if user_id == 'user_id':
                continue
            
            click_gap1 = int(click_gap1)
            click_gap2 = int(click_gap2)
            collect_gap = int(collect_gap)
            cart_gap = int(cart_gap)
            
            minGap = getValidMin([click_gap1, click_gap2, collect_gap, cart_gap])
            spamwriter.writerow([user_id, item_id, minGap])
            print num, minGap
            num += 1
                

def getValidMin(nums):
    MIN = 999 # 最大可能不会大于744，因此初始化为999合理
    for num in nums:
        if num < 0:
            continue
        MIN = min(MIN,num)
    return MIN

def calculateDecayCurvePoint():
    table = {}
    with open('../csv/last_access_gap.csv', 'rb') as infile:
        reader = csv.reader(infile)
        for row in reader:
            gap = row[2]
            
            if gap == 'last_access_gap':
                continue
            
            gap = int(gap)
            if table.get(gap):
                table[gap] += 1
            else:
                table[gap] = 1
                
    subTable = {}
    sorted(table.keys())
    for key in table.keys():
        subTable[key] = log(table[key]+1)
        if len(subTable.keys()) >= 500:
            break
    
    
    #normalize  
    tmax = max(subTable.keys()) +1
    ptmax = max(subTable.values())
    for key in subTable.keys():
        subTable[key] /= float(ptmax)
    
    print tmax
    
    minLoss = -1
    optExp = -1
    
    for exp in range(-999,0):
        exp /= 1000.0
        loss = 0
        for x in subTable.keys():
            y = subTable[x]
            loss += fabs(((tmax-x)**exp - y))   # absolute error
#             loss += ((tmax-x)**exp - y)**2    # square error
        
        if minLoss == -1:
            minLoss = loss
            optExp = exp
        elif loss < minLoss:
            minLoss = loss
            optExp = exp
    print optExp, minLoss
    
    scatter(subTable.keys(), subTable.values())
    x = linspace(1, 700, 5000)
    f1 = x**optExp
    plot(x, f1, 'r')
    show()

if __name__ == '__main__':
#     generateDecayCurvePotin()
    calculateDecayCurvePoint()
    