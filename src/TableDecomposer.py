'''
Created on Dec 19, 2012

@author: shriram
'''
import Utils.Trainer
from SVM.SVMImpl import SVMImpl
from Utils.SparseType import SparseType
from LR.LogisticRegressor import LogisticRegressor

def TrainUsingSVM(xmls, annotatedxmlloc):
    svm = SVMImpl()
    trainer = Utils.Trainer.Trainer()
    tableslist = list()
    for xml in xmls:
        tableslist.append(trainer.readAnnotatedxmlforTableDecomposition(annotatedxmlloc + xml + "_TD_ANNOTATED"))
    
    svm.domaintrainforTableDecomposition(tableslist) 
    return svm

def TestUsingSVM(svminstance, xml, location):
    trainer = Utils.Trainer.Trainer()
    table = trainer.readAnnotatedxmlforTableDecomposition(location + xml)
    result = svminstance.domainpredictforTableDecomposition(table)
    predicted = result[0]
    errorcount = result[1]
    sparseerror = result[2]
    
    for r in predicted:
        if(r[0] == SparseType.HEADER):
            print r[1].text + "***** HEADER *****"
        else:
            print r[1].text + "***** DATA *****"
            
    return [errorcount, sparseerror]

def TrainUsingLR(xmls, annotatedxmlloc):
    LR = LogisticRegressor()
    trainer = Utils.Trainer.Trainer()
    tableslist = list()
    for xml in xmls:
        tableslist.append(trainer.readAnnotatedxmlforTableDecomposition(annotatedxmlloc + xml + "_TD_ANNOTATED"))
    
    LR.domaintrainforTableDecomposition(tableslist) 
    return LR

def TestUsingLR(LR, xml, location):
    trainer = Utils.Trainer.Trainer()
    table = trainer.readAnnotatedxmlforTableDecomposition(location + xml)
    predicted = LR.domainpredictforTableDecomposition(table)
    for r in predicted[0]:
        if(r[0] == SparseType.HEADER):
            print r[1].text + "***** HEADER *****"
        else:
            print r[1].text + "***** DATA *****"
    return [predicted[1],predicted[2]]
    
def CrossValidationLR():
    xmls = list()
    annotatedxmlloc = "../TrainingData/TDannotated/"
    location = "../TrainingData/TDannotated/"
    errorcount = 0
    sparseerror = 0
    start = 1
    end = 49
    for cv in xrange(0,6):
        trainlist = list()
        testlist = list()
        r = cv*8 + start
        testlist = range(r, r+8)
        trainlist = range(r+8, end)
        if(r!=1):
            for strange in range(1,r):
                trainlist.append(strange)
        
        for x in trainlist:
            xmls.append(str(x))
        LR = TrainUsingLR(xmls, annotatedxmlloc)
        
        for x in testlist:
            result = TestUsingLR(LR, str(x)+"_TD_ANNOTATED", location)
            errorcount+= result[0]
            sparseerror += result[1]
    
    print errorcount
    print sparseerror  

def CrossValidationSVM():
    xmls = list()
    annotatedxmlloc = "../TrainingData/TDannotated/"
    location = "../TrainingData/TDannotated/"
    errorcount = 0
    sparseerror = 0
    start = 1
    end = 49
    for cv in xrange(0,6):
        trainlist = list()
        testlist = list()
        r = cv*8 + start
        testlist = range(r, r+8)
        trainlist = range(r+8, end)
        if(r!=1):
            for strange in range(1,r):
                trainlist.append(strange)
        
        for x in trainlist:
            xmls.append(str(x))
        svminstance = TrainUsingSVM(xmls, annotatedxmlloc)
        
        for x in testlist:
            result = TestUsingSVM(svminstance, str(x)+"_TD_ANNOTATED", location)
            errorcount+= result[0]
            sparseerror += result[1]
    
    print errorcount
    print sparseerror  
if __name__ == '__main__':
    xmls = list()
    for r in xrange(1,49):
        xmls.append(str(r))
    annotatedxmlloc = "../TrainingData/TDannotated/"
    predictxml = "2_TD_ANNOTATED"
    location = "../TrainingData/TDannotated/"
    
    #CrossValidationLR()
    #CrossValidationSVM()
#    LR = TrainUsingLR(xmls, annotatedxmlloc)
#    TestUsingLR(LR, predictxml, location)
#    
#    svminstance = TrainUsingSVM(xmls, annotatedxmlloc)
#    TestUsingSVM(svminstance, predictxml, location)
    

    