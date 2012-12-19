Dependencies:
1. PyML

To test the code
1. Please navigate to the ./src folder
2. Use pdftohtml to convert the pdf to the xml using the following command
	pdftohtml -xml <name of pdf> <name of output xml>
3. Place the output xml in /TrainingData/xmls/cs/
4. python TableDetector.py <name of test xml file> <method to test on>
The <method to test on> can be 1 - SVM, 2 - CRF, 3 - LR

Example command:
If the xml file is named 1.xml, then
	python TableDetector.py 1 2
will test this on a CRF
