'''
Created on Nov 29, 2012

@author: shriram
'''
import random
import sys
from SparseType import SparseType
from Constants import Constants
from Features import Features
'''
    Implementing the Collins Perceptron for Learning parameters. Assuming a prob of 1 to predicted value.
    
    #collist ->list of [observation sequence, features] tuples
    #col -> observation sequence <Sparsetype, texttag>
    #trainfeatures -> list of feature values
    #trainweights -> corresponding list of weights 
'''
class CRF:

    def __init__(self):
        self.trainedweights = list()
        self.START = -1
        self.possibletags = [SparseType.OTHERSPARSE, SparseType.NONSPARSE] #domain specific
        self.G1 = [0.01,0.99] #domain specific
        self.Features = Features()
        self.differenceweights = list()
        
    
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
                    collist.append([col, trainfeatures, annotatedxml[1]])
        self.train(collist)
    
    def train(self, collist):
        for _ in xrange(len(collist[0][1][0])):
            self.trainedweights.append(random.uniform(-0.001, 0.001))
            self.differenceweights.append(0.0)
            
        for r in xrange(0,Constants.NUM_EPOCHS):
            errorcount = 0.0
            totaltup = 0.0
            sparseerrorcount = 0.0
            
            for tup in collist:
                errors = self.learnparameters(tup[0], tup[1], self.trainedweights, tup[2])
                errorcount += errors[0]
                sparseerrorcount += errors[1]
                totaltup += len(tup[0])
                
            for weight in xrange(len(self.trainedweights)):
                self.differenceweights[weight] /= len(collist)
                self.trainedweights[weight] = self.trainedweights[weight] + self.differenceweights[weight]
                self.differenceweights[weight] = 0.0
                
            print "Error : Iteration " + str(r) + " Total Error = " + str(errorcount) + " Sparse Error = " + str(sparseerrorcount)
            
    def predict(self, col, fontdict):
        tagbyumatrix = self.GetMatrixForCalculatingArgMax(col, self.trainedweights, fontdict)
        predicted = self.predictsequence(tagbyumatrix)
        for i in xrange(len(col)):
            col[i][0] = predicted[i] + 1
        
        return col

    def predictsequence(self, tagbyumatrix):
        prevvalue = -sys.maxint - 1
        nextpointer = 0
        highindex = 0
        sequence = list()
        for index in xrange(len(self.possibletags)):
            curvalue = tagbyumatrix[len(tagbyumatrix)-1][index][0]
            if(curvalue > prevvalue):
                prevvalue = curvalue
                nextpointer = tagbyumatrix[len(tagbyumatrix)-1][index][1]
                highindex = index
                
        sequence.append(highindex)
        sequence.append(nextpointer)    
        for r in reversed(xrange(1, len(tagbyumatrix)-1)):
            sequence.append(tagbyumatrix[r][nextpointer][1])
        
        return list(reversed(sequence))
    
    def learnweightsBySG(self, predictedsequence, col, trainedweights, trainfeatures, fontdict):
        negativecol = list()
        errorcount = 0.0
        sparseerrorcount = 0.0
        for tup in xrange(len(col)):
            if((predictedsequence[tup]+1) != int(col[tup][0])): # +1 because index starts at 0 but sparsetype starts at 1
                errorcount += 1
                if((predictedsequence[tup]+1) == SparseType.NONSPARSE): #for sparse error count # domain specific 
                    sparseerrorcount += 1
            negativecol.append([predictedsequence[tup]+1, col[tup][1]])
            
        predictedfeatures = list()
        for i in xrange(0, len(col)):
            predictedfeatures.append(self.Features.domainfindfeatureFunction(i, negativecol, fontdict))
        
        FActuallist = list() 
        FPredictedlist = list()
        for floc in xrange(len(predictedfeatures[0])):
            TF = 0
            PF = 0
            for featurevecloc in xrange(len(predictedfeatures)):
                TF += trainfeatures[featurevecloc][floc]
                PF += predictedfeatures[featurevecloc][floc]
            FActuallist.append(TF)
            FPredictedlist.append(PF)
        
        for floc in xrange(len(predictedfeatures[0])):  #wi = wi + alpha(Fjactual - Fjpredicted)
            self.differenceweights[floc] += Constants.LEARNING_RATE * (FActuallist[floc] - FPredictedlist[floc]) 
        
        return [errorcount, sparseerrorcount]
        
    def learn(self, col, tagbyumatrix, trainfeatures, trainedweights, fontdict):
        predictedsequence = self.predictsequence(tagbyumatrix)
#        seq = ''
#        for r in predictedsequence:
#            if(r == 0):
#                seq += " S"
#            else:
#                seq += " NS"
#        print "PREDICTED : " + seq
#        seq = ''
#        for r in xrange(len(col)):
#            if(int(col[r][0]) == 1):
#                seq += " S"
#            else:
#                seq += " NS"
#        print "ACTUAL    : " + seq
        return self.learnweightsBySG(predictedsequence, col, trainedweights, trainfeatures, fontdict)
    
    def learnparameters(self, col, trainfeatures, trainedweights, fontdict):
        tagbyumatrix = self.GetMatrixForCalculatingArgMax(col, trainedweights, fontdict)
        #marginalprobabilityofinput = self.GetZValue(col, trainfeatures, trainedweights) #Not needed for Collins Perceptron
        return self.learn(col, tagbyumatrix, trainfeatures, trainedweights, fontdict)

    def GetMatrixForCalculatingArgMax(self, col, trainedweights, fontdict):
        gmatrices = self.buildGMatrices(col, trainedweights, fontdict)
        return self.calculateUMatrixByVitterbi(col, gmatrices)
    
    def buildGMatrices(self, col, trainedweights, fontdict):
        gmatrices = list() #[G1, G2......], G2 => [[[w1f1 + w2f2], row0col1, row0col2], [row1col0,  ], ....]
        gmatrices.append(self.G1)
        for line in xrange(1, len(col)):
            gmatrix = list()
            for curtag in self.possibletags:
                collist = list()
                for prevtag in self.possibletags:
                    sigma = 0
                    featurelist = self.Features.domainfindfeatureFunction(line, col, fontdict, prevtag, curtag)
                    for feat in xrange(len(trainedweights)):
                        sigma = sigma + featurelist[feat] * trainedweights[feat]
                    collist.append(sigma)
                gmatrix.append(collist)
            gmatrices.append(gmatrix)
        return gmatrices
        
    #U(k,v) = max(yk -1) [U(k-1,yk-1) + gk(yk-1,v)]        
    def calculateUMatrixByVitterbi(self, col, gmatrices):
        umatrix = list() #[[],[value ,prevmax]]
        umatrix.append([[self.G1[0], self.START], [self.G1[1], self.START]])
        for index in xrange(1, len(col)):
            rowlist = list()
            for currenttag in xrange(0, len(self.possibletags)):
                gmatrix = gmatrices[index]
                prevvalue = -sys.maxint - 1
                prevtagbackpointer = 0
                for prevtag in xrange(0, len(self.possibletags)):
                    curvalue = umatrix[index-1][prevtag][0] + gmatrix[prevtag][currenttag]
                    if(curvalue > prevvalue):
                        prevvalue = curvalue
                        prevtagbackpointer = prevtag
                rowlist.append([prevvalue, prevtagbackpointer])
            umatrix.append(rowlist)
        return umatrix 
                    
                
              
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
    
    