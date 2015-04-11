#! /usr/bin/env python
# -*- coding:utf-8 -*-

# Auther: Carl Hwang
# Date: 2015-4-5

import csv



from TrainLogisticRegression import FitLogisticRegression
from PredictByModel import LRSinglePredict

from TrainRandomForest import FitRandomForest
from PredictByModel import RFSinglePredict
import Evaluation

FitLogisticRegression(20000, '0413')
LRSinglePredict(20000, '0413', top_k=500)
Evaluation.evaluate()

# FitRandomForest(20000, '0413')
# RFSinglePredict(20000, '0413', top_k=600)
# Evaluation.evaluate()



