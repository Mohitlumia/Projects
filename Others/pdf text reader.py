import PyPDF2

def main():
	
	pdf_file = "/sdcard/Download/1115578486017084040907.pdf"
	pdf_read = PyPDF2.PdfFileReader(pdf_file)
	pdf_page = pdf_read.getPage(5)
	page_text = pdf_page.extractText()
	print(page_text)

if __name__ == "__main__":
	main()

	