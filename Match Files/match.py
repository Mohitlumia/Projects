import PyPDF2
import re

class match():
	
	def matchedPdf(self, fileLoc, word):
		pdf_read = PyPDF2.PdfFileReader(fileLoc)
		
		for i in range(pdf_read.getNumPages()):
			pdf_page = pdf_read.getPage(i)
			page_text = pdf_page.extractText()
	
			if re.search(word, page_text):
				return True
	
	
	def matchedFile(self, fileLoc, word):
		try:
			openFile = open(fileLoc, 'r')
			fileText = openFile.read()
			if re.search(word, fileText):
				return True
			openFile.close()
		except Exception:
			return False
