#! /usr/bin/env python
# -*- coding:utf-8 -*-

def NormOneDim(table):
    min_value,max_value = -1,-1
    norm_table = {}
    for key in table.keys():
        print table[key]
        value = float(table[key])
        if min_value==-1:
            min_value = value
            max_value = value
        min_value = min(min_value,value)
        max_value = max(max_value,value)
    print max_value,min_value  
    for key in table.keys():
        value = float(table[key])
        norm_table[key] = (value-min_value)/(max_value-min_value)
        
    return norm_table

def NormTwoDim(table):
    user_table ={}
    sub_table = {}
    norm_table = table.copy()
    for user_id in table.keys():
        per_user = table[user_id]
        #print per_user
        user_type = []
        for key in per_user.keys():
                
            if not user_table.get(key):
                user_table[key] =  [user_id,per_user[key]]
            else:
                user_type = user_table[key]
                user_type.append([user_id,per_user[key]])
                user_table[key] = user_type
            print user_table[key],'\n'

    for key in user_table.keys():
        user_table[key]= NormOneDim(user_table[key])
        
    for user_id in user_table[key].keys():
        norm_table[user_id][key] = user_table[key][user_id]
            
        print user_table
    
    return norm_table
                    