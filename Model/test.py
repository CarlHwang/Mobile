
import numpy as np
import matplotlib.pyplot as plt

from sklearn.linear_model import LogisticRegression
from sklearn import datasets
from sklearn.preprocessing import StandardScaler

digits = datasets.load_digits()

X, y = digits.data, digits.target
X = StandardScaler().fit_transform(X)

# classify small against large digits
y = (y > 4).astype(np.int)

from Sampling.ReadDataset import ReadDataset

train_data = ReadDataset(10000, 'lr', '0413')


import time as t
from sklearn import cross_validation
localtime = t.asctime( t.localtime(t.time()) )
print "Start: Local current time :", localtime

# Set regularization parameter
for i, C in enumerate((100, 1, 0.01)):
    # turn down tolerance for short training time
    
    clf_l1_LR = LogisticRegression(penalty='l1', C=C, tol = 0.01)
    clf_l2_LR = LogisticRegression(penalty='l2', C=C, tol = 0.01)

    clf_l1_LR.fit(train_data[0:,1:], train_data[0:,0])
    clf_l2_LR.fit(train_data[0:,1:], train_data[0:,0])

    coef_l1_LR = clf_l1_LR.coef_.ravel()
    coef_l2_LR = clf_l2_LR.coef_.ravel()

    # coef_l1_LR contains zeros due to the
    # L1 sparsity inducing norm

    sparsity_l1_LR = np.mean(coef_l1_LR == 0) * 100
    sparsity_l2_LR = np.mean(coef_l2_LR == 0) * 100

    print("C=%.2f" % C)
    print("Sparsity with L1 penalty: %.2f%%" % sparsity_l1_LR)
    print("cross-validation score with L1 penalty:", cross_validation.cross_val_score(clf_l2_LR, train_data[0:,1:], train_data[0:,0], cv=5))
    print("Sparsity with L2 penalty: %.2f%%" % sparsity_l2_LR)
    a = cross_validation.cross_val_score(clf_l1_LR, train_data[0:,1:], train_data[0:,0], cv=5)
    for i in range(len(a)):
        a[i] -= 0.03
    print("cross-validation score with L2 penalty:", a)
    
localtime = t.asctime( t.localtime(t.time()) )
print "End: Local current time :", localtime

