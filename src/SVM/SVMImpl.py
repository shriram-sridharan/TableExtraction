'''
Created on Dec 9, 2012

@author: shriram
'''
from Utils.SparseType import SparseType
from SVMFeatures import SVMFeatures
from PyML import SVM
from PyML import SparseDataSet
from SVM.SVMTDFeatures import SVMTDFeatures

class SVMImpl:
    def __init__(self):
        self.Features = SVMFeatures()
        self.TDFeatures = SVMTDFeatures()
        self.svminstance = SVM()
        
    def domaintrain(self, annotatedxmllist):
        datalist = list()
        labelslist = list()
        for annotatedxml in annotatedxmllist:
            for page in annotatedxml[0]:
                for col in page:
                    if(len(col) < 2):
                        continue
                    for tup in col:
                        if(tup[1].text is None or tup[1].text.strip() == ''):
                            col.remove(tup)
                    for i in xrange(0, len(col)):
                        if(int(col[i][0]) == SparseType.TABLELINE):
                            labelslist.append("S")
                        else:
                            labelslist.append("NS")
                        datalist.append(self.Features.domainfindfeatureFunction(i, col, annotatedxml[1]))
        self.train(datalist, labelslist)
    
    def domaintrainforTableDecomposition(self, tableslist):
        labelslist = list()
        datalist = list()
        for table in tableslist:
            for i in xrange(0, len(table)):
                if(int(table[i][0]) == SparseType.HEADER):
                    labelslist.append("HEADER")
                else:
                    labelslist.append("DATA")
                datalist.append(self.TDFeatures.domainfindfeatureFunction(i, table, None))
        self.trainforTD(datalist, labelslist)
        
    def domainpredictforTableDecomposition(self, table): 
        for i in xrange(0, len(table)):
            test_list = list()
            test_list.append(self.TDFeatures.domainfindfeatureFunction(i, table, None)) 
            if(self.predict(test_list) == 'HEADER'):
                table[i][0] = SparseType.HEADER
            else:
                table[i][0] = SparseType.DATA
        return table
               
    def domainpredict(self, col, fontdict):
        errorcount = 0
        sparseerror = 0
        for i in xrange(0, len(col)):
            test_list = list()
            test_list.append(self.Features.domainfindfeatureFunction(i, col, fontdict)) 
            if(self.predict(test_list) == 'S'):
                predicted = SparseType.TABLELINE
            else:
                predicted = SparseType.NONTABLELINE
            if((predicted) != int(col[i][0])):
                errorcount += 1 
                if((predicted) == SparseType.NONTABLELINE):
                    sparseerror += 1
            col[i][0] = predicted
        
        return [col, errorcount, sparseerror]
        
    def train(self, datalist, labelslist):    
        data = SparseDataSet(datalist, L = labelslist)
        self.svminstance.C = 20
        data.attachKernel('gaussian', degree = 5)
        self.svminstance.train(data)
        #result = self.svminstance.cv(data, 5)
        #print result
        
    def trainforTD(self, datalist, labelslist):    
        data = SparseDataSet(datalist, L = labelslist)
        self.svminstance.train(data)
        result = self.svminstance.cv(data, 6)
        print result    
        
    def predict(self, datalist):
        data = SparseDataSet(datalist)
        results = self.svminstance.test(data)
        return results.getPredictedLabels()[0]
    
    def save(self, filename):
        self.svminstance.save(filename)

    
