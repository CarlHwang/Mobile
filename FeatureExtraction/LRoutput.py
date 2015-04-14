import csv
from Sampling.ReadDataset import ReadPredictDataset
from sklearn.externals import joblib
import itertools


def LRAvgCombPredict(date, model_set, LROutput, hours=24):
    #num_negative_samples = [10000,12000,14000,16000,18000,20000]
    avg_row = []
    
    key = ''
    
    test_data, id_set = ReadPredictDataset(hours, isWithID=True)
    print len(test_data)
 
    for i in range(len(model_set)):
        print str(model_set[i])
        lr = joblib.load('../Model/PersistModel/lr_' + str(model_set[i]) + '_' + date + '.model')
        result = lr.predict_proba(test_data)
        avg_row.append(result[:,1])
        key += str(model_set[i])
   
    avg = []
    for i in range(len(avg_row[0])):
        feature = []
        for j in range(len(avg_row)):
            feature.append(avg_row[j][i]) 
        avg.append(sum(feature)/len(feature))
    
        
    for i in range(len(id_set)):
        usid, itid = id_set[i][0], id_set[i][1]
        ui_id = usid + ' ' + itid   
        
        if not LROutput.get(ui_id):
            LROutput[ui_id] = []
        LROutput[ui_id].append(avg[i])
    

def LROutput(date, hours = 720):

    ui_lr_feature = {}
    num_negative_samples = [10000,10001,12000,12001,14000,16000,18000,20000]

    
    avg_subfeature_set = list(itertools.combinations(num_negative_samples,4))
    for row in avg_subfeature_set:
        print row
        LRAvgCombPredict(date, row, ui_lr_feature,hours)
               
    outfile = open('../csv/complex/LROutput.csv', 'wb')
    spamwriter = csv.writer(outfile, dialect = 'excel')
    
    for key in ui_lr_feature.keys():
        user_id = key.split()[0]
        item_id = key.split()[1]
        avg = ui_lr_feature[key]
        
        row = [user_id, item_id]
        row.extend(avg)
        spamwriter.writerow(row)
  
LROutput('0413')

