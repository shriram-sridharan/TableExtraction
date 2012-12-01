'''
Created on Nov 29, 2012

@author: shriram
'''
import random
import sys
from SparseType import SparseType
from Constants import Constants

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
    
    def domaintrain(self, annotatedxmllist):
        collist = list()
        for annotatedxml in annotatedxmllist:
            for page in annotatedxml:
                for col in page:
                    if(len(col) < 2):
                        continue
                    trainfeatures = list()
                    for i in xrange(0, len(col)):
                        trainfeatures.append(self.domainfindfeatureFunction(i, col))
                    collist.append([col, trainfeatures])
        self.train(collist)
    
    def domainfindfeatureFunction(self, i, col, prevtag = None, curtag = None):
        featurelist = list()
        if(prevtag is None):
            prevtag = int(col[i-1][0])
        if(curtag is None):
            curtag = int(col[i][0])
            
        if(i!=0 and prevtag == SparseType.OTHERSPARSE and curtag == SparseType.OTHERSPARSE):
            featurelist.append(1)
        else:
            featurelist.append(0)
        
        if(i!=0 and prevtag == SparseType.OTHERSPARSE and curtag == SparseType.NONSPARSE):
            featurelist.append(1)
        else:
            featurelist.append(0)
        
        if(i!=0 and prevtag == SparseType.NONSPARSE and curtag == SparseType.OTHERSPARSE):
            featurelist.append(1)
        else:
            featurelist.append(0)
        
        if(i!=0 and prevtag == SparseType.NONSPARSE and curtag == SparseType.NONSPARSE):
            featurelist.append(1)
        else:
            featurelist.append(0)
               
        if(int(col[i][1].attrib['textpieces']) > 0 and curtag == SparseType.OTHERSPARSE):
            featurelist.append(1)
        else:
            featurelist.append(0)
        
        if((int(col[i][1].attrib['font']) == int(col[i-1][1].attrib['font'])) and curtag == SparseType.OTHERSPARSE 
                            and prevtag == SparseType.OTHERSPARSE):
            featurelist.append(1)
        else:
            featurelist.append(0)
            
        return featurelist
    
    def train(self, collist):
        for _ in xrange(len(collist[0][1][0])):
            self.trainedweights.append(random.uniform(-0.02,0.02))
            
        for _ in xrange(0,1000):
            errorcount = 0.0
            totaltup = 0.0
            for tup in collist:
                print self.trainedweights
                errorcount += self.learnparameters(tup[0], tup[1], self.trainedweights)
                print self.trainedweights
                totaltup += len(tup[0])
            print errorcount/totaltup
            
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
    
    def learnweightsBySG(self, predictedsequence, col, trainedweights, trainfeatures):
        negativecol = list()
        errorcount = 0.0
        for tup in xrange(len(col)):
            if((predictedsequence[tup]+1) != int(col[tup][0])): # +1 because index starts at 0 but sparsetype starts at 1
                errorcount += 1
            negativecol.append([predictedsequence[tup]+1, col[tup][1]])
            
        predictedfeatures = list()
        for i in xrange(0, len(col)):
            predictedfeatures.append(self.domainfindfeatureFunction(i, negativecol))
        
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
            trainedweights[floc] = trainedweights[floc] + Constants.LEARNING_RATE * (FActuallist[floc] - FPredictedlist[floc]) 
        
        return errorcount
        
    def learn(self, col, tagbyumatrix, trainfeatures, trainedweights):
        predictedsequence = self.predictsequence(tagbyumatrix)
        seq = ''
        for r in predictedsequence:
            if(r == 0):
                seq += " S"
            else:
                seq += " NS"
        print seq
        seq = ''
        for r in xrange(len(col)):
            if(int(col[r][0]) == 1):
                seq += " S"
            else:
                seq += " NS"
        print seq
        return self.learnweightsBySG(predictedsequence, col, trainedweights, trainfeatures, )
    
    
    def learnparameters(self, col, trainfeatures, trainedweights):
        tagbyumatrix = self.GetMatrixForCalculatingArgMax(col, trainfeatures, trainedweights)
        #marginalprobabilityofinput = self.GetZValue(col, trainfeatures, trainedweights) #Not needed for Collins Perceptron
        return self.learn(col, tagbyumatrix, trainfeatures, trainedweights)

    def GetMatrixForCalculatingArgMax(self, col, trainfeatures, trainedweights):
        gmatrices = self.buildGMatrices(col, trainfeatures, trainedweights)
        return self.calculateUMatrixByVitterbi(col, gmatrices)
    
    def buildGMatrices(self, col, trainfeatures, trainedweights):
        gmatrices = list() #[G1, G2......], G2 => [[[w1f1 + w2f2], row0col1, row0col2], [row1col0,  ], ....]
        gmatrices.append(self.G1)
        for line in xrange(1, len(col)):
            gmatrix = list()
            for curtag in self.possibletags:
                collist = list()
                for prevtag in self.possibletags:
                    sigma = 0
                    featurelist = self.domainfindfeatureFunction(line, col, prevtag, curtag)
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
                    
                
              
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
    
    