#! /usr/bin/env python
# -*- coding:utf-8 -*-


SplitHour = 720

def behaviorStr(behavior):
    if behavior == '1':
        return 'click'
    elif behavior == '2':
        return 'collect'
    elif behavior == '3':
        return 'cart'
    elif behavior == '4':
        return 'deal'
    
def hasGapBetween(gaps, lowerbound, upperbound, lowerinclude=False):
    if lowerinclude:
        lowerbound -= 1
    for gap in gaps:
        if lowerbound < gap and gap <= upperbound:
            return True
    return False
    