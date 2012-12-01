'''
Created on Nov 20, 2012

@author: shriram
'''
import PreProcessor
import Trainer
import sys
from CRF import CRF
if __name__ == '__main__':
    xmls = ["Test2","Test4","Test5"]
    preprocessor = PreProcessor.PreProcessor()
    trainer = Trainer.Trainer()
    
#    if(sys.argv[1] == "-create"):
#        for xmlname in xmls:      
#            preprocessedxml = preprocessor.preprocessxml("../TrainingData/xmls/"+ xmlname + ".xml") #list(pages), pages -> list(cols), col -> list(<Sparse/NonSparse, tag>) 
#            trainer.train(preprocessedxml, xmlname)
#    
#    elif(sys.argv[1] == "-train"):
    annotatedxmllist = list()
    for xmlname in xmls:
        annotatedxml = trainer.readAnnotatedXml(xmlname +"_annotated")
        annotatedxmllist.append(annotatedxml)
    CRF().domaintrain(annotatedxmllist)
