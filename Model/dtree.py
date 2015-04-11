#! /usr/bin/env python
# -*- coding:utf-8 -*-

# Auther: Carl Hwang
# Date: 2015-4-3

from dnode import decisionnode
import random

class DecisionTree():
    
    def __init__(self, 
                dataset, 
                criterion='gini', 
                min_sample_split=5, 
                max_depth=None):
        
        self.criterion = criterion
        self.root = self.buildRandomTree(dataset, 0, min_sample_split, max_depth)
            
    
    def classify(self, vec):
        
        current_node = self.root
        while not current_node.label == None:
            
            value = vec[current_node.feature]
            if value >= current_node.value:
                current_node = current_node.truebranch
            else:
                current_node = current_node.falsebranch
                
        return current_node.label
        
    
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
         
        labels = self.uniqueLabels(dataset)
        ent = 0.0
        
        for l in labels.keys():
            p = float(labels[l]) / len(dataset)
            ent = ent - p * log2(p)
    
        return ent
    
    
    def gini(self, dataset):
        '''the gini coeffience'''
        
        labels = self.uniqueLabels(dataset)
        gini = 1.0
        
        for l in labels.keys():
            p = float(labels[l]) / len(dataset)
            gini -= p**2
        
        return gini


    def uniqueLabels(self, dataset):
        labels = {}
        for row in dataset:
            r = row[-1]
            if r not in labels: labels[r] = 0
            labels[r] += 1

        return labels
    
    
    def getVotingLabel(self, dataset):
        random_pick = False
        labels = self.uniqueLabels(dataset)
        winner_label, winner_value = None, 0
        
        for key in labels.keys():
            if labels[key] > winner_value: winner_label = key
            elif labels[key] == winner_value: random_pick = True
            
        if random_pick:
            winner_label = random.choice(labels.keys())
            
        return winner_label
    
    
    def pickSplitFeat(self, dataset, random_pick=-1):
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
            candidates = [i for i in range(0, lenvec)]
        
        for feat_idx in candidates:
            feat_list = [vec[feat_idx] for vec in dataset]
            
            unique_value = set(feat_list)
#             if len(unique_value) == 1:   #do not split when all values in this dimension are the same
#                 continue
            
            for value in unique_value:
                set1, set2 = self.divideset(dataset, feat_idx, value)
                p = float(len(set1)) / len(dataset)
                
                if self.criterion == 'gini':
                    
                    tgini = p*self.gini(set1) + (1-p)*self.gini(set2)
                    if tgini < mingini:
                        print feat_idx, value, tgini
                        mingini = tgini
                        split_feat = feat_idx
                        split_val = value
                    
        return split_feat, split_val
    
    
    def buildRandomTree(self, dataset, current_level, min_sample_split=5, max_depth=None, neighbor_label=None):
        '''Recursive build a tree, once separate the data
        set to 2 part, each of them is a subtree.'''
        
        # It is allowed that the dataset is separated to 2 set
        # that each of them is empty. If so, the next tree building
        # process will assign a empty decision node to it.
        
        sizedataset = len(dataset)
        current_level += 1
        
        # stop split condition
        if sizedataset == 0: 
            return decisionnode(label=neighbor_label)
        
        if sizedataset <= min_sample_split: 
            return decisionnode(label=self.getVotingLabel(dataset))
        
        if not max_depth == None and current_level >= max_depth:
            return decisionnode(label=self.getVotingLabel(dataset))
        
        split_feat, split_val = self.pickSplitFeat(dataset) 
        print split_feat, split_val
        set1, set2 = self.divideset(dataset, split_feat, split_val)
        
        major_label_of_set1 = self.getVotingLabel(set1)
        major_label_of_set2 = self.getVotingLabel(set2)
        
        true_branch = self.buildRandomTree(set1, current_level, min_sample_split, max_depth, neighbor_label=major_label_of_set2)
        false_branch = self.buildRandomTree(set2, current_level, min_sample_split, max_depth, neighbor_label=major_label_of_set1)
        
        return decisionnode(feature=split_feat, value=split_val, truebranch=true_branch, falsebranch=false_branch)
        
        
    def printTree(self, indent=''):
        node = self.root
        if node.label != None:
            print str(node.label)
        else:
            print 'row[' + str(node.feature) + ']>=' + str(node.value) + '? '
    
            print indent + 'T->',
            self.printTree(node.truebranch, indent + '  ')
            print indent + 'F->',
            self.printTree(node.falsebranch, indent + '  ')
            
        