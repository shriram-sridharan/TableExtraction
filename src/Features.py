'''
Created on Dec 1, 2012

@author: shriram
'''
from SparseType import SparseType
class Features:

    
    def orthographicfeatures(self, featurelist, col, prevtag, curtag, i, fontdict):
        issamefont = (fontdict[int(col[i][1].attrib['font'])] == fontdict[int(col[i - 1][1].attrib['font'])])
        if(i!=0 and issamefont 
           and curtag == SparseType.OTHERSPARSE and prevtag == SparseType.OTHERSPARSE): 
            featurelist.append(1)
        else:
            featurelist.append(0)
    
    def lexicalfeatures(self, featurelist, col, prevtag, curtag, i):
        pass
    
    
    def layoutfeatures(self, featurelist, col, prevtag, curtag, i):
        if(int(col[i][1].attrib['textpieces']) > 0 and curtag == SparseType.OTHERSPARSE):
            featurelist.append(1)
        else:
            featurelist.append(0)
    
    def otherfeatures(self,featurelist, col, prevtag, curtag, i):
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
    
    def domainfindfeatureFunction(self, i, col, fontdict, prevtag = None, curtag = None):
        featurelist = list()
        if(prevtag is None and i!=0):
            prevtag = int(col[i-1][0])
        if(curtag is None and i!=0):
            curtag = int(col[i][0])
            
        self.orthographicfeatures(featurelist, col, prevtag, curtag, i, fontdict)
        #featurelist.append(self.lexicalfeatures(featurelist, col, prevtag, curtag, i))
        self.layoutfeatures(featurelist, col, prevtag, curtag, i)
        self.otherfeatures(featurelist, col, prevtag, curtag, i)   
        
        return featurelist