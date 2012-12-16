'''
Created on Dec 1, 2012

@author: shriram
'''
from Utils.Constants import Constants
import sys
from Utils.Utilities import Utilities

class LRFeatures:
    
    def orthographicfeatures(self, featurelist, col, i, fontdict):
        issamefont = i!=0 and (fontdict[int(col[i][1].attrib['font'])] == fontdict[int(col[i - 1][1].attrib['font'])])
        if(issamefont): 
            featurelist.append(1)
        else:
            featurelist.append(0)
        
        if(col[i][1].text is not None and col[i][1].text[0].isupper()):
            featurelist.append(1)
        else:
            featurelist.append(0)
    
    def isTableKeywordBeforeThis(self, currindex, col):
        for r in xrange(currindex - Constants.AVG_TABLE_SIZE, currindex):
            if(r < 0):
                return False
            if(Utilities().checkkeywordpresense(col, r)):
                return True
        return False
        
    def lexicalfeatures(self, featurelist, col, i):
        if(self.isTableKeywordBeforeThis(i, col)):
            featurelist.append(1)
        else:
            featurelist.append(0)
        
    def spaceinline(self, text):
        if(text is None):
            return [0,0,0,0]
        spacecount = 0
        largestspace = 0
        wordcount = 0
        smallestspace = sys.maxint
        wordspacelist = list()
        for r in xrange(len(text)):
            if(text[r] == ' '):
                spacecount += 1
            elif(spacecount != 0):
                wordcount += 1
                wordspacelist.append(spacecount)
                if(spacecount < smallestspace):
                    smallestspace = spacecount
                if(spacecount > largestspace):
                    largestspace = spacecount
                spacecount = 0
                
        wslcount = 0
        for wsl in wordspacelist:
            if(wsl > Constants.LARGEST_SPACE_DIFF):
                wslcount += 1
                
        return [largestspace, smallestspace, wordcount+1, wslcount]
    
    def layoutfeatures(self, featurelist, col, i): 
        #[textpieces, heightprev, heightnext, largest space, smallest space, words]
        if(int(col[i][1].attrib['textpieces']) > Constants.NUM_TEXT_PIECES):
            featurelist.append(1)
        else:
            featurelist.append(0)
        
        if(self.spaceinline(col[i][1].text)[2] == 1):
            featurelist.append(1)
        else:
            featurelist.append(0)
        
        if(i!=0 and int(col[i][1].attrib['height']) < int(col[i-1][1].attrib['height'])):
            featurelist.append(1)
        else:
            featurelist.append(0)
            
        if(i!=0 and int(col[i-1][1].attrib['height']) < int(col[i][1].attrib['height'])):
            featurelist.append(1)
        else:
            featurelist.append(0)
        
        if(i>0 and int(col[i][1].attrib['height']) == int(col[i-1][1].attrib['height'])):
            featurelist.append(1)
        else:
            featurelist.append(0)
        
        if(i>0 and int(col[i][1].attrib['height']) == int(col[i-1][1].attrib['height'])):
            featurelist.append(1)
        else:
            featurelist.append(0)
        
        self.spacelayoutfeatures(featurelist, col, i) 
        
    def spacelayoutfeatures(self, featurelist, col, i):
        spaceincurrentline = self.spaceinline(col[i][1].text)
        if (spaceincurrentline[0] >= Constants.LARGEST_SPACE):
            featurelist.append(1)
        else:
            featurelist.append(0)
        
        if (spaceincurrentline[0] == spaceincurrentline[1]):
            featurelist.append(1)
        else:
            featurelist.append(0)
        
        if (spaceincurrentline[2] > Constants.WORDS_IN_LINE):
            featurelist.append(1)
        else:
            featurelist.append(0)
        
        if (spaceincurrentline[3] > Constants.NO_WORDS_WITH_LARGESTSPACEDIFF):
            featurelist.append(1)
        else:
            featurelist.append(0)
            
    def domainfindfeatureFunction(self, i, col, fontdict, prevtag = None, curtag = None):
        featurelist = list()
        
        self.orthographicfeatures(featurelist, col, i, fontdict)
        self.lexicalfeatures(featurelist, col, i)
        self.layoutfeatures(featurelist, col, i)
        
        return featurelist