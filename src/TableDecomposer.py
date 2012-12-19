'''
Created on Dec 19, 2012

@author: shriram
'''
import Utils.Trainer
from SVM.SVMImpl import SVMImpl
from Utils.SparseType import SparseType

def TrainUsingSVM(xmls, annotatedxmlloc):
    svm = SVMImpl()
    trainer = Utils.Trainer.Trainer()
    tableslist = list()
    for xml in xmls:
        tableslist.append(trainer.readAnnotatedxmlforTableDecomposition(annotatedxmlloc + xml + "_TD_annotated"))
    
    svm.domaintrainforTableDecomposition(tableslist) 
    return svm

def TestUsingSVM(svminstance, xml, location):
    trainer = Utils.Trainer.Trainer()
    table = trainer.readAnnotatedxmlforTableDecomposition(location + xml)
    predicted = svminstance.domainpredictforTableDecomposition(table)
    for r in predicted:
        if(r[0] == SparseType.HEADER):
            print r[1].text + "***** HEADER *****"
        else:
            print r[1].text + "***** DATA *****"
            
if __name__ == '__main__':
    xmls = ["1","2","3","4","5","6","7","8","9","10","11","12","13","14","15","16"]
    annotatedxmlloc = "../TrainingData/TDannotated/"
    svminstance = TrainUsingSVM(xmls, annotatedxmlloc)
    
    xml = "2_TD_annotated"
    location = "../TrainingData/TDannotated/"
    TestUsingSVM(svminstance, xml, location)
    

    