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
            transformed_row = []
            label = int(row[2])
            transformed_row.append(label)
            for i in range(3,len(row)):
                transformed_row.append(float(row[i]))
            dataset.append(transformed_row)
            
    scaler = preprocessing.MinMaxScaler()
    scaled_dataset = scaler.fit_transform(dataset)
    return scaled_dataset


def ReadPredictDataset(hours, isWithID):
    dataset = []
    idset = []
    path = '../csv/testingset/predict_set_feature_' + str(hours) + 'h.csv'
    with open(path, 'rb') as f:
        reader = csv.reader(f)
        for row in reader:
            transformed_row = []
            idset.append([row[0], row[1]])
#             label = int(row[2])
#             transformed_row.append(label)
            for i in range(2,len(row)):
                transformed_row.append(float(row[i]))
            dataset.append(transformed_row)
            
    scaler = preprocessing.MinMaxScaler()
    scaled_dataset = scaler.fit_transform(dataset)
    if isWithID:
        return scaled_dataset, idset
    return scaled_dataset

