from CRF.CRF import CRF
import Processors.PreProcessor
import Processors.PostProcessor
import Utils.Trainer
import xml.etree.ElementTree as ET
from Utils.SparseType import SparseType
from LR.LogisticRegressor import LogisticRegressor
from SVM.SVMImpl import SVMImpl
import sys

def TrainUsingCRF(xmls, preprocessor, trainer, xmlloc, annotatedxmlloc):
    CRFImpl = CRF()
    annotatedxmllist = list()
    for xmlname in xmls:
        fontdict = preprocessor.getFontDictionary(ET.parse(xmlloc + xmlname + ".xml")) #list(pages), pages -> list(cols), col -> list(<Sparse/NonSparse, tag>)
        annotatedxml = trainer.readAnnotatedXml(annotatedxmlloc + xmlname + "_annotated")
        annotatedxmllist.append([annotatedxml, fontdict])
    
    CRFImpl.domaintrain(annotatedxmllist)
    print CRFImpl.trainedweights
    f = open("TrainedWeightsCRF", 'w')
    for weight in CRFImpl.trainedweights:
        f.write(str(weight) + "\n")
    
    f.close()
    
def TrainUsingLR(xmls, preprocessor, trainer, xmlloc, annotatedxmlloc):
    LRImpl = LogisticRegressor()
    annotatedxmllist = list()
    for xmlname in xmls:
        fontdict = preprocessor.getFontDictionary(ET.parse(xmlloc + xmlname + ".xml")) #list(pages), pages -> list(cols), col -> list(<Sparse/NonSparse, tag>)
        annotatedxml = trainer.readAnnotatedXml(annotatedxmlloc + xmlname + "_annotated")
        annotatedxmllist.append([annotatedxml, fontdict])
    
    LRImpl.domaintrain(annotatedxmllist)
    print LRImpl.trainedweights
    f = open("TrainedWeightsLR", 'w')
    for weight in LRImpl.trainedweights:
        f.write(str(weight) + "\n")
    
    f.close()

def TrainUsingSVM(xmls, preprocessor, trainer, xmlloc, annotatedxmlloc):
    svm = SVMImpl()
    annotatedxmllist = list()
    for xmlname in xmls:
        fontdict = preprocessor.getFontDictionary(ET.parse(xmlloc + xmlname + ".xml")) #list(pages), pages -> list(cols), col -> list(<Sparse/NonSparse, tag>)
        annotatedxml = trainer.readAnnotatedXml(annotatedxmlloc + xmlname + "_annotated")
        annotatedxmllist.append([annotatedxml, fontdict])
    
    svm.domaintrain(annotatedxmllist)
    return svm

    
def getModelwithTrainedWeights(isCRF = True):
    trainedweights = list()
    if(isCRF):
        f = open("TrainedWeightsCRF", "r")
        for weight in f:
            trainedweights.append(float(weight))
        
        f.close()
        CRFImpl = CRF(trainedweights)
        return CRFImpl
    else:
        f = open("TrainedWeightsLR", "r")
        for weight in f:
            trainedweights.append(float(weight))
        
        f.close()
        LR = LogisticRegressor(trainedweights)
        return LR

def TestUsingLR(predictxmlname, location):
    LR = getModelwithTrainedWeights(False)
             
    fontdict = preprocessor.getFontDictionary(ET.parse(location + predictxmlname + ".xml"))                  
    preprocessedxml = preprocessor.preprocessxml(location + predictxmlname + ".xml") #list(pages), pages -> list(cols), col -> list(<Sparse/NonSparse, tag>)
    
    alltables = list()
    errorcount = 0
    sparseerror = 0
    for page in preprocessedxml:
        for col in page:
            if(len(col) < 2):
                continue
            for tup in col:
                if(tup[1].text is None or tup[1].text.strip() == ''):
                    col.remove(tup)
            for lineno in xrange(len(col)):
                col[lineno].append(lineno)
            result = LR.domainpredict(col, fontdict)
            predicted = result[0]
            errorcount+= result[1]
            sparseerror += result[2]
#            for r in predicted:
#                if(r[0] == SparseType.OTHERSPARSE):
#                    print r[1].text + " *** Line no *** " + str(r[2])
            data = postprocessor.findTables(predicted)
            tables = data
            if(len(tables) == 0):
                continue
            for t in tables:
                alltables.append(t)
    
    for table in alltables:
        print "============================================="
        for row in table:
            print row[1].text.encode('ascii','ignore') + " " + str(row[0]) 
    
    print errorcount 
    print sparseerror    
    
    return [errorcount, sparseerror]
  
def CreateHtmls(xmls, preprocessor, trainer, xmlloc):
    for xmlname in xmls:
        try:
            preprocessedxml = preprocessor.preprocessxml(xmlloc + xmlname + ".xml") #list(pages), pages -> list(cols), col -> list(<Sparse/NonSparse, tag>)
            trainer.train(preprocessedxml, xmlname)
        except:
            print "Problem with " + xmlname, sys.exc_info()[0]

def TestUsingCRF(predictxmlname, location):
    CRF = getModelwithTrainedWeights()
    fontdict = preprocessor.getFontDictionary(ET.parse(location + predictxmlname + ".xml"))                  
    preprocessedxml = preprocessor.preprocessxml(location + predictxmlname + ".xml") #list(pages), pages -> list(cols), col -> list(<Sparse/NonSparse, tag>)
    
    alltables = list()
    errorcount = 0
    sparseerror = 0
    for page in preprocessedxml:
        for col in page:
            if(len(col) < 2):
                    continue
            for tup in col:
                if(tup[1].text is None or tup[1].text.strip() == ''):
                    col.remove(tup)
            for lineno in xrange(len(col)):
                col[lineno].append(lineno)
            
            result = CRF.predict(col, fontdict)
            predicted = result[0]
            errorcount += result[1]
            sparseerror += result[2]
#            for r in predicted:
#                if(r[0] == SparseType.OTHERSPARSE):
#                    print r[1].text.encode('ascii','ignore') + " *** Line no *** " + str(r[2])
            data = postprocessor.findTables(predicted)
            tables = data
            if(len(tables) == 0):
                continue
            for t in tables:
                alltables.append(t)

    for table in alltables:
        print "============================================="
        for row in table:
            print row[1].text.encode('ascii','ignore') + " " + str(row[0]) 
    
    return [errorcount, sparseerror]

def TestUsingSVM(svminstance, predictxmlname, location):
    fontdict = preprocessor.getFontDictionary(ET.parse(location + predictxmlname + ".xml"))                  
    preprocessedxml = preprocessor.preprocessxml(location + predictxmlname + ".xml") #list(pages), pages -> list(cols), col -> list(<Sparse/NonSparse, tag>)
    
    alltables = list()
    for page in preprocessedxml:
        for col in page:
            if(len(col) < 2):
                    continue
            for tup in col:
                if(tup[1].text is None or tup[1].text.strip() == ''):
                    col.remove(tup)
            for lineno in xrange(len(col)):
                col[lineno].append(lineno)
            predicted = svminstance.domainpredict(col, fontdict)
#            for r in predicted:
#                if(r[0] == SparseType.OTHERSPARSE):
#                    print r[1].text.encode('ascii','ignore') + " *** Line no *** " + str(r[2])
            data = postprocessor.findTables(predicted)
            tables = data
            if(len(tables) == 0):
                continue
            for t in tables:
                alltables.append(t)
    
    for table in alltables:
        print "============================================="
        for row in table:
            print row[1].text.encode('ascii','ignore') + " " + str(row[0]) 
   
def crossValidation():
    location = "../TrainingData/xmls/cs/"
    annotatedxmlloc = "../TrainingData/annotated/"
    errorcount = 0
    sparseerror = 0
    
    preprocessor = Processors.PreProcessor.PreProcessor()
    trainer = Utils.Trainer.Trainer()
    xmls = ["1","2","3","4","5","6","7","8","9","10"]
    TrainUsingCRF(xmls, preprocessor, trainer, location, annotatedxmlloc)
    for predictxmlname in ["11","12","13","14","15"]:
        error = TestUsingCRF(predictxmlname, location)
        errorcount += error[0]
        sparseerror += error[1]
    
    preprocessor = Processors.PreProcessor.PreProcessor()
    trainer = Utils.Trainer.Trainer()
    xmls = ["11","12","13","14","15","6","7","8","9","10"]
    TrainUsingCRF(xmls, preprocessor, trainer, location, annotatedxmlloc)
    for predictxmlname in ["1","2","3","4","5"]:
        error =TestUsingCRF(predictxmlname, location)
        errorcount += error[0]
        sparseerror += error[1]
    
    preprocessor = Processors.PreProcessor.PreProcessor()
    trainer = Utils.Trainer.Trainer()
    xmls = ["1","2","3","4","5","11","12","13","14","15"]
    TrainUsingCRF(xmls, preprocessor, trainer, location, annotatedxmlloc)
    for predictxmlname in ["6","7","8","9","10"]:
        error =TestUsingCRF(predictxmlname, location)
        errorcount += error[0]
        sparseerror += error[1]
    
    print "**********************************************************"
    print errorcount
    print sparseerror

def crossValidationLR():
    location = "../TrainingData/xmls/cs/"
    annotatedxmlloc = "../TrainingData/annotated/"
    errorcount1 = 0
    sparseerror1 = 0
    
    preprocessor = Processors.PreProcessor.PreProcessor()
    trainer = Utils.Trainer.Trainer()
    xmls = ["1","2","3","4","5","6","7","8","9","10"]
    TrainUsingLR(xmls, preprocessor, trainer, location, annotatedxmlloc)
    for predictxmlname in ["11","12","13","14","15"]:
        error = TestUsingLR(predictxmlname, location)
        errorcount1 += error[0]
        sparseerror1 += error[1]
    
    preprocessor = Processors.PreProcessor.PreProcessor()
    trainer = Utils.Trainer.Trainer()
    xmls = ["11","12","13","14","15","6","7","8","9","10"]
    TrainUsingLR(xmls, preprocessor, trainer, location, annotatedxmlloc)
    for predictxmlname in ["1","2","3","4","5"]:
        error =TestUsingLR(predictxmlname, location)
        errorcount1 += error[0]
        sparseerror1 += error[1]
    
    preprocessor = Processors.PreProcessor.PreProcessor()
    trainer = Utils.Trainer.Trainer()
    xmls = ["1","2","3","4","5","11","12","13","14","15"]
    TrainUsingLR(xmls, preprocessor, trainer, location, annotatedxmlloc)
    for predictxmlname in ["6","7","8","9","10"]:
        error =TestUsingLR(predictxmlname, location)
        errorcount1 += error[0]
        sparseerror1 += error[1]
    
    print "**********************************************************"
    print errorcount1
    print sparseerror1
                        
if __name__ == '__main__':
    xmls = ["1","2","3","4","5","6","7","8","9","10","11","12","13","14","15"]
    preprocessor = Processors.PreProcessor.PreProcessor()
    postprocessor = Processors.PostProcessor.PostProcessor()
    trainer = Utils.Trainer.Trainer()
    
    xmlloc = "../TrainingData/xmls/cs/"
    #CreateHtmls(xmls, preprocessor, trainer, xmlloc)
   
    location = "../TrainingData/xmls/cs/"
    annotatedxmlloc = "../TrainingData/annotated/"
    crossValidation()
    #crossValidationLR()
    #svminstance = TrainUsingSVM(xmls, preprocessor, trainer, location, annotatedxmlloc)
    #TrainUsingCRF(xmls, preprocessor, trainer, location, annotatedxmlloc)
    #TrainUsingLR(xmls, preprocessor, trainer, location, annotatedxmlloc)
    
#    predictxmlname = '1'
#    location = "../TestData/xmls/"
#    TestUsingSVM(svminstance, predictxmlname, location)
#    
#    print "******************************* CRF *************************************"
#    TestUsingCRF(predictxmlname, location)
#    
#    print "******************************* LR *************************************"
#    TestUsingLR(predictxmlname, location)
#    
