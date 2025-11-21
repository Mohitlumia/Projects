import os
from checkformat import checkFormat
from match import match

m = match()


location = '/storage/emulated/0/python'
Formats = ['py', 'txt', 'html', 'pdf']

word = r'numbers'


def mainFun(loc):
	
	for name in os.listdir(loc):
		# add file name with location
		fileLoc = '{}/{}'.format(loc, name)
		# if found pdf file
		if checkFormat(name, Formats) == 'pdf':
			# open the Pdf file and search for the word
			if m.matchedPdf(fileLoc, word):
				# print location of file
				print('\n', loc)
				# print name
				print(name)
		# check for the readable file
		elif checkFormat(name, Formats):
			# open the file and search for the word
			if m.matchedFile(fileLoc, word):
				# print location of file
				print('\n', loc)
				# print name
				print(name)
		# pretend file to be a folder and repeat the function
		try:
			mainFun(fileLoc)
		except Exception:
			pass


mainFun(location)
