Dependencies:
1. PyML

To test the code
1. Please navigate to the ./src folder
2. Use pdftohtml to convert the pdf to the xml using the following command
	pdftohtml -xml <name of pdf> <name of output xml>
3. Place the output xml in /TrainingData/xmls/cs/

TO run code

Run python TableDetector.py <name of test xml file> <method to test on> <detectonly>
The <method to test on> can be 1 - SVM, 2 - CRF, 3 - LR
<detectonly> -> This option specifies whether only table has to be only detected or decomposed too. C
		Can be T or F. 

Example command:
If the xml file is named 1.xml, then
	python TableDetector.py 1 2 T
will only detect tables using a CRF





