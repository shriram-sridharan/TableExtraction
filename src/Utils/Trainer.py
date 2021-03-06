'''
Created on Nov 20, 2012

@author: shriram
'''
import xml.etree.ElementTree as ET
from xml.sax.saxutils import escape

'''
    Annotating only Sparse and Non Sparse Lines
'''
class Trainer:
    def html_escape(self,text):
        html_escape_table = {
        '"': "&quot;",
        "'": "&apos;"
        }
        return escape(text, html_escape_table)
  
    def train(self, preprocessedxml, xmlname):
        f = open('../TrainingData/htmls/train'+xmlname+'.html','w')
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
                    f.write('<option value="sparse">Sparse</option>')
                    f.write('<option value="nonsparse" selected="selected">Not Sparse</option>')
                    f.write("</select><input type='hidden' name='texttag"+str(i)+"' value='"+  self.html_escape(ET.tostring(tup[1],'utf-8',"xml")) + "'/>"+ ET.tostring(tup[1]) +"</div>")
                    i += 1
                f.write('<input type="hidden" name="colend'+str(colno)+'" value="'+str(i)+'"/><div>')
                colno += 1
            f.write('<input type="hidden" name="pageend'+str(pageno)+'" value="'+str(colno)+'"/> <div>')
            pageno += 1
        f.write('<input type="submit" value="Done!"/></form></body></html>')
        f.close()
        
    def readAnnotatedXml(self,xmlname):
        f = open(xmlname)
        preprocessedxml = list()
        col = list()
        for line in f:
            if(line == "=============================== PAGE ===================================\n"):
                pagelist = list()
                preprocessedxml.append(pagelist)
            elif(line == "=============================== COL ===================================\n"):
                col = list()
                pagelist.append(col)
            else:
                tup0 = line[:line.find(" ")]
                tup1 = line[line.find(" ")+1:]
                col.append([tup0,ET.fromstring(tup1)])
        
        return preprocessedxml
                    
    def readAnnotatedxmlforTableDecomposition(self, xmlname):
        f = open(xmlname)
        table = list()
        for line in f:
            if(line.strip() == ''):
                continue
            tup0 = line[:line.find("\t")]
            tup1 = line[line.find("\t")+1:]
            table.append([tup0,ET.fromstring(tup1)])
        return table
        
        
        
        
        
        