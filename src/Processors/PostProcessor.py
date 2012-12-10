'''
Created on Dec 6, 2012

@author: sridharan5
'''
from Utils.SparseType import SparseType
from Utils.Utilities import Utilities
from Utils.Constants import Constants
import math

class PostProcessor:
    def isTableKeywordAfterThis(self, currpredictedindex, predicted):
        for r in xrange(currpredictedindex, currpredictedindex + Constants.LINES_TO_SEARCH_FOR_TABLE):
            if(r >= len(predicted)):
                return -1
            if(Utilities().checkkeywordpresense(predicted, r)):
                return r
        return -1
    
    def getnextsparse(self, currpredictedindex, predicted):
        for r in xrange(currpredictedindex+1, len(predicted)):
            if(predicted[r][0] == SparseType.OTHERSPARSE):
                return r
        return -1
    
    def getprevioussparse(self, currpredictedindex, predicted):
        for r in reversed(xrange(0, currpredictedindex)):
            if(predicted[r][0] == SparseType.OTHERSPARSE):
                return r
        return -1

    def findPossibleTableStructureAfterThis(self, predicted, currpredictedindex):
        tablekeywordlineno = predicted[currpredictedindex][2]
        #Assuming that the table caption can extend for a maximum for 2 lines
        nextsparse = self.getnextsparse(currpredictedindex, predicted)
        nextsparselineno = predicted[nextsparse][2]
        table = list()
        diff = nextsparselineno - tablekeywordlineno
        if(diff > Constants.MAX_DIFF_BETWEEN_SPARSE_AND_NONSPARSE or nextsparse == -1): #No table
            return [currpredictedindex, table]
        
        for _ in xrange(diff):
            table.append(predicted[currpredictedindex])
            currpredictedindex += 1
        
        currentlineno = tablekeywordlineno
        nextlineno = tablekeywordlineno
        while(nextlineno!= -1 and nextlineno - currentlineno <= 2 and currpredictedindex < len(predicted)):
            table.append(predicted[currpredictedindex])
            currentlineno = predicted[currpredictedindex][2]
            nextlineno = predicted[self.getnextsparse(currpredictedindex, predicted)][2]
            currpredictedindex += 1
                
        return [currpredictedindex - 1, table]
                
    
    def findPossibleTableStructureBeforeThis(self, predicted, currpredictedindex):
        tablekeywordlineno = predicted[currpredictedindex][2]
        #Assuming that the table caption can extend for a maximum for 2 lines
        prevsparse = self.getprevioussparse(currpredictedindex, predicted)
        prevsparselineno = predicted[prevsparse][2]
        table = list()
        diff =  tablekeywordlineno - prevsparselineno
        inputcurrpredictedindex = currpredictedindex
        if(diff > 3): #No table
            return [currpredictedindex, table]
        
        for _ in xrange(diff):
            table.append(predicted[currpredictedindex])
            currpredictedindex -= 1
        
        currentlineno = tablekeywordlineno
        prevlineno = tablekeywordlineno
        while(prevlineno != -1 and currpredictedindex >= 0):
            currentlineno = predicted[currpredictedindex][2]
            prevlineno = predicted[self.getprevioussparse(currpredictedindex, predicted)][2]
            if(math.fabs(currentlineno - prevlineno) >  2):
                break
            table.append(predicted[currpredictedindex])
            currpredictedindex -= 1
                
        return [inputcurrpredictedindex, table]
    
    
    def findTables(self, predicted):
        tables = list()
        currpredictedindex = -1
        while currpredictedindex < len(predicted) - 1:
            currpredictedindex += 1
            if(Utilities().checkkeywordpresense(predicted, currpredictedindex)):
                data = self.findPossibleTableStructureAfterThis(predicted, currpredictedindex)
                currpredictedindex = data[0]
                if(len(data[1])!=0):
                    tables.append(data[1])
                    continue
            if(predicted[currpredictedindex][0] == SparseType.OTHERSPARSE): #Hoping to find a table after this
                data = self.findPossibleTableStructureAfterThis(predicted, currpredictedindex)
                currpredictedindex = data[0]
                if(len(data[1])!=0):
                    tblkeywordloc = self.isTableKeywordAfterThis(currpredictedindex, predicted)
                    if(tblkeywordloc == -1):
                        continue
                    data = self.findPossibleTableStructureBeforeThis(predicted, tblkeywordloc)
                    if(len(data[1])!=0):
                        tables.append(reversed(data[1]))
                        currpredictedindex = data[0]
                        
        return tables