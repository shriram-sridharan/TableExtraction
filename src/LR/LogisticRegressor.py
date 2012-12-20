'''
Created on Dec 9, 2012

@author: shriram
'''
import math
import random
from LRFeatures import LRFeatures
from Utils.SparseType import SparseType
from Utils.Constants import Constants
from LRTDFeatures import LRTDFeatures

class LogisticRegressor:
    def __init__(self, trainedweights = list()):
        self.Features = LRFeatures()
        self.TDFeatures = LRTDFeatures()
        self.trainedweights = trainedweights
        self.learningrate = Constants.LR_LEARNING_RATE
                
    def domaintrain(self, annotatedxmllist):
        collist = list()
        for annotatedxml in annotatedxmllist:
            for page in annotatedxml[0]:
                for col in page:
                    if(len(col) < 2):
                        continue
                    for tup in col:
                        if(tup[1].text is None or tup[1].text.strip() == ''):
                            col.remove(tup)
                    trainfeatures = list()
                    for i in xrange(0, len(col)):
                        trainfeatures.append(self.Features.domainfindfeatureFunction(i, col, annotatedxml[1]))
                    collist.append([col, trainfeatures])
        self.train(collist)
        
    def domainpredict(self, col, fontdict):
        errorcount = 0
        sparseerror = 0
        for i in xrange(0, len(col)):
            featurevector = self.Features.domainfindfeatureFunction(i, col, fontdict)
            predicted = self.predict(featurevector)
            if((predicted) != int(col[i][0])):
                errorcount += 1 
                if((predicted) == SparseType.NONTABLELINE):
                    sparseerror += 1
            col[i][0] = predicted
            
        return [col,errorcount, sparseerror]
    
    def domaintrainforTableDecomposition(self, tableslist):
        datalist = list()
        labelslist = list()
        for table in tableslist:
            for i in xrange(0, len(table)):
                labelslist.append(table[i][0])
                datalist.append(self.TDFeatures.domainfindfeatureFunction(i, table, None))
        self.trainforTD(datalist, labelslist)
        
    def domainpredictforTableDecomposition(self, table): 
        errorcount = 0
        sparseerror = 0
        for i in xrange(0, len(table)):
            test_list = self.TDFeatures.domainfindfeatureFunction(i, table, None) 
            predicted = self.predictforTD(test_list)
            if((predicted) != int(table[i][0])):
                errorcount += 1 
                if((predicted) == SparseType.HEADER):
                    sparseerror += 1
            table[i][0] = predicted
        return [table, errorcount, sparseerror]
                
    def predict(self, featurevector):
        sigmoid = self.getSigmoid(featurevector, self.trainedweights)
        if(sigmoid > 0.5):
            return SparseType.TABLELINE
        return SparseType.NONTABLELINE
    
    def predictforTD(self, featurevector):
        sigmoid = self.getSigmoid(featurevector, self.trainedweights)
        if(sigmoid > 0.5):
            return SparseType.HEADER
        return SparseType.DATA
    
    def trainforTD(self, datalist, labelslist):
        self.trainedweights = list()
        for _ in xrange(len(datalist[0])):
            self.trainedweights.append(random.uniform(-0.1, 0.1))
        for r in range(Constants.LR_EPOCHS):
            errorcount = 0.0
            sparseerrorcount = 0.0
            totalcount = 0.0
            for datarow in xrange(len(datalist)):
                totalcount += 1
                sigmoidExpected = 0
                inputVector = datalist[datarow]
                if(int(labelslist[datarow]) == SparseType.HEADER):
                    sigmoidExpected = 1
                self.stochasticGradientDescent(inputVector, self.trainedweights, sigmoidExpected, self.learningrate);
                predicted = self.predictforTD(inputVector)
                if(predicted != int(labelslist[datarow])):
                    errorcount += 1
                    if(int(labelslist[datarow]) == SparseType.HEADER): #for sparse error count # domain specific 
                        sparseerrorcount += 1
                            
            self.learningrate = Constants.INITIAL_LEARNING_RATE * math.exp(-(float(r)/Constants.CRF_NUM_EPOCHS))                 
            print "Iteration " + str(r) + " Learning Rate " + str(self.learningrate) + " Count= " + str(totalcount) +" Total Error = " + str(errorcount) + " Sparse Error = " + str(sparseerrorcount)

    def train(self, collist):
        self.trainedweights = list()
        for _ in xrange(len(collist[0][1][0])):
            self.trainedweights.append(random.uniform(-0.1, 0.1))
        for r in range(Constants.LR_EPOCHS):
            errorcount = 0.0
            sparseerrorcount = 0.0
            totalcount = 0.0
            for colnum in range(len(collist)):
                for lineno in xrange(len(collist[colnum][0])):
                    totalcount += 1
                    sigmoidExpected = 0
                    inputVector = collist[colnum][1][lineno]
                    if(int(collist[colnum][0][lineno][0]) == SparseType.TABLELINE):
                        sigmoidExpected = 1
                    self.stochasticGradientDescent(inputVector, self.trainedweights, sigmoidExpected, self.learningrate);
                    predicted = self.predict(inputVector)
                    if(predicted != int(collist[colnum][0][lineno][0])):
                        errorcount += 1
                        if(int(collist[colnum][0][lineno][0]) == SparseType.TABLELINE): #for sparse error count # domain specific 
                            sparseerrorcount += 1
                            
            self.learningrate = Constants.INITIAL_LEARNING_RATE * math.exp(-(float(r)/Constants.CRF_NUM_EPOCHS))                 
            print "Iteration " + str(r) + " Learning Rate " + str(self.learningrate) + " Count= " + str(totalcount) +" Total Error = " + str(errorcount) + " Sparse Error = " + str(sparseerrorcount)

    def stochasticGradientDescent(self,inputVector, weightVector, sigmoidExpected, eta):
        sigmoid = self.getSigmoid(inputVector, weightVector)
        #update weights
        for r in range(len(weightVector)):
            weightVector[r] = weightVector[r] + eta*(sigmoidExpected - sigmoid)*sigmoid*(1-sigmoid)*inputVector[r]
    
    def getSigmoid(self,inputVector, weightVector):
        net = 0
        for r in range(len(inputVector)):
            net = net + inputVector[r]*weightVector[r]
        sigmoid = 1/(1+math.exp(-net))
        return sigmoid
