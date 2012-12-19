'''
Created on Dec 9, 2012

@author: shriram
'''
from Utils.SparseType import SparseType
from SVMFeatures import SVMFeatures
from PyML import SVM
from PyML import SparseDataSet

class SVMImpl:
    def __init__(self):
        self.Features = SVMFeatures()
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
        
    def domainpredict(self, col, fontdict):
        for i in xrange(0, len(col)):
            test_list = list()
            test_list.append(self.Features.domainfindfeatureFunction(i, col, fontdict)) 
            if(self.predict(test_list) == 'S'):
                col[i][0] = SparseType.TABLELINE
            else:
                col[i][0] = SparseType.NONTABLELINE
        return col
        
    def train(self, datalist, labelslist):    
        data = SparseDataSet(datalist, L = labelslist)
        self.svminstance.C = 20
        data.attachKernel('gaussian', degree = 5)
        self.svminstance.train(data)
        result = self.svminstance.cv(data, 5)
        print result
        #print result.getPredictedLabels()
        
    def predict(self, datalist):
        data = SparseDataSet(datalist)
        results = self.svminstance.test(data)
        return results.getPredictedLabels()[0]
    
    def save(self, filename):
        self.svminstance.save(filename)
        
        
        