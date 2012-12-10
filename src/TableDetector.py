from CRF.CRF import CRF
import Processors.PreProcessor
import Processors.PostProcessor
import Utils.Trainer
import xml.etree.ElementTree as ET
from Utils.SparseType import SparseType
from LR.LogisticRegressor import LogisticRegressor

def TrainUsingCRF(xmls, preprocessor, trainer):
    CRFImpl = CRF()
    annotatedxmllist = list()
    for xmlname in xmls:
        fontdict = preprocessor.getFontDictionary(ET.parse("../TrainingData/xmls/" + xmlname + ".xml")) #list(pages), pages -> list(cols), col -> list(<Sparse/NonSparse, tag>)
        annotatedxml = trainer.readAnnotatedXml('../TrainingData/annotated/' + xmlname + "_annotated")
        annotatedxmllist.append([annotatedxml, fontdict])
    
    CRFImpl.domaintrain(annotatedxmllist)
    print CRFImpl.trainedweights
    f = open("TrainedWeightsCRF", 'w')
    for weight in CRFImpl.trainedweights:
        f.write(str(weight) + "\n")
    
    f.close()
    
def TrainUsingLR(xmls, preprocessor, trainer):
    LRImpl = LogisticRegressor()
    annotatedxmllist = list()
    for xmlname in xmls:
        fontdict = preprocessor.getFontDictionary(ET.parse("../TrainingData/xmls/" + xmlname + ".xml")) #list(pages), pages -> list(cols), col -> list(<Sparse/NonSparse, tag>)
        annotatedxml = trainer.readAnnotatedXml('../TrainingData/annotated/' + xmlname + "_annotated")
        annotatedxmllist.append([annotatedxml, fontdict])
    
    LRImpl.domaintrain(annotatedxmllist)
    print LRImpl.trainedweights
    f = open("TrainedWeightsLR", 'w')
    for weight in LRImpl.trainedweights:
        f.write(str(weight) + "\n")
    
    f.close()
    
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
    for page in preprocessedxml:
        for col in page:
            if(len(col) < 2):
                    continue
            for lineno in xrange(len(col)):
                col[lineno].append(lineno)
            predicted = LR.domainpredict(col, fontdict)
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
            print row[1].text + " " + str(row[0])   
def CreateHtmls(xmls, preprocessor, trainer):
    for xmlname in xmls:
        preprocessedxml = preprocessor.preprocessxml("../TrainingData/xmls/" + xmlname + ".xml") #list(pages), pages -> list(cols), col -> list(<Sparse/NonSparse, tag>)
        trainer.train(preprocessedxml, xmlname)

def TestUsingCRF(predictxmlname, location):
    CRF = getModelwithTrainedWeights()
    fontdict = preprocessor.getFontDictionary(ET.parse(location + predictxmlname + ".xml"))                  
    preprocessedxml = preprocessor.preprocessxml(location + predictxmlname + ".xml") #list(pages), pages -> list(cols), col -> list(<Sparse/NonSparse, tag>)
    
    alltables = list()
    for page in preprocessedxml:
        for col in page:
            if(len(col) < 2):
                    continue
            for lineno in xrange(len(col)):
                col[lineno].append(lineno)
            predicted = CRF.predict(col, fontdict)
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
            print row[1].text + " " + str(row[0]) 
            
if __name__ == '__main__':
    xmls = ["Test1","Test2","Test3","Test4","Test5"] #
    preprocessor = Processors.PreProcessor.PreProcessor()
    postprocessor = Processors.PostProcessor.PostProcessor()
    trainer = Utils.Trainer.Trainer()
    
    #CreateHtmls(xmls, preprocessor, trainer)
   
    predictxmlname = 'Test1'
    location = "../TrainingData/xmls/" 
    
    TrainUsingCRF(xmls, preprocessor, trainer)
    TestUsingCRF(predictxmlname, location)
    
#    TrainUsingLR(xmls, preprocessor, trainer)
#    TestUsingLR(predictxmlname, location)
    
    
          
    
    
    
    
