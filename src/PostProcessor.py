'''
Created on Dec 6, 2012

@author: sridharan5
'''
from SparseType import SparseType

class PostProcessor:
    def getnextsparse(self, currpredictedindex, predicted):
        for r in xrange(currpredictedindex+1, len(predicted)):
            if(predicted[r][0] == SparseType.OTHERSPARSE):
                return r
        return -1
    
    def findTables(self, predicted):
        tables = list()
        curtablelist = list()
        tablefound = False
        currpredictedindex = -1
        while currpredictedindex < len(predicted) - 1:
            currpredictedindex += 1
            if(predicted[currpredictedindex][0] == SparseType.OTHERSPARSE):
                curtablelist.append(predicted[currpredictedindex][1].text.encode('utf-8'))

            elif(predicted[currpredictedindex][1].text is not None and predicted[currpredictedindex][1].text.lower().startswith("table")):
                if(len(curtablelist) > 2):
                    curtablelist.append(predicted[currpredictedindex][1].text.encode('utf-8'))
                    tables.append(curtablelist)
                    curtablelist = list()
                else:
                    #Find whether the sparse lines detected are before or after the keyword
                    nextsparse = self.getnextsparse(currpredictedindex, predicted)
                    if((nextsparse == -1) or (int(predicted[nextsparse][1].attrib['top']) - int(predicted[currpredictedindex][1].attrib['top']) 
                                              > 3 * int(predicted[currpredictedindex][1].attrib['height']))):
                        curtablelist = list()
                        continue
                    
                    curtablelist = list()
                    for c in xrange(currpredictedindex,nextsparse+1):
                        curtablelist.append(predicted[c][1].text.encode('utf-8'))
                    currpredictedindex = nextsparse
                    tablefound = True
                    
            if(predicted[currpredictedindex][0] == SparseType.NONSPARSE):
                if(len(curtablelist) == 0):
                    continue
                
                nextsparse = self.getnextsparse(currpredictedindex, predicted)
                if((nextsparse == -1) or (int(predicted[nextsparse][1].attrib['top']) - int(predicted[currpredictedindex][1].attrib['top']) 
                                          > 2.5 * int(predicted[currpredictedindex][1].attrib['height']))):
                    if(len(curtablelist) > 1):
                        if(tablefound):
                            tables.append(curtablelist)
                        else:
                            i = currpredictedindex
                            onelineafter = (i < len(predicted) - 1 and predicted[i+1][1].text is not None and predicted[i+1][1].text.lower().startswith("table "))
                            twolinesafter = (i < len(predicted) - 2  and predicted[i+2][1].text is not None and predicted[i+2][1].text.lower().startswith("table "))
                            tabletextafter = (onelineafter or twolinesafter)
                            if(tabletextafter):
                                if(onelineafter):
                                    currpredictedindex = i+1 
                                    curtablelist.append(predicted[i+1][1].text.encode('utf-8'))
                                    tables.append(curtablelist)
                                else:
                                    currpredictedindex = i+2
                                    curtablelist.append(predicted[i+1][1].text.encode('utf-8'))
                                    curtablelist.append(predicted[i+2][1].text.encode('utf-8'))
                                    tables.append(curtablelist)
                    curtablelist = list()
                    continue

                for c in xrange(currpredictedindex,nextsparse+1):
                    curtablelist.append(predicted[c][1].text.encode('utf-8'))
                currpredictedindex = nextsparse         
                
        return tables