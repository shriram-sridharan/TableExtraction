'''
Created on Nov 20, 2012

@author: shriram
'''
import xml.etree.ElementTree as ET


def removeBandITags(xmlloc):
    f = open(xmlloc, 'r')
    f1 = open(xmlloc + '_tag', 'w')
    for line in f:
        f1.write(line.replace('<b>', '').replace('</b>', '').replace('<i>', '').replace('</i>', ''))
    
    f.close()
    f1.close()
    
    return xmlloc+'_tag'

def processedxml(xmlloc):
    xmlloc = removeBandITags(xmlloc)
    parseTree = ET.parse(xmlloc)
    # How to identify number of columns in a page - Use the height for sentence combining and marked difference for column identifying
    
if __name__ == '__main__':
    #preprocessedxml = preprocessxml(xmlloc) #<Sparse/NonSparse, tag>
    '''
        Train/Test using CRF
    '''