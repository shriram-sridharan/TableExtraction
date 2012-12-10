#!/usr/bin/python
import cgi
form = cgi.FieldStorage()
print "Content-type: text/html\r\n\r\n"
filename = form.getvalue('xmlname')
doc = dict()
for r in form.keys():
    if(r.startswith('pagebegin')):
        pageno = int(r[9:])
        if(doc.has_key(pageno)):
            continue
        collist = list()
        colbegin = int(form.getvalue(r))
        colend = int(form.getvalue('pageend'+str(pageno)))
        for cols in xrange(colbegin,colend):
            ibegin = int(form.getvalue('colbegin'+str(cols)))
            iend = int(form.getvalue('colend'+str(cols)))
            tuplist = list()
            sparsebegin = False
            for i in xrange(ibegin, iend):
                if(form.getvalue('docparams'+str(i)) == "sparse"):
                    sparsebegin = not sparsebegin
                    tup0 = 1
                elif(sparsebegin == True):
                    tup0 = 1
                else:
                    tup0 = 2
                tuplist.append([tup0, form.getvalue('texttag'+str(i))])
            collist.append(tuplist)
        doc[pageno] = collist

f = open(filename+"_annotated",'w')
for r in doc.keys():
    f.write("=============================== PAGE ===================================\n")
    for col in doc[r]:
        f.write("=============================== COL ===================================\n")
        for tup in col:
            print tup[1]
            f.write(str(tup[0])+ " " + tup[1].decode('ascii','ignore'))
f.close()