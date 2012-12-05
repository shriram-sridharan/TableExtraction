'''
Created on Nov 20, 2012

@author: shriram
'''
import PreProcessor
import Trainer
from CRF import CRF
import xml.etree.ElementTree as ET
if __name__ == '__main__':
    xmls = ["Test1","Test2","Test3","Test4", "Test5"] #
    preprocessor = PreProcessor.PreProcessor()
    trainer = Trainer.Trainer()

################### CREATE HTMLS TO ANNOTATE ####################
#        for xmlname in xmls:      
#            preprocessedxml = preprocessor.preprocessxml("../TrainingData/xmls/"+ xmlname + ".xml") #list(pages), pages -> list(cols), col -> list(<Sparse/NonSparse, tag>) 
#            trainer.train(preprocessedxml, xmlname)
#    

################### TRAIN USING ANNOTATE XMLS ####################
    annotatedxmllist = list()
    for xmlname in xmls:
        fontdict = preprocessor.getFontDictionary(ET.parse("../TrainingData/xmls/"+ xmlname + ".xml")) #list(pages), pages -> list(cols), col -> list(<Sparse/NonSparse, tag>) 
        annotatedxml = trainer.readAnnotatedXml(xmlname +"_annotated")
        annotatedxmllist.append([annotatedxml, fontdict])
    CRF().domaintrain(annotatedxmllist)
    
################### TEST USING TRAINED MODEL ####################
    