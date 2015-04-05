#! /usr/bin/env python
# -*- coding:utf-8 -*-

class decisionnode:
    def __init__(self, feature=-1, value=None, label=None, truebranch=None, falsebranch=None):
        self.feature=feature
        self.value=value
        self.label=label
        self.truebranch = truebranch
        self.falsebranch = falsebranch