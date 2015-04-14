#! /usr/bin/env python
# -*- coding:utf-8 -*-


import csv
from sklearn import preprocessing

def ReadDataset(negative_sample_needed, target_model, date, level = '1'):
    
    dataset = []
    path = '../csv/trainningset/level' + level + '/' + date + '_' + target_model + '_' + str(negative_sample_needed) + '.csv'
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


def ReadPredictDataset(hours, isWithID, level = '1'):
    dataset = []
    idset = []
    path = '../csv/testingset/level' + level + '/predict_set_feature_' + str(hours) + 'h.csv'
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

