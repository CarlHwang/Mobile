#! /usr/bin/env python
# -*- coding:utf-8 -*-


import csv
from sklearn import preprocessing

# def ReadDataset(dataset_name):
#     
#     dataset = []
#     
#     path = '../csv/trainningset/' + dataset_name + '.csv'
#     with open(path, 'rb') as f:
#         reader = csv.reader(f)
#         for row in reader:
#             user_id = row[0]
#             
#             if user_id == 'user_id':
#                 continue
#             
#             rowlen = len(row)
#             sample = []
#             for i in range(2,rowlen-1):
#                 sample.append(float(row[i]))
#             sample.append(int(row[-1]))
#                 
#             dataset.append(sample)
#     
#     return dataset

def ReadDataset(negative_sample_needed, target_model, date):
    
    dataset = []
    path = '../csv/trainningset/' + date + '_' + target_model + '_' + str(negative_sample_needed) + '.csv'
    with open(path, 'rb') as f:
        reader = csv.reader(f)
        for row in reader:
            dataset.append(row[2:])
            
    scaler = preprocessing.MinMaxScaler()
    scaled_dataset = scaler.fit_transform(dataset)
    return scaled_dataset
            
