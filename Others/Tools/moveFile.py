import os, shutil


locFrom = ''
locTo = ''
'''make sure to not have '/' at
   the end of location'''

Formats = ['jpeg','jpg','png','gif']


def MoveFile(locF,locT):
	
	for f in os.listdir(locF):
		file_name, file_ext = os.path.splitext(f)
		
		locN = locF+'/'+f

		for F in Formats:
			if "."+F == file_ext:
				try:
					shutil.move(locN,locT)
				except Exception:
						pass
		else:
			try:
				MoveFile(locN,locT)
			except Exception:
				pass

MoveFile(locFrom,locTo)

