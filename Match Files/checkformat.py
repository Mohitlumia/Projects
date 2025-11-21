
def checkFormat(fileName, Formats):

	format_type = fileName.split('.')[-1]
	for Format in Formats:
		if format_type == 'pdf':
			return 'pdf'
		elif format_type == Format:
			return True
		else:
			return False