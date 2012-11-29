'''
Created on Nov 20, 2012

@author: shriram
'''
import xml.etree.ElementTree as ET

'''
    Try 1: To see where the table begin and end is sufficient for training
'''
class Trainer:
    def train(self, preprocessedxml, xmlname):
        f = open('../TrainingData/preprocessedxml/train.html','w')
        f.write('<html><body><form action="http://localhost/cgi-bin/TableProcessor.py" method="post">')
        f.write('<input type="hidden" name="xmlname" value="'+xmlname +'"/>')
        i = 0
        pageno = 0
        colno = 0
        for page in preprocessedxml:
            f.write('<div class="page"><input type="hidden" name="pagebegin'+str(pageno)+'" value="'+str(colno)+'"/>')
            for col in page:
                f.write('<div class="col"><input type="hidden" name="colbegin'+str(colno)+'" value="'+str(i)+'"/>')
                for tup in col:
                    f.write('<div><select id="docparams" name="docparams'+ str(i) +'">')
                    f.write('<option value="sparse" selected="selected">Sparse</option>')
                    f.write('<option value="nonsparse">Not Sparse</option>')
                    f.write("</select><input type='hidden' name='texttag"+str(i)+"' value='"+ ET.tostring(tup[1]) + "'/>"+ ET.tostring(tup[1]) +"</div>")
                    i += 1
                f.write('<input type="hidden" name="colend'+str(colno)+'" value="'+str(i)+'"/><div>')
                colno += 1
            f.write('<input type="hidden" name="pageend'+str(pageno)+'" value="'+str(colno)+'"/> <div>')
            pageno += 1
        f.write('<input type="submit" value="Done!"/></form></body></html>')
        f.close()