'''
Created on Dec 8, 2012

@author: shriram
'''
import re

class Utilities:
    def checkkeywordpresense(self, predicted, currpredictedindex):
        compiledre = re.compile('table\d')
        if(predicted[currpredictedindex][1].text is None):
            return False
        return (compiledre.match(predicted[currpredictedindex][1].text[0:7].lower().replace(' ','')) is not None)