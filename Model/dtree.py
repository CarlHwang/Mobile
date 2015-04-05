#! /usr/bin/env python
# -*- coding:utf-8 -*-

# Auther: Carl Hwang
# Date: 2015-4-3

from dnode import decisionnode
import random

class decisiontree():
    
    def __init__(self, dataset, criterion=gini, min_sample_split=5, max_depth=None):
        self.root = self.buildrandomtree(dataset, 0, min_sample_split, max_depth)
        self.criterion = criterion
        pass
    
    
    def divideset(self, dataset, axis, value):
        ''''Make a function that tells us if a row is in 
        the first group (true) or the second group (false)'''
        
        split_function = None
        if isinstance(value, int) or isinstance(value, float):
            split_function = lambda row:row[axis] >= value
        else:
            split_function = lambda row:row[axis] == value
       
        set1 = [row for row in dataset if split_function(row)]
        set2 = [row for row in dataset if not split_function(row)]
        
        return set1, set2
    
    
    def entropy(self, dataset):
        '''Entropy is the sum of p(x)log(p(x)) across all q'''
        
        from math import log
        log2 = lambda x:log(x) / log(2) 
         
        labels = self.uniquelabels(dataset)
        ent = 0.0
        
        for l in labels.keys():
            p = float(labels[l]) / len(dataset)
            ent = ent - p * log2(p)
    
        return ent
    
    
    def gini(self, dataset):
        '''the gini coeffience'''
        
        labels = self.uniquelabels(dataset)
        gini = 1.0
        
        for l in labels.keys():
            p = float(labels[l]) / len(dataset)
            gini -= p**2
        
        return gini


    def uniquelabels(self, dataset):
        labels = {}
        for row in dataset:
            r = row[-1]
            if r not in labels: labels[r] = 0
            labels[r] += 1

        return labels
    
    
    def getvotinglabel(self, dataset):
        random_pick = False
        labels = self.uniquelabels(dataset)
        winner_label, winner_value = None, 0
        
        for key in labels.keys():
            if labels[key] > winner_value: winner_label = key
            elif labels[key] == winner_value: random_pick = True
            
        if random_pick:
            winner_label = random.choice(labels.keys())
            
        return winner_label
    
    
    def picksplitfeat(self, dataset, criterion=gini, random_pick=-1):
        '''pick a best split feature and its split point for spliting,
        return the feature index and the value.'''
        
        candidates = []
        lenvec = len(dataset[0]) -1
        
        split_feat, split_val = None, None
        mingini = 1
        
        if random_pick != -1:
            while(len(candidates) != random_pick):
                randint = random.randint(0, lenvec-1)
                if randint not in candidates: candidates.append(randint)
        else:
            candidates = [i for i in range(0, lenvec-1)]
        
        for feat_idx in candidates:
            feat_list = [vec[feat_idx] for vec in dataset]
            
            unique_value = set(feat_list)
#             if len(unique_value) == 1:   #do not split when all values in this dimension are the same
#                 continue
            
            for value in unique_value:
                set1, set2 = self.divideset(dataset, feat_idx, value)
                p = float(len(set1)) / len(dataset)
                
                tgini = p*self.criterion(set1) + (1-p)*self.criterion(set2)
                if tgini < mingini:
                    mingini = tgini
                    split_feat = feat_idx
                    split_val = value
                    
        return split_feat, split_val
    
    
    def buildrandomtree(self, dataset, current_level, min_sample_split=5, max_depth=None, neighbor_label=None):
        '''Recursive build a tree, once separate the data
        set to 2 part, each of them is a subtree.'''
        
        # It is allowed that the dataset is separated to 2 set
        # that each of them is empty. If so, the next tree building
        # process will assign a empty decision node to it.
        
        lendataset = len(dataset)
        current_level += 1
        
        # stop split condition
        if lendataset == 0: 
            return decisionnode(label=neighbor_label)
        
        if lendataset <= min_sample_split: 
            return decisionnode(label=self.getvotinglabel(dataset))
        
        if current_level < max_depth:
            return decisionnode(label=self.getvotinglabel(dataset))
        
        split_feat, split_val = self.picksplitfeat(dataset, criterion=self.criterion) 
        set1, set2 = self.divideset(dataset, split_feat, split_val)
        
        major_label_of_set1 = self.getvotinglabel(set1)
        major_label_of_set2 = self.getvotinglabel(set2)
        
        true_branch = self.buildrandomtree(set1, current_level, min_sample_split, max_depth, neighbor_label=major_label_of_set2)
        false_branch = self.buildrandomtree(set2, current_level, min_sample_split, max_depth, neighbor_label=major_label_of_set1)
        
        return decisionnode(feature=split_feat, value=split_val, truebranch=true_branch, falsebranch=false_branch)
        
        