'''
Created on Nov 20, 2012

@author: shriram

'''
from CRF import CRF
import PreProcessor
import PostProcessor
import Trainer
import xml.etree.ElementTree as ET
from SparseType import SparseType
from PostProcessor import TableKeywordLoc

def getCRFwithTrainedWeights():
    trainedweights = list()
    f = open("TrainedWeights", "r")
    for weight in f:
        trainedweights.append(float(weight))
    
    f.close()
    CRFImpl = CRF(trainedweights)
    return CRFImpl

if __name__ == '__main__':
    xmls = ["1","3","4","Test1","Test2","Test3","Test4","Test5"] #
    preprocessor = PreProcessor.PreProcessor()
    postprocessor = PostProcessor.PostProcessor()
    trainer = Trainer.Trainer()

################### CREATE HTMLS TO ANNOTATE ####################
#    for xmlname in xmls:      
#        preprocessedxml = preprocessor.preprocessxml("../TrainingData/xmls/"+ xmlname + ".xml") #list(pages), pages -> list(cols), col -> list(<Sparse/NonSparse, tag>) 
#        trainer.train(preprocessedxml, xmlname)
   
################### TRAIN USING ANNOTATE XMLS ####################
#    CRFImpl = CRF()
#    annotatedxmllist = list()
#    for xmlname in xmls:
#        fontdict = preprocessor.getFontDictionary(ET.parse("../TrainingData/xmls/"+ xmlname + ".xml")) #list(pages), pages -> list(cols), col -> list(<Sparse/NonSparse, tag>) 
#        annotatedxml = trainer.readAnnotatedXml('../TrainingData/annotated/' + xmlname +"_annotated")
#        annotatedxmllist.append([annotatedxml, fontdict])
#    CRFImpl.domaintrain(annotatedxmllist)
#    print CRFImpl.trainedweights
#    
#    f = open("TrainedWeights",'w')
#    for weight in CRFImpl.trainedweights:
#        f.write(str(weight) + "\n")
#    f.close()
################### TEST USING TRAINED MODEL ####################
    CRF = getCRFwithTrainedWeights()
    predictxmlname = '9'
     
    location = "../TestData/xmls/"
    #location = "../TrainingData/xmls/"
             
    fontdict = preprocessor.getFontDictionary(ET.parse(location + predictxmlname + ".xml"))                  
    preprocessedxml = preprocessor.preprocessxml(location + predictxmlname + ".xml") #list(pages), pages -> list(cols), col -> list(<Sparse/NonSparse, tag>)
    
    alltables = list()
    tablekeywordloc = TableKeywordLoc.UNKNOWN
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
            data = postprocessor.findTables(predicted, tablekeywordloc)
            tablekeywordloc = data[1]
            tables = data[0]
            if(len(tables) == 0):
                continue
            for t in tables:
                alltables.append(t)
    
    for table in alltables:
        print "============================================="
        for row in table:
            print row[1].text
            
    
    
    
    
