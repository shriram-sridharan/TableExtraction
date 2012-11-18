'''
Created on Nov 17, 2012

@author: shriram
'''
import xml.etree.ElementTree as ET
def lineDetection(xmldoc, fontdict):
    parseTree = ET.parse(xmldoc)
    fontspecTags = parseTree.iter('fontspec')
    for tags in fontspecTags:
        fontdict[int(tags.attrib['id'])] = int(tags.attrib['size'])
        
    for tags in parseTree.iter('page'):
        columns = findColumns(tags, int(tags.attrib['width']))
        for col in columns:
                detectSparseLines(col,fontdict)
'''
Heuristics Based:
Begins with Table {No}.
Ends with a sparse Line
'''

def detectSparseLines(col, fontdict):
    potentialTable = False
    nextPotentialLines = 0
    top = 0
    height = 0
    font = 0
    confirmedTable = False
    potentialTop = 0
    table = list()
    
    for tag in col:
        if(tag.text is None):
            continue
        text = tag.text.encode('ascii', 'ignore')
        if(confirmedTable):
            if(((int(tag.attrib['top']) - top < 2) or ((int(tag.attrib['top']) - (top + height) < 2))) 
                     ):
                table.append(text) 
                top = int(tag.attrib['top'])
                height = int(tag.attrib['height'])
                font = fontdict[int(tag.attrib['font'])]
            else:
                print "Table Encountered " + table[0] + str(potentialTop) + " "  + (tag.attrib['top'])
               
                potentialTable = False
                confirmedTable = False
                nextPotentialLines = 0
                top = 0
                potentialTop = 0
                table = list()
        else:   
            if (potentialTable and nextPotentialLines < 5):
                nextPotentialLines += 1
                table.append(text)
                if (len(text.split(' ')) < 4):
                    if(top is 0):
                        top = int(tag.attrib['top'])
                        height = int(tag.attrib['height'])
                        font = fontdict[int(tag.attrib['font'])]
                    elif (((int(tag.attrib['top']) - top < 2) or ((int(tag.attrib['top']) - (top + height) < 2))) 
                          and fontdict[int(tag.attrib['font'])] is font):
                        confirmedTable = True
                    else:
                        top = int(tag.attrib['top'])
                        height = int(tag.attrib['height'])
                        font = fontdict[int(tag.attrib['font'])]
            else:
                potentialTable = False
                nextPotentialLines = 0
                top = 0
                potentialTop = 0
                table = list()     
                       
        if(text.startswith("Table")):
            if(not confirmedTable):
                potentialTable = True
                potentialTop = tag.attrib['top']
                table.append(text)
                
'''
TODO
Handling Multiple Columns
'''
def findColumns(tags, width):
    col1 = list()
    col2 = list()
    for texttag in tags.findall('text'):
        if(int(texttag.attrib['left']) < width/2):
            col1.append(texttag)
        else:
            col2.append(texttag)
    return [col1, col2]

if __name__ == '__main__':
    fontdict = dict()
    f = open("Test.xml",'r')
    f1 = open("Test2.xml",'w')
    for line in f:
        f1.write(line.replace('<b>','').replace('</b>','').replace('<i>','').replace('</i>',''))
    f.close()
    f1.close()
    lineDetection("Test2.xml", fontdict)