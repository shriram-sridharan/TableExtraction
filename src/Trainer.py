'''
Created on Nov 20, 2012

@author: shriram
'''
import xml.etree.ElementTree as ET

'''
    Try 1: To see where the table begin and end is sufficient for training
'''
class Trainer:
    def train(self, preprocessedxml):
        f = open('../TrainingData/preprocessedxml/train1.html','w')
        f.write('<html><body><form action=''>')
        for page in preprocessedxml:
            f.write('<div class="page">')
            for col in page:
                f.write('<div class="col">')
                for tup in col:
                    f.write('<div><select id="tableparams" name="tableparams">')
                    f.write('<option value="tablebegin" selected="selected">No Table</option>')
                    f.write('<option value="tablebegin">Table Begin</option>')
                    f.write('<option value="tableend">Table End</option>')
                    f.write("</select><input type='hidden' value='"+ ET.tostring(tup[1]) + "'/>"+ ET.tostring(tup[1]) +"</div>")
                f.write('<div>')
            f.write('<div>')
        f.write('<input type="submit" value="Done!"/></form></body></html>')
        f.close()