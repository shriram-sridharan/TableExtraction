'''
Created on Nov 20, 2012

@author: shriram
'''
import xml.etree.ElementTree as ET
import math
from SparseType import SparseType
from Constants import Constants

def removeBandITags(xmlloc):
    f = open(xmlloc, 'r')
    f1 = open(xmlloc + '_tag', 'w')
    for line in f:
        f1.write(line.replace('<b>', '').replace('</b>', '').replace('<i>', '').replace('</i>', ''))
    
    f.close()
    f1.close()
    
    return xmlloc+'_tag'

'''
    Check for marked difference in top 
    Info: Figures' data will go into new columns
    Should we check the left too?
'''
def findColumns(page):
    width = int(page.attrib['width'])
    height = int(page.attrib['height'])
    THRESHOLD_HEIGHT = height/3
    #THRESHOLD_WIDTH = width/3
    pagecolumns = list()
    
    prevtexttag = page.find('text')
    col = list()
    for texttag in page.findall('text'):
        col.append(texttag)
        prevtop = int(prevtexttag.attrib['top'])
        currtop = int(texttag.attrib['top'])
        #prevleft = int(prevtexttag.attrib['left'])
        #curleft = int(texttag.attrib['left'])
        if((prevtop - currtop) > THRESHOLD_HEIGHT):
            print "New Column Found"
            pagecolumns.append(col)
            col = list()
        prevtexttag = texttag
    pagecolumns.append(col)        
    return pagecolumns

'''
Combine Superscript and subscript.
Combine divided lines
if page has only one column, then can check for interleavings??
'''

def combineSubAndSuperScripts(page):
    prevtexttag = page.find('text')
    texttags = list()
    for texttag in page.findall('text'):
        newtexttag = texttag
        currtop = int(texttag.attrib['top'])
        currheight = int(texttag.attrib['height'])
        prevheight = int(prevtexttag.attrib['height'])
        prevtop = int(prevtexttag.attrib['top'])
        prevleft = int(prevtexttag.attrib['left'])
        prevwidth = int(prevtexttag.attrib['width'])
        currleft = int(texttag.attrib['left'])
        doTextsMerge = prevtop + prevheight > currtop or math.fabs(prevtop - currtop) < currheight
        doLeftsMerge = math.fabs(prevleft + prevwidth - currleft) < Constants.SUBSCRIPT_LEFT_THRESHOLD
        
        if (doTextsMerge and doLeftsMerge and len(texttags) is not 0): #Subscript or superscript
            previnsertedtexttag = texttags.pop()
            previnsertedtexttag[1].text = previnsertedtexttag[1].text + texttag.text
            previnsertedtexttag[1].attrib['width'] = str(int(previnsertedtexttag[1].attrib['width']) + int(texttag.attrib['width'])) 
            #print "Combined " + prevtexttag[1].text
            newtexttag = previnsertedtexttag[1]
            
        texttags.append([SparseType.NONSPARSE, newtexttag])
        prevtexttag = newtexttag
    
    return texttags

def combineTextPieces(page):
    subSupCombinedTexttags =  combineSubAndSuperScripts(page)
    prevtexttag = subSupCombinedTexttags[0][1]
    texttags = list()
    
    for tup in subSupCombinedTexttags:
        texttag = tup[1] 
        
        newtexttag = texttag
        currtop = int(texttag.attrib['top'])
        prevtop = int(prevtexttag.attrib['top'])
        prevleft = int(prevtexttag.attrib['left'])
        prevwidth = int(prevtexttag.attrib['width'])
        currleft = int(texttag.attrib['left'])
        
        if(prevtop is currtop and len(texttags) is not 0):
            previnsertedtexttag = texttags.pop()
            nospaces = math.fabs(prevleft + prevwidth - currleft)
            space= ''
            for r in xrange(int(nospaces)):
                space += ' '
            previnsertedtexttag[1].text = previnsertedtexttag[1].text + space + texttag.text
            previnsertedtexttag[1].attrib['width'] = str(int(previnsertedtexttag[1].attrib['width']) + int(texttag.attrib['width'])) 
            newtexttag = previnsertedtexttag[1]
            texttags.append([SparseType.SPARSEUNKNOWN, newtexttag])
            
        else:
            texttags.append([SparseType.NONSPARSE, texttag])
            
        prevtexttag = newtexttag
        
        #or math.fabs(prevtop - currtop) < currheight/Constants.SAME_LINE_HEIGHT_FACTOR   
    f = open('a.xml','w')
    for r in texttags:
        f.write(ET.tostring(r[1]))
    f.close()    
    return texttags   


def getFontDictionary(parseTree):
    fontdict = dict()
    fontspecTags = parseTree.iter('fontspec')
    for tags in fontspecTags:
        fontdict[int(tags.attrib['id'])] = int(tags.attrib['size'])
    return fontdict

def preprocessxml(xmlloc):
    xmlloc = removeBandITags(xmlloc)
    parseTree = ET.parse(xmlloc)
    
    for page in parseTree.iter('page'):
        #fontdict = getFontDictionary(parseTree)
        combinedPage = combineTextPieces(page)
        #columns = findColumns(page)
        #print "For Page " + page.attrib['number'] + " Col = " +str(len(columns)) 
    
if __name__ == '__main__':
    preprocessxml("../TrainingData/xmls/combinetest.xml") #<Sparse/NonSparse, tag>
    '''
        Train/Test using CRF
    '''