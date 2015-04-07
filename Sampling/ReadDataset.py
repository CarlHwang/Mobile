#! /usr/bin/env python
# -*- coding:utf-8 -*-


import csv

def ReadDataset(sampling_rate):
    
    with open('../csv/label.csv', 'rb') as f:
        reader = csv.reader(f)
        for row in reader:
            user_id = row[0]