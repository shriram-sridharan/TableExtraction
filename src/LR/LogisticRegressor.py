'''
Created on Dec 9, 2012

@author: shriram
'''
import math
import random
from LRFeatures import LRFeatures
from Utils.SparseType import SparseType
from Utils.Constants import Constants

class LogisticRegressor:
    def __init__(self, trainedweights = list()):
        self.Features = LRFeatures()
        self.trainedweights = trainedweights
        self.learningrate = Constants.LR_LEARNING_RATE
                
    def domaintrain(self, annotatedxmllist):
        collist = list()
        for annotatedxml in annotatedxmllist:
            for page in annotatedxml[0]:
                for col in page:
                    if(len(col) < 2):
                        continue
                    trainfeatures = list()
                    for i in xrange(0, len(col)):
                        trainfeatures.append(self.Features.domainfindfeatureFunction(i, col, annotatedxml[1]))
                    collist.append([col, trainfeatures])
        self.train(collist)
        
    def domainpredict(self, col, fontdict):
        for i in xrange(0, len(col)):
            featurevector = self.Features.domainfindfeatureFunction(i, col, fontdict)
            col[i][0] = self.predict(featurevector)
        return col
                
    def predict(self, featurevector):
        sigmoid = self.getSigmoid(featurevector, self.trainedweights)
        if(sigmoid > 0.5):
            return SparseType.OTHERSPARSE
        return SparseType.NONSPARSE
    
    def train(self, collist):
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
                    if(int(collist[colnum][0][lineno][0]) == SparseType.OTHERSPARSE):
                        sigmoidExpected = 1
                    self.stochasticGradientDescent(inputVector, self.trainedweights, sigmoidExpected, self.learningrate);
                    predicted = self.predict(inputVector)
                    if(predicted != int(collist[colnum][0][lineno][0])):
                        errorcount += 1
                        if(int(collist[colnum][0][lineno][0]) == SparseType.OTHERSPARSE): #for sparse error count # domain specific 
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
