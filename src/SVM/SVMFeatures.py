'''
Created on Dec 1, 2012

@author: shriram
'''
from Utils.Constants import Constants
import sys

class SVMFeatures:
    
    def orthographicfeatures(self, featurelist, col, prevtag, curtag, i, fontdict):
        issamefont = i!=0 and (fontdict[int(col[i][1].attrib['font'])] == fontdict[int(col[i - 1][1].attrib['font'])])
        if(issamefont): 
            featurelist.append(1)
        else:
            featurelist.append(0)

        tabletextbefore = ((i>0 and col[i-1][1].text is not None and col[i-1][1].text.lower().startswith("table ")) or 
                           (i>1 and col[i-2][1].text is not None and col[i-2][1].text.lower().startswith("table ")))
        
        if((tabletextbefore)):
            featurelist.append(1)
        else:
            featurelist.append(0)
            
    def lexicalfeatures(self, featurelist, col, prevtag, curtag, i):
        pass
    
    def spaceinline(self, text):
        if(text is None):
            return [0,0,0]
        spacecount = 0
        largestspace = 0
        wordcount = 0
        smallestspace = sys.maxint
        for r in xrange(len(text)):
            if(text[r] == ' '):
                spacecount += 1
            elif(spacecount != 0):
                wordcount += 1
                if(spacecount < smallestspace):
                    smallestspace = spacecount
                if(spacecount > largestspace):
                    largestspace = spacecount
                spacecount = 0
        return [largestspace, smallestspace, wordcount+1 ]
    
    def spacelayoutfeatures(self, featurelist, col, curtag, i):
        spaceincurrentline = self.spaceinline(col[i][1].text)
        if (spaceincurrentline[0] >= Constants.LARGEST_SPACE):
            featurelist.append(1)
        else:
            featurelist.append(0)
        if (spaceincurrentline[1] <= Constants.SMALLEST_SPACE):
            featurelist.append(1)
        else:
            featurelist.append(0)
        if (spaceincurrentline[2] <= Constants.WORDS_IN_LINE):
            featurelist.append(1)
        else:
            featurelist.append(0)

    def layoutfeatures(self, featurelist, col, prevtag, curtag, i): 
        #[textpieces, heightprev, heightnext, largest space, smallest space, words]
        if(int(col[i][1].attrib['textpieces']) > Constants.NUM_TEXT_PIECES):
            featurelist.append(1)
        else:
            featurelist.append(0)
        
        if(i>1 and int(col[i][1].attrib['height']) < int(col[i-2][1].attrib['height'])):
            featurelist.append(1)
        else:
            featurelist.append(0)
            
        if(i!=len(col)-1 and int(col[i][1].attrib['height']) < int(col[i+1][1].attrib['height'])):
            featurelist.append(1)
        else:
            featurelist.append(0)
        
        self.spacelayoutfeatures(featurelist, col, curtag, i) 
        
    
    def domainfindfeatureFunction(self, i, col, fontdict, prevtag = None, curtag = None):
        featurelist = list()
        if(prevtag is None and i!=0):
            prevtag = int(col[i-1][0])
        if(curtag is None and i!=0):
            curtag = int(col[i][0])
        
        self.orthographicfeatures(featurelist, col, prevtag, curtag, i, fontdict)
        #featurelist.append(self.lexicalfeatures(featurelist, col, prevtag, curtag, i))
        self.layoutfeatures(featurelist, col, prevtag, curtag, i)
        
        return featurelist