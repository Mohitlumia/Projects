import os

os.chdir('/storage/emulated/0/Documents/')
print(os.getcwd())
print('')

for f in os.listdir():
	print(f)
	file_name, file_ext = os.path.splitext(f)
	f_n = file_name.split('-')
	print(f_n)
	new_name = '{}-{}{}'.format(f_n[1], f_n[0], file_ext)
	os.rename(f, new_name)
