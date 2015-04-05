#! /usr/bin/env python
# -*- coding:utf-8 -*-

# Auther: Carl Hwang
# Date: 2015-4-5

import random
from Model.dtree import DecisionTree


'''
    three things:
    1. boostrap
    2. oob
    3. feature importance
'''

class RandomForest():
    
    def __init__(self, 
                dataset, 
                boostrap_size, 
                num_tree=500, 
                criterion='gini',
                min_sample_split=5, 
                err_function='mse',
                max_depth=None): 
        
        self.num_tree = num_tree
        self.err_function = err_function
        self.forest = []
        self.boostraped = []
        self.bagging_table = None
        self.criterion = criterion
        self.buildrandomforest(dataset, min_sample_split, max_depth)
        
        
    def Boostrap(self, dataset, boostrap_size):
        
        size_dataset = len(dataset)
        self.bagging_table = [[0]*size_dataset]*self.num_tree
        
        for i in range(self.num_tree):
            subset = []
            
            for j in range(boostrap_size):
                rand_index = random.randint(0, size_dataset-1)
                subset.append(dataset[rand_index])
                self.bagging_table[i][j] = 1
                
            yield subset    # yield a subset
        
        
    def buildRandomForest(self, dataset, boostrap_size, min_sample_split=5, max_depth=None):
        for subset in self.boostrap(dataset, boostrap_size):
            decision_tree = DecisionTree(subset, self.criterion, min_sample_split, max_depth)
            self.forest.append(decision_tree)
            
    
    def squareError(self, label, predicted):
        return (label-predicted) ** 2
    
            
    def getOutOfBagTrees(self, sample_index):
        for tree_index in range(len(self.bagging_table)):
            if not self.bagging_table[tree_index][sample_index] == 1:
                yield tree_index


    def getOutOfBagSamples(self, tree_index):
        for sample_index in range(len(self.bagging_table[0])):
            if not self.bagging_table[tree_index][sample_index] == 1:
                yield sample_index
                
    
    def doFeaturePermutaion(self, dataset, samples, feature_index):
        permuted_set = dataset[:]   #deep copy
        data = []
        for sample_index in samples:
            data.append(permuted_set[sample_index][feature_index])
            
        random.shuffle(data)
        
        for shuffle_index in range(data):
            sample_index = samples[shuffle_index]
            permuted_set[sample_index][feature_index] = data[shuffle_index]
            
        return permuted_set
    
         
    def outOfBagErrorPermuted(self, dataset, feature_index):
        '''
        @note: by CARL
        
        Complicated!!! 
        
        in order to do feature importance computation, we user an equation as:
        importance(i) = Eoob(G) - Eoob_p(G).
        for each sample on G, minimizing sum of error of each tree prediction.
        Eoob_p(G) denotes that the Eoob on a new dataset G, with random sample 
        permutation on feature i over all the samples have not been bagged in 
        the particular tree
        
        the for loop is originally like below:
        -------------------------
        
        for sample_index in range(size_dataset):
            
            sum_predicted = 0
            num_tree = 0
            
            for out_of_bag_tree_index in self.getOutOfBagTrees(sample_index):
            
                ''
                a sample only used to validate on the tree that have not bagged it
                for this tree, we find other samples that also have not been bagged,
                then do permutation on feature i over all this samples.
                ''
                
                out_of_bag_samples = [sample_index for sample_index in self.getOutOfBagSamples(tree_index)]
                    
                permuted_set = self.doFeaturePermutaion(dataset, out_of_bag_samples, feature_index)
                
                vec = permuted_set[sample_index]
                label = vec[-1] # sample labe
                
                sum_predicted += self.forest[out_of_bag_tree_index].classify(vec[:-1])
        -------------------------
        
        the innerest loop must be calculate first because the prediction
        is based on the average value of trees. But in order to calculate
        based on a tree is required to find other samples, it shows a 
        sample - tree - sample struct, it is not easy understandable,
        beyond that, it requires to do permutation O(N*T) while N denotes
        the sample scale and T denotes the tree scale.
        
        So I adjust the inner and outer loop, user a container to maintain
        the have-not-been-sum prediction value, reverse the objection of 
        inner and outer loop. And calculate the sum at the end. With this
        improve, the permutation time reduced to O(T).
                
        '''
        
        maintainence = []
        
        for tree_index in range(self.num_tree):
            
            out_of_bag_samples = [sample_index for sample_index in self.getOutOfBagSamples(tree_index)]
                    
            permuted_set = self.doFeaturePermutaion(dataset, out_of_bag_samples, feature_index)
            
            for sample_index in out_of_bag_samples:
                vec = permuted_set[sample_index]
                label = vec[-1] # sample label
                maintainence.append( {sample_index : self.forest[tree_index].classify(vec[:-1])} )
        
        Eoob = 0.0        
        size_dataset = len(dataset)
        
        for sample_index in range(size_dataset):
            
            sum_predicted = 0
            num_tree = 0
            
            for tree in maintainence:
                if sample_index in tree.keys():
                    sum_predicted += tree[sample_index]
                    num_tree += 1
                    
            if num_tree == 0:
                continue
            
            predicted = int(float(sum_predicted) / num_tree + 0.5)
            
            err = 0.0
            if self.err_function == 'mse':
                err = self.squareerror(label, predicted)
                
            Eoob += err
        
        return Eoob /  size_dataset
                
    
    def outOfBagError(self, dataset):
        size_dataset = len(dataset)
        
        Eoob = 0.0
        for sample_index in range(size_dataset):
            vec = dataset[sample_index]
            label = vec[-1] # sample labe
            
            sum_predicted = 0
            num_tree = 0
            
            for out_of_bag_tree_index in self.getoutofbagtrees(sample_index):
                sum_predicted += self.forest[out_of_bag_tree_index].classify(vec[:-1])
                num_tree += 1
                
            if num_tree == 0:
                continue
            
            predicted = int(float(sum_predicted) / num_tree + 0.5)
            
            err = 0.0
            if self.err_function == 'mse':
                err = self.squareerror(label, predicted)
                
            Eoob += err
            
        return Eoob / size_dataset
    
    
    def calFeatureImportance(self, dataset):
        importance = []
        for feature_index in range(dataset[0] - 1):
            importance.append(self.outOfBagErrorPermuted(dataset, feature_index))
            
            
    '''
    #
    #    TO BE CONSIDERED LATER
    #
    '''
    
    def featureprojection(self, dataset):
        ''' project the feature vector to any space '''
        pass
    