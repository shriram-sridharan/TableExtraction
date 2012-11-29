'''
Created on Nov 20, 2012

@author: shriram
'''
import PreProcessor
import Trainer

if __name__ == '__main__':
    xmlname = "Test3"
    preprocessor = PreProcessor.PreProcessor()
    preprocessedxml = preprocessor.preprocessxml("../TrainingData/xmls/"+ xmlname + ".xml") #list(pages), pages -> list(cols), col -> list(<Sparse/NonSparse, tag>) 
    
    trainer = Trainer.Trainer()
    trainer.train(preprocessedxml, xmlname)
    '''
        Train/Test using CRF
    '''