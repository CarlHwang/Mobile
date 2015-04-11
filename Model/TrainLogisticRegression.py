
from sklearn import linear_model
from sklearn.externals import joblib
from Sampling.ReadDataset import ReadDataset


def FitLogisticRegression(num_negative_sample, date):
    
    train_data = ReadDataset(num_negative_sample, 'lr', date)
    lr = linear_model.LogisticRegression(penalty='l2', C=350, max_iter=1000, solver='lbfgs', tol=0.001)
    lr = lr.fit(train_data[0:,1:], train_data[0:,0])
    joblib.dump(lr, './PersistModel/lr_' + str(num_negative_sample) + '_' + date + '.model')