'''
Created on Nov 20, 2012

@author: shriram
'''
import PreProcessor

if __name__ == '__main__':
    preprocessor = PreProcessor.PreProcessor()
    preprocessedxml = preprocessor.preprocessxml("../TrainingData/xmls/Test3.xml") #list(pages), pages -> list(cols), col -> list(<Sparse/NonSparse, tag>) 
    '''
        Train/Test using CRF
    '''