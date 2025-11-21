def count_char(text, char):
	count = 0
	for c in text:
		if c == char:
			count += 1
	return count
			
filename = input("Enter a file name: ")
with open(filename) as f:
	text = f.read()

print(count_char(('''<!DOCTYPE html>

<p>This is<br/> paragraph 1</p>

<p>This is paragraph 2</p>

<p>This is paragraph 3</p>

<p>This is paragraph 4</p>

<p>This is paragraph 5</p>

<p>This is paragraph 6</p>

</body>

</html''').split(), "paragraph"))

print(count_char(text, 's'))

for char in "abcdefghijklmnopqrstuvwxyz":
	perc = 100*count_char(text, char)/len(text)
	print("{0} - {1}%".format(char, round(perc, 2)))
# last line 'char' for {0} and round(perc, 2) for {1} and in round(perc, 2) represents 2 digits of float